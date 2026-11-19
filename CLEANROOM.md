<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# Clean-room policy

alveus is written from public specifications and its own measurements. It
contains no code that was read, copied or translated from FFmpeg, libav, or
anything derived from them. This file states the rules that keep it that way,
who may contribute to what, and what happens when a rule is broken.

This policy is a project rule, not legal advice.

## The short version

If you only read one section, read this one. Every contribution follows these
three rules:

1. **Never read FFmpeg or libav source, or source derived from it.** That
   includes forks, patch sets, ports, translations, bindings, and the
   documentation that lives in their source trees.
2. **Work from public specifications.** ITU-T Recommendations, ISO/IEC
   standards, IETF RFCs and Internet-Drafts, and the other published
   specifications listed under [Allowed inputs](#allowed-inputs). Spec
   writers may add measurements made by running programs as black boxes;
   implementers receive those only as spec notes and committed fixtures
   (see [Roles](#roles)).
3. **Attest it in every pull request.** The pull request template
   ([.github/pull_request_template.md](.github/pull_request_template.md))
   carries the attestation. A pull request without it is not reviewed.

## Allowed inputs

A contributor may use the sources that the last column marks for the role
they hold (see [Roles](#roles)). Cite the document and the clause, section
or page in the pull request and in the module documentation of the code that
implements it.

| Kind | Examples | Used by |
| :--- | :--- | :--- |
| Standards bodies | ITU-T Recommendations (H.264, H.265, H.266, H.273), ITU-R Recommendations (BT.601, BT.709, BT.2020), ISO/IEC standards (14496-12, 23009-1); specification text only, not code published as a normative part | Both roles |
| IETF | RFCs (RFC 8794 EBML, RFC 9559 Matroska, RFC 9043 FFV1, RFC 9639 FLAC, RFC 6716 Opus, RFC 3533 Ogg) and Internet-Drafts of the CELLAR working group, read from `rfc-editor.org` or `datatracker.ietf.org`; specification text only, not code published as a normative part | Both roles |
| Format and codec specifications | AOMedia AV1 Bitstream and Decoding Process Specification, the Matroska and WebM container documentation, Xiph specifications; specification text only, not code published as a normative part | Both roles |
| Normative reference code in specifications | Code published inside a specification as part of its normative definition (for example the Opus reference implementation in RFC 6716; see [ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)) | Spec writer only |
| Hardware and platform APIs | Vendor API references and the public headers that define those APIs (Khronos Vulkan Video, VA-API, vendor video SDKs) | Both roles |
| Literature | Published papers and textbooks on signal processing, colour science, entropy coding and resampling | Both roles |
| Own measurements | Results of running programs as black boxes: inputs, outputs, hashes, timings, error behaviour, help output (see [Black-box observation](#black-box-observation) and [ADR-0002](docs/adr/0002-command-line-names-from-observation.md)) | Spec writer only |
| Conformance material | Published conformance and test streams with their expected results, and test vectors taken from a specification. Licence first: before a file is used, its licence is recorded and confirmed to permit committing and redistributing the file with alveus under conditions the project meets, and each committed file carries a REUSE notice in [REUSE.toml](REUSE.toml) or a `.license` file (see [docs/plan/milestones.md](docs/plan/milestones.md#m1-matroska-demux-and-ffv1-decode-bit-exact) and [ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)) | Both roles |
| General references | Dictionaries and encyclopedias, for documentation prose only (for example the origin of the project name); never a source for code or format behaviour | Both roles |

Where a specification is mirrored in a repository that also holds FFmpeg or
libav code, read the published copy from the standards body instead. For FFV1
that means RFC 9043 from the RFC Editor, not a repository copy.

## Forbidden inputs

No contributor reads, copies, translates or paraphrases these, for any part
of alveus, code or documentation:

- FFmpeg and libav source code, including headers, build files, tests, and the
  documentation kept in their source trees.
- Anything derived from that source: forks, downstream patch sets, products
  that embed it, mailing-list patches, commit diffs, bug-tracker attachments,
  and wiki or forum posts that quote it.
- Ports and translations of it into other languages, and bindings to it
  (for example Rust `*-sys` crates generated from its headers).

Reading the source of other media implementations is not an input either.
Other implementations may serve alveus in two ways only: as a dependency after
a licence and provenance review, or as a black box whose behaviour is
measured. The one exception is code that a specification publishes as its
normative part, such as the Opus reference implementation in RFC 6716: the
spec writer, and no one else, reads it as part of that specification (see
[Allowed inputs](#allowed-inputs) and
[ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)). The
exception never covers FFmpeg or libav source.

## C ports: behaviour reference only

Some Rust media crates are ports of C code bases. rav1d, a Rust port of the
dav1d AV1 decoder, is the reference case. alveus treats every such port as
follows:

- It is excluded as code prior art. No contributor reads its source to write
  alveus code, and no alveus design cites its internals.
- It may be listed and used for behaviour only: run it as a black box, record
  its outputs, and compare alveus against them in tests.

The same holds for any code base that was machine-translated or hand-ported
from another language.

## Roles

Two roles keep observation and implementation apart. For any one component (a
container, a codec, a filter), the person or agent session that writes the
spec notes is not the one that writes the implementation.

| Role | May use | Produces |
| :--- | :--- | :--- |
| Spec writer | Every row of [Allowed inputs](#allowed-inputs), including normative reference code in specifications and black-box observation of other programs | Spec notes in their own words: clause and RFC section references, bit layouts, test vectors, measured behaviour, and behaviour of normative reference code described without transliterating its structure |
| Implementer | The rows of [Allowed inputs](#allowed-inputs) marked for both roles (specification text, API references, literature, conformance material), never normative reference code; spec notes; committed test fixtures | Code and tests that cite the clauses they implement |

The implementer never explores other implementations' behaviour directly, and
never reads normative reference code published inside a specification
([ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)).
Their contact with other programs is through fixtures the spec writer or the
test harness committed: inputs, expected outputs and hashes. Where a
specification publishes code as its normative part, only the spec writer reads
that code, describes it by behaviour in their own words, cites the RFC section
or specification clause, and never transliterates its C structure (control
flow, function split, naming or data layout). Because no normative reference
code enters alveus, no code licence carries over from it
([ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)).

The pull request names who held which role.

### Black-box observation

The spec writer may run any program, including the FFmpeg command-line tool,
as a black box: feed it inputs, record outputs, hashes and error behaviour.
The record is a measurement and may be committed as a fixture. Reading the
program's source is not observation and stays forbidden. What the program
prints when run, including its help output, counts as an observation that
only the spec writer records, as a measurement
([ADR-0002](docs/adr/0002-command-line-names-from-observation.md)). User
documentation and man pages live in the source tree and are not allowed
inputs. Command-line option names for the compatibility levels in
[docs/plan/scope-matrix.md](docs/plan/scope-matrix.md) reach the implementer
only through spec notes and the fixtures the spec writer commits, such as the
command-line corpus of level L2.

### Agent sessions and lanes

An AI agent session or model lane that has read FFmpeg or libav source, or
source derived from it, in any project, never writes alveus code, spec notes,
test fixtures or plan text. Only a fresh session, or a fresh lane whose brief
covers alveus alone, may.
A brief for such a lane carries no memory, notes or state from contaminated
work.

### Human contributors

A human contributor who has read FFmpeg or libav source for the component a
pull request touches writes neither code, spec notes nor test fixtures for
that component, because spec notes and fixtures reach the implementer as
inputs. Any other past exposure is disclosed in the attestation, and the
reviewer decides whether the contributor works on the component at all, and
in which role.

## Attestation

Every pull request carries the attestation block from
[.github/pull_request_template.md](.github/pull_request_template.md). It
states:

- that the author did not read, copy or translate forbidden inputs while
  preparing the change;
- the inputs used, each with document and clause, and that the last column
  of [Allowed inputs](#allowed-inputs) marks each for the role the author
  held: an implementer uses only the rows marked for both roles, and
  reaches other programs' behaviour only through spec notes and committed
  fixtures;
- who held the spec-writer and implementer roles for the touched components.

Three checks cover it, and each catches a different failure:

1. Review: the maintainer rejects a pull request whose attestation is missing,
   incomplete or contradicted by its content, for example code whose
   behaviour no cited clause describes, or spec notes that transliterate the
   structure of normative reference code (control flow, function split,
   naming or data layout) instead of describing its behaviour
   ([ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)).
2. The attestation check: a mechanical check that fails a pull request whose
   attestation block is missing, has an unchecked box, or has an empty or
   placeholder field. An answer is an item of a bullet list (`-`, `*` or `+`)
   under the field label; text outside such a list, numbered lists and quoted
   lists do not count, and HTML comments are ignored. It checks that the
   attestation is complete, not that it is true.
3. The provenance scan: a licence and copyright scanner run over every
   changed file, which fails on a notice that names FFmpeg, libav or another
   forbidden source. It catches copied code that kept its notices.

Check 2 runs as the `Clean-room attestation` job of
[.github/workflows/cleanroom.yml](.github/workflows/cleanroom.yml)
([tools/cleanroom/attestation.py](tools/cleanroom/attestation.py), fixtures
under
[tools/cleanroom/fixtures/attestation/](tools/cleanroom/fixtures/attestation/))
and reruns whenever a pull request's description is edited, reading the current
description through the API on each run so a rerun checks the description as it
stands.
[.github/rulesets/main.json](.github/rulesets/main.json) lists it among the
required status checks, and the ruleset on the forge takes the same list once
planted pull requests have shown the check fails there (criterion 2 of
milestone M0 in [docs/plan/milestones.md](docs/plan/milestones.md)). Check 3
is planned for milestone M0 and joins the required status checks when it
lands, so a pull request cannot merge without passing both checks. Until then,
only the maintainer has write access to the repository, so every merge passes
through the maintainer's review, and no other contributor gets write access
before both checks are required.

The ruleset lets the repository admin role bypass it when merging a pull
request, because the repository has a single maintainer and requires no
approvals. That bypass is never used to merge a pull request whose
clean-room check has failed or has not finished. The forge records every
bypass, and the maintainer reads that record when each milestone closes
(`GET /repos/{owner}/{repo}/rulesets/rule-suites` with
`rule_suite_result=bypass`). A pull request found merged through the bypass
without a passing clean-room check is reviewed again, and handled as
contamination (below) if its attestation does not hold.

No check proves that a complete attestation is true. A missing or incomplete
attestation meets two checks (1 and 2), and so does copied code that kept its
notices (1 and 3). Code that was translated, or copied with its notices
removed, under a complete but false attestation meets review alone. The
policy therefore relies on contributors attesting truthfully, and a false
attestation found after merging is handled as contamination (below).

## When contamination happens

If anyone finds that forbidden input reached alveus, whether through their own
work or someone else's:

1. Stop work on the affected component and say so in the pull request or an
   issue. Describe what was read and when, but do not quote or link the
   forbidden material.
2. The maintainer pauses merges that touch the affected component and
   checks every open pull request. One whose branch contains the affected
   commits, or that changes the affected files, is closed or rebased onto a
   clean base before further work on the component is merged.
3. The maintainer marks the affected files and commits.
4. A contributor who has not seen the material rewrites them from the
   specifications, or the change is reverted.
5. The contaminated contributor or session leaves the component, and the
   incident is recorded in a contamination log that the first incident
   creates under `docs/cleanroom/`.
6. Published history is not rewritten by default. The ruleset forbids force
   pushes to `main`, and existing clones and forks already hold the commits,
   so a rewrite would not remove the material. The contamination log names
   the affected commits, and no later work builds on them. If a case needs
   the material removed from history as well, for example after a takedown
   request, the maintainer decides it in a decision record under
   [docs/adr/](docs/adr/). That record names the rewrite procedure, the
   temporary ruleset change it needs, and the notice sent to known forks.

## Decided questions

Questions that were open when this policy was drafted are recorded as decision
records under [docs/adr/](docs/adr/):

- Command-line option names come from black-box observation, help output
  included ([ADR-0002](docs/adr/0002-command-line-names-from-observation.md)).
- Normative reference code in specifications is read by the spec writer only,
  and carries no code licence into alveus
  ([ADR-0003](docs/adr/0003-normative-reference-code-in-specifications.md)).
