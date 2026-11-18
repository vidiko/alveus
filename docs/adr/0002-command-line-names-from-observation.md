# ADR-0002: Command-line option names come from black-box observation

- **Status**: Accepted
- **Date**: 2026-11-18
- **Authors**: alveus maintainers

## Context

The command-line compatibility levels in
[docs/plan/scope-matrix.md](../plan/scope-matrix.md) grade how much of an
existing command carries over to `alveus-cli`
([docs/plan/architecture.md](../plan/architecture.md)). Level L0 uses alveus's
own grammar, while level L1 accepts a listed subset of common FFmpeg-style
options as aliases and level L2 checks a corpus of real command lines by
black-box comparison.

To specify and implement levels L1 and L2, alveus needs an allowed source for
those option names. [CLEANROOM.md](../../CLEANROOM.md#forbidden-inputs) forbids
reading files in the FFmpeg or libav source trees, including the user
documentation and man pages kept there, while
[CLEANROOM.md](../../CLEANROOM.md#black-box-observation) allows the spec writer
to run the FFmpeg command-line tool as a black box and record what it outputs.

Options considered:

| Option | Allowed sources | Assessment |
| :--- | :--- | :--- |
| Documentation and help output allowed | Published user documentation, man pages, and black-box runs (including help output) | Weakens [CLEANROOM.md](../../CLEANROOM.md#forbidden-inputs): the user documentation and man pages live in the FFmpeg source tree and are already forbidden. |
| Help output only (black-box observation) | Black-box runs of the FFmpeg command-line tool, including what it prints as help output | Treats help output like any other program output observed by the spec writer, while keeping source-tree documentation and man pages out of the allowed inputs. |
| Observed behaviour only | Black-box runs of media conversions, excluding help output | Leaves the spec writer without a measured list of the option names the tool accepts. Each name would have to be known before it can be tried, and no allowed input supplies it. |

## Decision

Command-line option names for the FFmpeg-compatibility levels in
[docs/plan/scope-matrix.md](../plan/scope-matrix.md) come only from black-box
runs of the FFmpeg command-line tool
([CLEANROOM.md](../../CLEANROOM.md#black-box-observation)). Its help output
(what the program prints when run) counts as an observation, so only the spec
writer runs the tool and records the observed option names and behaviour in
spec notes, in their own words, as a measurement
([CLEANROOM.md](../../CLEANROOM.md#roles)). The implementer receives option
names only through those spec notes and the fixtures the spec writer commits,
such as the command-line corpus of level L2, as for any other observed
behaviour ([CLEANROOM.md](../../CLEANROOM.md#black-box-observation)).
FFmpeg's user documentation and man pages stay out of the allowed inputs
([CLEANROOM.md](../../CLEANROOM.md#forbidden-inputs)), because they live in its
source tree.

## Consequences

- **Positive**: Compatibility level L1 in
  [docs/plan/scope-matrix.md](../plan/scope-matrix.md) is unblocked without
  creating an exception to the ban on source-tree files in
  [CLEANROOM.md](../../CLEANROOM.md#forbidden-inputs). The role boundary in
  [CLEANROOM.md](../../CLEANROOM.md#roles) stays uniform across codec
  behaviour and command-line compatibility: the spec writer observes and writes
  spec notes, and the implementer works from spec notes and committed fixtures.
- **Negative**: Every alias in compatibility levels L1 and L2 must be observed
  and written up in spec notes by a spec writer before an implementer adds it
  to `alveus-cli`. The spec writer describes the observed options in their own
  words rather than copying help prose.

**Revisit when** a compatibility level in
[docs/plan/scope-matrix.md](../plan/scope-matrix.md) requires option details
that black-box observation cannot measure, or when the role split in
[CLEANROOM.md](../../CLEANROOM.md#roles) changes.
