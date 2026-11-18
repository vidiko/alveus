# SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
# SPDX-License-Identifier: EUPL-1.2
"""Mechanical completeness check for the pull request clean-room attestation.

This module implements check 2 of CLEANROOM.md ("Attestation"). It derives the
required checkboxes and fields at run time from the ``## Clean-Room
Attestation`` section of ``.github/pull_request_template.md`` and verifies that
a pull request body contains that section once, checks every required box, and
provides non-empty, non-placeholder list items for every required field.

The module-level constant ``PLACEHOLDERS`` holds the lowercase word and phrase
tokens rejected as placeholder list items (in addition to empty items,
punctuation-only items, and angle-bracketed ``<...>`` placeholders). The
answers ``none`` and ``None.`` are valid disclosures and are not in
``PLACEHOLDERS``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from markdown_it.token import Token

_MISSING_PARSER_ERROR: str = (
    "markdown-it-py is not installed; install tools/cleanroom/requirements.txt"
)

try:
    from markdown_it import MarkdownIt
except ImportError:
    _PARSER: MarkdownIt | None = None
else:
    _PARSER = MarkdownIt("commonmark").enable("table")

MAX_BODY_CHARS: int = 65536
ATTESTATION_HEADING: str = "clean-room attestation"
PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "tbd",
        "todo",
        "fixme",
        "xxx",
        "placeholder",
        "fill in",
        "n/a",
        "na",
    }
)

_BOX_MARKER_RE = re.compile(r"^\[([ xX])\](?:\s|$)")
_URI_AUTOLINK_RE = re.compile(r"^<[A-Za-z][A-Za-z0-9+.-]{1,31}:[^\s<>]*>$")
_EMAIL_AUTOLINK_RE = re.compile(
    r"^<[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9]"
    r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*>$"
)


@dataclass(frozen=True)
class TemplateSpec:
    """Attestation requirements derived from the pull request template."""

    boxes: tuple[str, ...]
    fields: tuple[str, ...]


@dataclass(frozen=True)
class Problem:
    """One completeness problem found in a pull request attestation."""

    code: str
    detail: str


def is_placeholder(item: str) -> bool:
    """Return whether a list item's text is empty or a placeholder."""
    text = " ".join(item.split())
    if not text:
        return True
    if all(ch in "-.…?" for ch in text):
        return True
    if text.startswith("<") and text.endswith(">"):
        return (
            _URI_AUTOLINK_RE.match(text) is None
            and _EMAIL_AUTOLINK_RE.match(text) is None
        )
    lowered = text.casefold()
    return lowered in PLACEHOLDERS or lowered.rstrip(".:") in PLACEHOLDERS


def _render_children(children: Sequence[Token]) -> str:
    """Render inline child tokens to whitespace-collapsed plain text."""
    parts: list[str] = []
    for child in children:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return " ".join("".join(parts).split())


def _render_inline(token: Token) -> str:
    """Render an inline token's children to whitespace-collapsed plain text."""
    return _render_children(token.children or ())


def _field_label(inline_token: Token) -> str | None:
    """Return the label of a field paragraph inline token, or None."""
    children = [
        child
        for child in (inline_token.children or ())
        if not (child.type == "text" and not child.content)
    ]
    if not children or children[0].type != "strong_open":
        return None
    inner: list[Token] = []
    for child in children[1:]:
        if child.type == "strong_close":
            break
        inner.append(child)
    return _render_children(inner)


def _extract_sections(text: str) -> list[list[Token]]:
    """Parse text and return token slices for Clean-Room Attestation sections."""
    if _PARSER is None:
        raise RuntimeError(_MISSING_PARSER_ERROR)
    tokens = _PARSER.parse(text)
    sections: list[list[Token]] = []
    current: list[Token] | None = None
    skip_until = -1
    for index, token in enumerate(tokens):
        if index < skip_until:
            continue
        if token.type == "heading_open" and token.tag in ("h1", "h2"):
            title = (
                _render_inline(tokens[index + 1])
                if index + 1 < len(tokens) and tokens[index + 1].type == "inline"
                else ""
            )
            if (
                token.level == 0
                and token.tag == "h2"
                and title.casefold() == ATTESTATION_HEADING
            ):
                current = []
                sections.append(current)
                skip_until = index + 3
                continue
            current = None
            continue
        if current is not None:
            current.append(token)
    return sections


def _parse_boxes(tokens: Sequence[Token]) -> list[tuple[bool, str]]:
    """Extract (checked, collapsed_text) checkboxes before the first field."""
    boxes: list[tuple[bool, str]] = []
    in_bullet_list = False
    for index, token in enumerate(tokens):
        if (
            token.level == 0
            and token.type == "paragraph_open"
            and index + 1 < len(tokens)
            and _field_label(tokens[index + 1]) is not None
        ):
            break
        if token.level == 0 and token.type == "bullet_list_open":
            in_bullet_list = True
        elif token.level == 0 and token.type == "bullet_list_close":
            in_bullet_list = False
        elif (
            in_bullet_list
            and token.level == 1
            and token.type == "list_item_open"
            and index + 2 < len(tokens)
            and tokens[index + 1].type == "paragraph_open"
            and tokens[index + 1].level == 2
            and tokens[index + 2].type == "inline"
        ):
            inline_tok = tokens[index + 2]
            match = _BOX_MARKER_RE.match(inline_tok.content)
            if match is not None:
                checked = match.group(1) in ("x", "X")
                text = _render_inline(inline_tok)[3:].strip()
                boxes.append((checked, text))
    return boxes


def _collect_answer_token(
    tokens: Sequence[Token],
    index: int,
    current_items: list[str],
    bullet_stack: list[bool],
    item_stack: list[tuple[int, int, list[str] | None]],
) -> None:
    """Update list and item stacks for one token inside a field answer region."""
    token = tokens[index]
    if token.type in ("bullet_list_open", "ordered_list_open"):
        is_bullet = token.type == "bullet_list_open" and (
            token.level == 0 or (bool(bullet_stack) and bullet_stack[-1])
        )
        bullet_stack.append(is_bullet)
    elif token.type in ("bullet_list_close", "ordered_list_close"):
        bullet_stack.pop()
    elif token.type == "list_item_open":
        if bullet_stack and bullet_stack[-1]:
            current_items.append("")
            item_stack.append((token.level, len(current_items) - 1, []))
        else:
            item_stack.append((token.level, -1, None))
    elif token.type == "list_item_close":
        _, slot, parts = item_stack.pop()
        if parts is not None:
            current_items[slot] = " ".join(part for part in parts if part)
    elif (
        token.type == "paragraph_open"
        and item_stack
        and item_stack[-1][2] is not None
        and token.level == item_stack[-1][0] + 1
        and index + 1 < len(tokens)
        and tokens[index + 1].type == "inline"
    ):
        item_stack[-1][2].append(_render_inline(tokens[index + 1]))


def _parse_fields(tokens: Sequence[Token]) -> dict[str, list[str]]:
    """Extract field labels and their collapsed list items from section tokens."""
    fields: dict[str, list[str]] = {}
    current_items: list[str] | None = None
    bullet_stack: list[bool] = []
    item_stack: list[tuple[int, int, list[str] | None]] = []
    skip_until = -1
    for index, token in enumerate(tokens):
        if index < skip_until:
            continue
        if token.level == 0 and token.type == "paragraph_open":
            label = _field_label(tokens[index + 1]) if index + 1 < len(tokens) else None
            if label is not None:
                current_items = fields.setdefault(label, [])
                skip_until = index + 3
                continue
        if current_items is not None:
            _collect_answer_token(
                tokens, index, current_items, bullet_stack, item_stack
            )
    return fields


def load_template(path: Path) -> TemplateSpec:
    """Derive the attestation box and field specification from template path."""
    if _PARSER is None:
        raise RuntimeError(_MISSING_PARSER_ERROR)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"cannot read template {path}: {exc}"
        raise ValueError(msg) from exc
    sections = _extract_sections(raw)
    if len(sections) != 1:
        msg = f"template {path} must contain exactly one attestation section"
        raise ValueError(msg)
    boxes = tuple(text for _, text in _parse_boxes(sections[0]) if text)
    fields = tuple(_parse_fields(sections[0]).keys())
    if not boxes or not fields:
        msg = f"template {path} attestation section is missing boxes or fields"
        raise ValueError(msg)
    return TemplateSpec(boxes=boxes, fields=fields)


def _check_boxes(spec: TemplateSpec, section: Sequence[Token]) -> list[Problem]:
    """Check that every template box is present and checked in section."""
    found: dict[str, bool] = {}
    for checked, text in _parse_boxes(section):
        found[text] = found.get(text, True) and checked
    problems: list[Problem] = []
    for index, expected in enumerate(spec.boxes, 1):
        short = expected[:60] + ("..." if len(expected) > 60 else "")
        if expected not in found:
            problems.append(
                Problem("missing-box", f"box {index} is missing ({short!r})")
            )
        elif not found[expected]:
            problems.append(
                Problem("unchecked-box", f"box {index} is not checked ({short!r})")
            )
    return problems


def _check_fields(spec: TemplateSpec, section: Sequence[Token]) -> list[Problem]:
    """Check that every template field is present, non-empty and filled."""
    found = _parse_fields(section)
    problems: list[Problem] = []
    for label in spec.fields:
        if label not in found:
            problems.append(Problem("missing-field", f"field '{label}' is missing"))
            continue
        items = found[label]
        if not any(item for item in items):
            problems.append(
                Problem(
                    "empty-field",
                    f"field '{label}' has no list item with text; "
                    'write each answer as a "- " list item',
                )
            )
        elif any(is_placeholder(item) for item in items):
            problems.append(
                Problem(
                    "placeholder-field",
                    f"field '{label}' contains a placeholder entry",
                )
            )
    return problems


def check_body(spec: TemplateSpec, body: str | None) -> list[Problem]:
    """Validate a pull request body against spec and return all problems."""
    if _PARSER is None:
        raise RuntimeError(_MISSING_PARSER_ERROR)
    text = body or ""
    if len(text) > MAX_BODY_CHARS:
        return [
            Problem(
                "oversized-body",
                f"pull request body length {len(text)} exceeds {MAX_BODY_CHARS}",
            )
        ]
    sections = _extract_sections(text)
    if not sections:
        return [
            Problem(
                "missing-block",
                "missing '## Clean-Room Attestation' section",
            )
        ]
    if len(sections) > 1:
        return [
            Problem(
                "duplicate-block",
                "'## Clean-Room Attestation' section appears more than once",
            )
        ]
    return _check_boxes(spec, sections[0]) + _check_fields(spec, sections[0])


def _read_event_body(path: Path) -> str:
    """Read pull_request.body from a GitHub Actions event JSON file."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"cannot read event file {path}: {exc}"
        raise ValueError(msg) from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in event file {path}: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(data, dict) or not isinstance(data.get("pull_request"), dict):
        msg = f"event file {path} has no 'pull_request' object"
        raise TypeError(msg)
    pr = data["pull_request"]
    if "body" not in pr or (pr["body"] is not None and not isinstance(pr["body"], str)):
        msg = f"event file {path} has no string or null 'pull_request.body'"
        raise TypeError(msg)
    return pr["body"] or ""


def _read_markdown_body(path: Path) -> str:
    """Read a pull request body from a Markdown file."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"cannot read body file {path}: {exc}"
        raise ValueError(msg) from exc


def _build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Check that a pull request's clean-room attestation is complete."
    )
    parser.add_argument(
        "--template",
        type=Path,
        required=True,
        help="Path to .github/pull_request_template.md.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--event",
        type=Path,
        help="Path to the GitHub Actions event JSON payload.",
    )
    source.add_argument(
        "--body",
        type=Path,
        help="Path to a Markdown file containing the pull request body.",
    )
    parser.add_argument(
        "--annotations",
        action="store_true",
        help="Emit GitHub Actions ::error workflow annotations on failure.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return 0 on pass, 1 on incomplete, or 2 on usage error."""
    args = _build_parser().parse_args(argv)
    try:
        spec = load_template(args.template)
        body = (
            _read_event_body(args.event)
            if args.event is not None
            else _read_markdown_body(args.body)
        )
        problems = check_body(spec, body)
    except (RuntimeError, TypeError, ValueError) as exc:
        print(f"attestation: error: {exc}", file=sys.stderr)
        return 2
    if not problems:
        print("attestation: pass")
        return 0
    for problem in problems:
        print(f"attestation: {problem.code}: {problem.detail}")
        if args.annotations:
            print(
                f"::error title=Clean-room attestation::"
                f"{problem.code}: {problem.detail}"
            )
    print(f"attestation: fail ({len(problems)} problems)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
