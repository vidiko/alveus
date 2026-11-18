---
description: Clean-room media framework in Rust from public specifications.
---

# alveus

alveus is a planned media framework in Rust: containers, codecs, filters and
a command-line tool, written clean-room from public specifications
([CLEANROOM.md](../CLEANROOM.md)).

**Status: planning.** There is no framework code yet. The project plan is in
[plan/README.md](plan/README.md). Milestone M0 sets up the workspace and the
gates, and the first media milestone, M1, is Matroska demuxing with FFV1
decoding ([plan/milestones.md](plan/milestones.md)).

## The name

*alveus* is a Latin noun meaning a hollow or cavity, and from that a trough,
the hull of a ship, and the bed or channel of a river. It derives from Latin
*alvus*, "belly". English keeps the word as a rare legal term for a river's
bed or channel (source:
[Wiktionary, "alveus"](https://en.wiktionary.org/wiki/alveus)).

The river-channel sense fits a framework that streams flow through.

Pronunciation:

- Classical Latin: **AL-weh-us**, with the last vowel as in English *put*;
  IPA [ˈaɫ.we.ʊs].
- English: **AL-vee-us**, IPA /ˈæl.vi.əs/.

The project writes the name in lower case: alveus.

## Clean room

alveus contains no code read, copied or translated from FFmpeg, libav or
anything derived from them ([CLEANROOM.md](../CLEANROOM.md)). Contributors work
from public specifications, while spec writers record black-box measurements
that implementers receive only as spec notes and committed fixtures
([CLEANROOM.md](../CLEANROOM.md#roles)). Every pull request attests compliance
under the rules, role split and provenance checks defined in
[CLEANROOM.md](../CLEANROOM.md#attestation).

## Where to go next

| Page | What it covers |
| :--- | :--- |
| [Project plan](plan/README.md) | Overview of the planning directory and the pages still to be written. |
| [Milestone ladder](plan/milestones.md) | Milestones M0 through M7, their dependencies, test material and exit criteria. |
| [Scope matrix](plan/scope-matrix.md) | Planned containers, codecs, filters, protocols, hardware APIs and CLI compatibility levels. |
| [Crate architecture](plan/architecture.md) | Planned Cargo workspace crates, stage traits, HISS invariants and dependency checks. |
| [Architectural Decision Records](adr/README.md) | Append-only decision records for the first slice, CLI option observation and normative reference code. |

## Contributing

Before writing any code, spec notes or fixtures, read
[CLEANROOM.md](../CLEANROOM.md) for the allowed inputs and role separation, and
[CONTRIBUTING.md](../CONTRIBUTING.md) for the High-Integrity Systems Standard
(HISS) rules, testing discipline, commit format and local verification gate.
