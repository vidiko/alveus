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

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_HEADING_RE = re.compile(r"^(#{1,2})(?:[ \t]+(.*?))?[ \t]*$")
_BOX_RE = re.compile(r"^[ \t]*[-*][ \t]+\[([ xX])\](?:[ \t]+(.*))?$")
_FIELD_RE = re.compile(r"^\*\*([^*\n]+)\*\*")
_BULLET_RE = re.compile(r"^[ \t]*[-*](?:[ \t]+(.*))?$")


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


def _collapse(parts: Sequence[str]) -> str:
    """Join text parts and collapse whitespace runs to single spaces."""
    return " ".join(" ".join(parts).split())


def _clean_text(raw: str) -> str:
    """Normalise CRLF and CR line endings to LF and strip HTML comments."""
    normalised = raw.replace("\r\n", "\n").replace("\r", "\n")
    return _COMMENT_RE.sub("", normalised)


def is_placeholder(item: str) -> bool:
    """Return whether a list item's text is empty or a placeholder."""
    text = " ".join(item.split())
    if not text:
        return True
    if all(ch in "-.…?" for ch in text):
        return True
    if text.startswith("<") and text.endswith(">"):
        return True
    lowered = text.casefold()
    return lowered in PLACEHOLDERS or lowered.rstrip(".:") in PLACEHOLDERS


def _extract_blocks(text: str) -> list[list[str]]:
    """Return the line lists of all Clean-Room Attestation sections in text."""
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match is not None:
            level = match.group(1)
            title = (match.group(2) or "").strip()
            if level == "##" and title.casefold() == ATTESTATION_HEADING:
                current = []
                blocks.append(current)
            else:
                current = None
            continue
        if current is not None:
            current.append(line)
    return blocks


def _parse_boxes(lines: Sequence[str]) -> list[tuple[bool, str]]:
    """Extract (checked, collapsed_text) checkboxes before the first field."""
    boxes: list[tuple[bool, str]] = []
    active_parts: list[str] | None = None
    active_checked = False
    for line in lines:
        if _FIELD_RE.match(line) is not None:
            break
        box_match = _BOX_RE.match(line)
        if box_match is not None:
            if active_parts is not None:
                boxes.append((active_checked, _collapse(active_parts)))
            active_checked = box_match.group(1) in ("x", "X")
            active_parts = [box_match.group(2) or ""]
        elif not line.strip() or _BULLET_RE.match(line) is not None:
            if active_parts is not None:
                boxes.append((active_checked, _collapse(active_parts)))
                active_parts = None
        elif active_parts is not None:
            active_parts.append(line.strip())
    if active_parts is not None:
        boxes.append((active_checked, _collapse(active_parts)))
    return boxes


def _parse_fields(lines: Sequence[str]) -> dict[str, list[str]]:
    """Extract field labels and their collapsed list items from block lines."""
    fields: dict[str, list[str]] = {}
    current_items: list[str] | None = None
    active_parts: list[str] | None = None
    for line in lines:
        field_match = _FIELD_RE.match(line)
        if field_match is not None:
            if current_items is not None and active_parts is not None:
                current_items.append(_collapse(active_parts))
            label = " ".join(field_match.group(1).split())
            current_items = fields.setdefault(label, [])
            active_parts = None
            continue
        if current_items is None:
            continue
        bullet_match = _BULLET_RE.match(line)
        if bullet_match is not None:
            if active_parts is not None:
                current_items.append(_collapse(active_parts))
            active_parts = [bullet_match.group(1) or ""]
        elif not line.strip():
            if active_parts is not None:
                current_items.append(_collapse(active_parts))
                active_parts = None
        elif active_parts is not None:
            active_parts.append(line.strip())
    if current_items is not None and active_parts is not None:
        current_items.append(_collapse(active_parts))
    return fields


def load_template(path: Path) -> TemplateSpec:
    """Derive the attestation box and field specification from template path."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"cannot read template {path}: {exc}"
        raise ValueError(msg) from exc
    blocks = _extract_blocks(_clean_text(raw))
    if len(blocks) != 1:
        msg = f"template {path} must contain exactly one attestation section"
        raise ValueError(msg)
    boxes = tuple(text for _, text in _parse_boxes(blocks[0]) if text)
    fields = tuple(_parse_fields(blocks[0]).keys())
    if not boxes or not fields:
        msg = f"template {path} attestation section is missing boxes or fields"
        raise ValueError(msg)
    return TemplateSpec(boxes=boxes, fields=fields)


def _check_boxes(spec: TemplateSpec, block: Sequence[str]) -> list[Problem]:
    """Check that every template box is present and checked in block."""
    found: dict[str, bool] = {}
    for checked, text in _parse_boxes(block):
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


def _check_fields(spec: TemplateSpec, block: Sequence[str]) -> list[Problem]:
    """Check that every template field is present, non-empty and filled."""
    found = _parse_fields(block)
    problems: list[Problem] = []
    for label in spec.fields:
        if label not in found:
            problems.append(Problem("missing-field", f"field '{label}' is missing"))
            continue
        items = found[label]
        if not any(item for item in items):
            problems.append(Problem("empty-field", f"field '{label}' has no content"))
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
    text = body or ""
    if len(text) > MAX_BODY_CHARS:
        return [
            Problem(
                "oversized-body",
                f"pull request body length {len(text)} exceeds {MAX_BODY_CHARS}",
            )
        ]
    blocks = _extract_blocks(_clean_text(text))
    if not blocks:
        return [
            Problem(
                "missing-block",
                "missing '## Clean-Room Attestation' section",
            )
        ]
    if len(blocks) > 1:
        return [
            Problem(
                "duplicate-block",
                "'## Clean-Room Attestation' section appears more than once",
            )
        ]
    return _check_boxes(spec, blocks[0]) + _check_fields(spec, blocks[0])


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
    except (TypeError, ValueError) as exc:
        print(f"attestation: error: {exc}", file=sys.stderr)
        return 2
    problems = check_body(spec, body)
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
