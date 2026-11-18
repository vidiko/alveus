# ADR-0003: Normative reference code in specifications

- **Status**: Accepted
- **Date**: 2026-11-18
- **Authors**: alveus maintainers

## Context

[CLEANROOM.md](../../CLEANROOM.md#allowed-inputs) allows both roles to read
published standards-body and IETF specifications, while
[CLEANROOM.md](../../CLEANROOM.md#forbidden-inputs) forbids reading the source
of other media implementations. Some specifications publish source code as part
of their normative definition rather than prose alone. In particular, RFC 6716
(the Opus audio codec, scheduled for milestone M5 in
[docs/plan/milestones.md](../plan/milestones.md)) publishes a C reference
implementation as a normative part of the RFC.

Before M5 can start, alveus must settle two questions: which role, if any, may
read normative reference code published inside a specification, and whether
reading that code or using test vectors from the specification carries a
licence into alveus.

Options considered:

| Option | Who may read normative reference code | Assessment |
| :--- | :--- | :--- |
| Nobody reads it | Neither spec writer nor implementer | Blocks any codec whose specification defines normative behaviour in reference code, including Opus in RFC 6716 ([docs/plan/milestones.md](../plan/milestones.md)), wherever the prose alone leaves normative details unspecified. |
| Spec writer only | Spec writer reads it as part of the specification and writes spec notes in own words; implementer never reads it | Keeps the clean-room barrier in [CLEANROOM.md](../../CLEANROOM.md#roles): the implementer never sees the C source, and no reference code enters alveus, while the spec writer can still capture every normative requirement. |
| Both roles | Spec writer and implementer both read the reference code directly | Exposes the implementer to a concrete C implementation while writing Rust code, risking direct translation of control flow, function splits, identifiers and data layouts, and raising code-licence carry-over questions. |

## Decision

When a specification publishes code as its normative part (for example the Opus
reference implementation in RFC 6716), only the spec writer reads that code, as
part of the specification
([CLEANROOM.md](../../CLEANROOM.md#allowed-inputs)). The spec writer writes
spec notes in their own words that describe the behaviour and cite the RFC
section or specification clause they describe. The implementer never reads the
normative reference code ([CLEANROOM.md](../../CLEANROOM.md#roles)).

Review under [CLEANROOM.md](../../CLEANROOM.md#attestation) checks the spec
notes for transliteration of the C structure (control flow, function split,
naming, or data layout copied from the code instead of described by
behaviour) and rejects pull requests whose spec notes transliterate it.

Because only the spec writer reads the normative reference code and writes spec
notes in their own words, no normative reference code enters alveus, and no
code licence carries over. Test vectors or other files taken from a
specification are fixtures and follow the licence-first rule for conformance
material ([CLEANROOM.md](../../CLEANROOM.md#allowed-inputs), as applied to
the M1 test material in [docs/plan/milestones.md](../plan/milestones.md)):
their licence is confirmed and recorded before use, and each committed file
carries a REUSE notice in [REUSE.toml](../../REUSE.toml) or a companion
`.license` file.

## Consequences

- **Positive**: Milestone M5 in
  [docs/plan/milestones.md](../plan/milestones.md) is unblocked while keeping
  the implementer insulated from C source code. No reference-implementation
  code licence carries over into alveus crates or spec notes, and any
  specification test vectors committed as fixtures carry explicit per-file
  REUSE metadata that `reuse lint` checks.
- **Negative**: Preparing and reviewing spec notes for specifications with
  normative reference code requires extra care: the spec writer must restate
  algorithms by behaviour rather than C structure, and maintainer review
  ([CLEANROOM.md](../../CLEANROOM.md#attestation)) must verify that the spec
  notes do not transliterate control flow, function splits, names or data
  layouts.

**Revisit when** review finds that a normative algorithm cannot be described
by behaviour without reproducing the reference code's structure, or when a
specification's own terms restrict reading the code it publishes.
