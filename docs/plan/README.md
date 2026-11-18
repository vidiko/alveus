# Project plan

This directory holds the plan for alveus: what it will support, how the code
is organised, and in which order the work happens. alveus is in the planning
stage; no framework code exists yet.

Start with the milestone ladder if you want to know what comes next, or with
the scope matrix if you want to know whether a format is planned.

| Page | Answers |
| :--- | :--- |
| [milestones.md](milestones.md) | What is built in which order, and how each step is checked. |
| [scope-matrix.md](scope-matrix.md) | Which containers, codecs, filters, protocols and hardware APIs are planned, from which specification, at which tier; how far command-line compatibility goes. |
| [architecture.md](architecture.md) | How the Cargo workspace is split into crates, the interfaces between them, and the rules every crate follows. |

All work follows the clean-room policy in [CLEANROOM.md](../../CLEANROOM.md).

## Pages still to write

These pages complete the plan. Each is written in its own pull request, by a
contributor who meets [CLEANROOM.md](../../CLEANROOM.md):

- **Prior-art survey.** Existing Rust media crates with their licence,
  maturity and provenance, and which of them alveus may depend on or measure
  against. Ports of C code bases are listed for behaviour only.
- **Testing.** The conformance manifest format, where each stream set comes
  from and under which licence, fuzzing budgets, and the black-box tools named
  in the milestone exit criteria.
- **Quality-measurement interface.** The frame interface the first consumer
  in milestone M4 reads.

## Changing the plan

A change to the plan is a pull request that edits these pages. Moving a row
of the scope matrix to tier X, or changing the order of milestones, also
needs a decision record under [docs/adr/](../adr/).
