# SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
# SPDX-License-Identifier: EUPL-1.2
"""MkDocs hook that rewrites relative links leaving docs/ to repository URLs.

A page such as docs/index.md may link ../CLEANROOM.md. MkDocs cannot serve that
file, so the hook points the link at the file on the forge instead. Links inside
code spans and fenced code blocks stay as written. A link leaving docs/ whose
target does not exist is logged as a warning, which fails a strict build.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

_LOG = logging.getLogger("mkdocs.hooks.repo_links")
# A code span (kept as is) or an inline link that is not an image.
_TOKEN_RE = re.compile(
    r"(?P<code>(?P<ticks>`+)[^`]*?(?P=ticks))"
    r"|(?<!!)(?P<label>\[[^\[\]\n]+\])\((?P<target>[^()\s]+)\)"
)
_FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
_SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "/", "#")


def _blob_base(config: Any) -> str:
    """Return <repo_url>/blob/<branch>, the branch taken from edit_uri."""
    repo_url = str(config.get("repo_url") or "").rstrip("/")
    edit_uri = str(config.get("edit_uri") or "").strip("/")
    parts = edit_uri.split("/")
    branch = parts[1] if len(parts) > 1 and parts[0] in ("edit", "blob") else "HEAD"
    return f"{repo_url}/blob/{branch}"


def _rewrite_target(raw_target: str, page: dict[str, Any]) -> str:
    """Resolve one link target and rewrite it when it leaves docs/."""
    if raw_target.startswith(_SKIP_PREFIXES) or "://" in raw_target:
        return raw_target
    target_path, sep, anchor = raw_target.partition("#")
    if not target_path:
        return raw_target
    resolved = Path(os.path.normpath(page["dir"] / target_path))
    if resolved.is_relative_to(page["docs_dir"]):
        return raw_target
    repo_root = page["docs_dir"].parent
    if resolved.is_relative_to(repo_root) and resolved.exists():
        rel_repo = resolved.relative_to(repo_root).as_posix()
        fragment = f"#{anchor}" if sep else ""
        return f"{page['blob_base']}/{rel_repo}{fragment}"
    _LOG.warning(
        "Doc file '%s' contains a link '%s' outside docs/, but target does not exist.",
        page["src_uri"],
        raw_target,
    )
    return raw_target


def _closes(line: str, fence: str) -> bool:
    """Return whether line closes a fenced block opened with fence."""
    closer = _FENCE_RE.match(line)
    if closer is None:
        return False
    run = closer.group("fence")
    same_kind = run[0] == fence[0] and len(run) >= len(fence)
    return same_kind and not line.strip().strip(run[0])


def _rewrite_prose(text: str, page: dict[str, Any]) -> str:
    """Rewrite inline links in prose, leaving code spans untouched."""

    def _replace(match: re.Match[str]) -> str:
        if match.group("code") is not None:
            return match.group(0)
        target = _rewrite_target(match.group("target"), page)
        return f"{match.group('label')}({target})"

    return _TOKEN_RE.sub(_replace, text)


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    """Rewrite relative Markdown links that leave docs/ to forge blob URLs."""
    del files
    docs_dir = Path(os.path.abspath(str(config["docs_dir"])))
    src_uri = str(
        getattr(page.file, "src_uri", None) or page.file.src_path
    ).replace("\\", "/")
    context = {
        "docs_dir": docs_dir,
        "dir": Path(os.path.normpath(docs_dir / src_uri)).parent,
        "src_uri": src_uri,
        "blob_base": _blob_base(config),
    }
    out: list[str] = []
    prose: list[str] = []
    fence = ""
    for line in markdown.splitlines(keepends=True):
        opener = _FENCE_RE.match(line)
        if not fence and opener:
            out.append(_rewrite_prose("".join(prose), context))
            prose = []
            fence = opener.group("fence")
            out.append(line)
        elif fence:
            out.append(line)
            if _closes(line, fence):
                fence = ""
        else:
            prose.append(line)
    out.append(_rewrite_prose("".join(prose), context))
    return "".join(out)
