# SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
# SPDX-License-Identifier: EUPL-1.2
"""Test tools/cleanroom/attestation.py."""

# Run from the repository root: python3 -I -B tools/cleanroom/test_attestation.py .

from __future__ import annotations

import contextlib
import importlib
import io
import json
import subprocess  # nosec B404  # Fixed python3 argv, no shell.
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1]).resolve()
sys.path.append(str(ROOT / "tools/cleanroom"))
MOD = importlib.import_module("attestation")

TEMPLATE = ROOT / ".github/pull_request_template.md"
FIXTURES = ROOT / "tools/cleanroom/fixtures/attestation"
SCRIPT = ROOT / "tools/cleanroom/attestation.py"

PASS_FIXTURES: tuple[str, ...] = (
    "complete.md",
    "complete-uppercase-reflowed.md",
    "complete-none-exposure.md",
    "complete-extra-sections.md",
    "autolink-inputs.md",
    "heading-forms.md",
    "fenced-example.md",
    "indented-backticks.md",
    "backtick-info-string.md",
)

# (fixture filename, expected problem code set, expected problem count).
FAIL_FIXTURES: tuple[tuple[str, frozenset[str], int], ...] = (
    ("no-block.md", frozenset({"missing-block"}), 1),
    ("unchecked-first.md", frozenset({"unchecked-box"}), 1),
    ("unchecked-both.md", frozenset({"unchecked-box"}), 2),
    ("box-deleted.md", frozenset({"missing-box"}), 1),
    ("box-reworded.md", frozenset({"missing-box"}), 1),
    ("empty-inputs.md", frozenset({"empty-field"}), 1),
    ("placeholder-roles.md", frozenset({"placeholder-field"}), 1),
    ("placeholder-angle.md", frozenset({"placeholder-field"}), 1),
    ("mixed-placeholder.md", frozenset({"placeholder-field"}), 1),
    ("field-missing.md", frozenset({"missing-field"}), 1),
    ("template-unfilled.md", frozenset({"unchecked-box", "empty-field"}), 5),
    ("comment-only-field.md", frozenset({"empty-field"}), 1),
    ("duplicate-block.md", frozenset({"duplicate-block"}), 1),
    ("wrong-level-heading.md", frozenset({"missing-block"}), 1),
    ("unclosed-comment.md", frozenset({"missing-block"}), 1),
    ("fenced-block.md", frozenset({"missing-block"}), 1),
    ("unclosed-fence.md", frozenset({"missing-block"}), 1),
    ("wrong-level-h1.md", frozenset({"missing-block"}), 1),
    ("paragraph-answer.md", frozenset({"empty-field"}), 1),
    ("indented-code-heading.md", frozenset({"missing-block"}), 1),
    ("tilde-fence-backtick-close.md", frozenset({"missing-block"}), 1),
    ("long-fence-short-close.md", frozenset({"missing-block"}), 1),
)

FAIL_DETAIL_EXPECTATIONS: dict[str, str] = {
    "paragraph-answer.md": (
        "field 'Past exposure to disclose' has no list item with text; "
        'write each answer as a "- " list item'
    ),
}

PLACEHOLDER_CASES: tuple[tuple[str, bool], ...] = (
    ("<document and clause>", True),
    ("<>", True),
    ("< https://x >", True),
    ("<https://a.b/c>", False),
    ("<a@b.org>", False),
    ("None.", False),
    ("<a:b>", True),
    ("<ab:c>", False),
    ("<" + "a" * 32 + ":x>", False),
    ("<" + "a" * 33 + ":x>", True),
    ("<http://x y>", True),
    ("<TODO: fill in>", True),
)

NON_LINE_SEPARATORS: tuple[tuple[str, str], ...] = (
    ("u000b-vt", "\x0b"),
    ("u000c-ff", "\x0c"),
    ("u001c-fs", "\x1c"),
    ("u001d-gs", "\x1d"),
    ("u001e-rs", "\x1e"),
    ("u0085-nel", "\x85"),
    ("u2028-ls", "\u2028"),
    ("u2029-ps", "\u2029"),
)


# (case name, argv with {tpl}/{tmp}/{fx} slots, expected rc, expected output needle).
# {tpl} = PR template, {tmp} = per-run temp dir, {fx} = fixture root.
_ERROR = "attestation: error:"
CLI_CASES: tuple[tuple[str, tuple[str, ...], int, str], ...] = (
    (
        "cli/event-pass",
        ("--template", "{tpl}", "--event", "{tmp}/event-pass.json"),
        0,
        "attestation: pass",
    ),
    (
        "cli/event-null-body",
        ("--template", "{tpl}", "--event", "{tmp}/event-null.json"),
        1,
        "attestation: missing-block:",
    ),
    (
        "cli/body-pass",
        ("--template", "{tpl}", "--body", "{fx}/pass/complete.md"),
        0,
        "attestation: pass",
    ),
    (
        "cli/annotations",
        (
            "--template",
            "{tpl}",
            "--body",
            "{fx}/fail/unchecked-first.md",
            "--annotations",
        ),
        1,
        "::error title=Clean-room attestation::unchecked-box:",
    ),
    (
        "cli/missing-template",
        ("--template", "{tmp}/no-such-template.md", "--body", "{fx}/pass/complete.md"),
        2,
        _ERROR,
    ),
    (
        "cli/bad-template-no-section",
        ("--template", "{fx}/fail/no-block.md", "--body", "{fx}/pass/complete.md"),
        2,
        _ERROR,
    ),
    (
        "cli/bad-json",
        ("--template", "{tpl}", "--event", "{tmp}/event-bad.json"),
        2,
        _ERROR,
    ),
    (
        "cli/no-pull-request-key",
        ("--template", "{tpl}", "--event", "{tmp}/event-nopr.json"),
        2,
        _ERROR,
    ),
)


def _report(name: str, ok: bool, detail: str = "") -> bool:
    """Print one test case outcome and return ok."""
    status = "ok  " if ok else "FAIL"
    suffix = f" -> {detail}" if not ok and detail else ""
    print(f"{status} {name}{suffix}")
    return ok


def _check_fixture_inventory() -> tuple[int, int]:
    """Ensure every pass/ and fail/ fixture file is listed in the tables."""
    actual_pass = {path.name for path in (FIXTURES / "pass").glob("*.md")}
    want_pass = set(PASS_FIXTURES)
    ok_pass = _report(
        "inventory pass/",
        actual_pass == want_pass,
        f"unlisted_or_missing={actual_pass ^ want_pass!r}",
    )
    actual_fail = {path.name for path in (FIXTURES / "fail").glob("*.md")}
    want_fail = {name for name, _, _ in FAIL_FIXTURES}
    ok_fail = _report(
        "inventory fail/",
        actual_fail == want_fail,
        f"unlisted_or_missing={actual_fail ^ want_fail!r}",
    )
    return 2, (0 if ok_pass else 1) + (0 if ok_fail else 1)


def _run_inprocess_main(argv: list[str]) -> tuple[int, str, str]:
    """Invoke MOD.main(argv) while capturing stdout and stderr."""
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
        rc = MOD.main(argv)
    return rc, out_buf.getvalue(), err_buf.getvalue()


def _check_pass_fixtures(spec: Any, tmp_dir: Path) -> tuple[int, int]:
    """Run every passing fixture and the runtime CRLF and CR fixtures."""
    cases = 0
    bad = 0
    for name in PASS_FIXTURES:
        path = FIXTURES / "pass" / name
        problems = MOD.check_body(spec, path.read_text(encoding="utf-8"))
        rc, out, _ = _run_inprocess_main(
            ["--template", str(TEMPLATE), "--body", str(path)]
        )
        ok = not problems and rc == 0 and out.strip() == "attestation: pass"
        bad += not _report(f"pass/{name}", ok, f"rc={rc} problems={problems!r}")
        cases += 1
    base_complete = (
        (FIXTURES / "pass/complete.md")
        .read_text(encoding="utf-8")
        .replace("\r\n", "\n")
    )
    for stem, newline in (("complete-crlf", "\r\n"), ("complete-cr", "\r")):
        alt_text = base_complete.replace("\n", newline)
        alt_path = tmp_dir / f"{stem}.md"
        alt_path.write_bytes(alt_text.encode("utf-8"))
        problems = MOD.check_body(spec, alt_text)
        rc, out, _ = _run_inprocess_main(
            ["--template", str(TEMPLATE), "--body", str(alt_path)]
        )
        ok = not problems and rc == 0 and out.strip() == "attestation: pass"
        bad += not _report(f"pass/{stem}", ok, f"rc={rc} problems={problems!r}")
        cases += 1
    return cases, bad


def _check_fail_fixtures(spec: Any) -> tuple[int, int]:
    """Run every failing fixture in-process and assert exact problem codes."""
    cases = 0
    bad = 0
    for name, want_codes, want_count in FAIL_FIXTURES:
        path = FIXTURES / "fail" / name
        problems = MOD.check_body(spec, path.read_text(encoding="utf-8"))
        got_codes = frozenset(item.code for item in problems)
        rc, out, _ = _run_inprocess_main(
            ["--template", str(TEMPLATE), "--body", str(path)]
        )
        want_tail = f"attestation: fail ({want_count} problems)"
        want_detail = FAIL_DETAIL_EXPECTATIONS.get(name)
        lines = out.strip().splitlines()
        ok = (
            rc == 1
            and got_codes == want_codes
            and len(problems) == want_count
            and len(lines) == want_count + 1
            and lines[-1] == want_tail
            and (want_detail is None or problems[0].detail == want_detail)
        )
        bad += not _report(
            f"fail/{name}",
            ok,
            f"rc={rc} codes={set(got_codes)!r} count={len(problems)}",
        )
        cases += 1
    for label, empty_val in (("fail/empty-string", ""), ("fail/null-body", None)):
        problems = MOD.check_body(spec, empty_val)
        got_codes = frozenset(item.code for item in problems)
        ok = got_codes == frozenset({"missing-block"}) and len(problems) == 1
        bad += not _report(label, ok, f"codes={set(got_codes)!r}")
        cases += 1
    return cases, bad


def _check_line_separators(spec: Any) -> tuple[int, int]:
    """Reject non-CommonMark line separators before the attestation heading."""
    base = (FIXTURES / "pass/complete.md").read_text(encoding="utf-8")
    target = "\n## Clean-Room Attestation"
    bad = 0
    for label, sep in NON_LINE_SEPARATORS:
        body = base.replace(target, f"\nSee notes.{sep}## Clean-Room Attestation", 1)
        problems = MOD.check_body(spec, body)
        got_codes = frozenset(item.code for item in problems)
        ok = (
            target in base
            and got_codes == frozenset({"missing-block"})
            and len(problems) == 1
        )
        bad += not _report(
            f"separator/{label}",
            ok,
            f"codes={set(got_codes)!r} count={len(problems)}",
        )
    return len(NON_LINE_SEPARATORS), bad


def _check_placeholder_cases() -> tuple[int, int]:
    """Check unit cases for MOD.is_placeholder including CommonMark autolinks."""
    bad = 0
    for item, want in PLACEHOLDER_CASES:
        got = MOD.is_placeholder(item)
        bad += not _report(
            f"placeholder/{item}",
            got is want,
            f"got={got!r} want={want!r}",
        )
    return len(PLACEHOLDER_CASES), bad


def _check_boundaries(spec: Any) -> tuple[int, int]:
    """Check the 65536-character body size boundary in both directions."""
    base = (FIXTURES / "pass/complete.md").read_text(encoding="utf-8")
    pad_65536 = base + ("x" * (MOD.MAX_BODY_CHARS - len(base)))
    probs_ok = MOD.check_body(spec, pad_65536)
    ok_exact = len(pad_65536) == 65536 and not probs_ok
    b1 = not _report("boundary/65536-pass", ok_exact, f"problems={probs_ok!r}")
    pad_65537 = pad_65536 + "x"
    probs_over = MOD.check_body(spec, pad_65537)
    codes_over = frozenset(item.code for item in probs_over)
    ok_over = len(pad_65537) == 65537 and codes_over == frozenset({"oversized-body"})
    b2 = not _report("boundary/65537-oversized", ok_over, f"codes={set(codes_over)!r}")
    return 2, b1 + b2


def _run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Execute attestation.py as a subprocess with a 30-second deadline."""
    # nosemgrep: dangerous-subprocess-use-audit  # Fixed python3 argv.
    return subprocess.run(  # nosec B603  # Fixed python3 argv, no shell or untrusted input.
        [sys.executable, "-I", "-B", str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def _write_cli_events(tmp_dir: Path) -> None:
    """Write the event JSON files that CLI_CASES read from tmp_dir."""
    complete_text = (FIXTURES / "pass/complete.md").read_text(encoding="utf-8")
    contents = {
        "event-pass.json": json.dumps({"pull_request": {"body": complete_text}}),
        "event-null.json": json.dumps({"pull_request": {"body": None}}),
        "event-bad.json": "{not valid json",
        "event-nopr.json": json.dumps({"action": "opened"}),
    }
    for name, text in contents.items():
        (tmp_dir / name).write_text(text, encoding="utf-8")


def _fill_slots(arg: str, slots: dict[str, str]) -> str:
    """Replace the {tpl}, {tmp} and {fx} slots of one CLI_CASES argument."""
    for slot, value in slots.items():
        arg = arg.replace(slot, value)
    return arg


def _check_cli_cases(tmp_dir: Path) -> tuple[int, int]:
    """Exercise the CLI over --event, --body, --annotations and error exits."""
    _write_cli_events(tmp_dir)
    slots = {"{tpl}": str(TEMPLATE), "{tmp}": str(tmp_dir), "{fx}": str(FIXTURES)}
    bad = 0
    for name, argv_slots, want_rc, needle in CLI_CASES:
        proc = _run_cli([_fill_slots(arg, slots) for arg in argv_slots])
        stream = proc.stderr if want_rc == 2 else proc.stdout
        ok = proc.returncode == want_rc and needle in stream
        bad += not _report(
            name,
            ok,
            f"rc={proc.returncode} out={proc.stdout!r} err={proc.stderr!r}",
        )
    return len(CLI_CASES), bad


def main() -> int:
    """Run all attestation completeness tests and exit 1 on any failure."""
    spec = MOD.load_template(TEMPLATE)
    total_cases = 0
    total_bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for count, bad in (
            _check_fixture_inventory(),
            _check_pass_fixtures(spec, tmp_dir),
            _check_fail_fixtures(spec),
            _check_line_separators(spec),
            _check_placeholder_cases(),
            _check_boundaries(spec),
            _check_cli_cases(tmp_dir),
        ):
            total_cases += count
            total_bad += bad
    print(f"cases={total_cases} failed={total_bad}")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
