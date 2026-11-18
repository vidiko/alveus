# SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
# SPDX-License-Identifier: EUPL-1.2
"""Positive, negative and boundary cases for docs/hooks/repo_links.py.

Run from the repository root: python3 -I -B docs/hooks/test_repo_links.py .
"""

import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SPEC = importlib.util.spec_from_file_location("repo_links", ROOT / "docs/hooks/repo_links.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
CFG = {
    "docs_dir": str(ROOT / "docs"),
    "repo_url": "https://github.com/vidiko/alveus",
    "edit_uri": "edit/main/docs/",
}
PAGE = types.SimpleNamespace(file=types.SimpleNamespace(src_uri="index.md", src_path="index.md"))
B = "https://github.com/vidiko/alveus/blob/main/"
CASES = [
    (CFG, "[a](../CLEANROOM.md)", f"[a]({B}CLEANROOM.md)"),
    (CFG, "[a](../CLEANROOM.md#roles)", f"[a]({B}CLEANROOM.md#roles)"),
    (CFG, "[a](plan/README.md)", "[a](plan/README.md)"),
    (CFG, "![i](../CLEANROOM.md)", "![i](../CLEANROOM.md)"),
    (CFG, "`[a](../CLEANROOM.md)`", "`[a](../CLEANROOM.md)`"),
    (CFG, "``x `[a](../CLEANROOM.md)` y``", "``x `[a](../CLEANROOM.md)` y``"),
    (CFG, "```md\n[a](../CLEANROOM.md)\n```\n[b](../CLEANROOM.md)",
     f"```md\n[a](../CLEANROOM.md)\n```\n[b]({B}CLEANROOM.md)"),
    (CFG, "~~~~\n[a](../CLEANROOM.md)\n~~~\nstill\n~~~~\n[b](../LICENSE)",
     f"~~~~\n[a](../CLEANROOM.md)\n~~~\nstill\n~~~~\n[b]({B}LICENSE)"),
    (CFG, "[a](https://example.org/x)", "[a](https://example.org/x)"),
    (CFG, "[a](#here)", "[a](#here)"),
    (CFG, "[a](../NO-SUCH.md)", "[a](../NO-SUCH.md)"),
    (dict(CFG, edit_uri=""), "[a](../LICENSE)",
     "[a](https://github.com/vidiko/alveus/blob/HEAD/LICENSE)"),
]


def main() -> int:
    bad = 0
    for cfg, src, want in CASES:
        got = MOD.on_page_markdown(src, PAGE, cfg, None)
        ok = got == want
        bad += 0 if ok else 1
        print("ok  " if ok else "FAIL", repr(src), "" if ok else f"-> {got!r}")
    print(f"cases={len(CASES)} failed={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
