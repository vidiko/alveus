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
   specifications listed under [Allowed inputs](#allowed-inputs), plus
   measurements you made yourself.
3. **Attest it in every pull request.** The pull request template
   ([.github/pull_request_template.md](.github/pull_request_template.md))
   carries the attestation. A pull request without it is not reviewed.

## Allowed inputs

A contributor may use these sources. Cite the document and the clause, section
or page in the pull request and in the module documentation of the code that
implements it.

| Kind | Examples |
| :--- | :--- |
| Standards bodies | ITU-T Recommendations (H.264, H.265, H.266, H.273), ITU-R Recommendations (BT.601, BT.709, BT.2020), ISO/IEC standards (14496-12, 23009-1) |
| IETF | RFCs (RFC 8794 EBML, RFC 9559 Matroska, RFC 9043 FFV1, RFC 9639 FLAC, RFC 6716 Opus, RFC 3533 Ogg) and Internet-Drafts of the CELLAR working group, read from `rfc-editor.org` or `datatracker.ietf.org` |
| Format and codec specifications | AOMedia AV1 Bitstream and Decoding Process Specification, the Matroska and WebM container documentation, Xiph specifications |
| Hardware and platform APIs | Vendor API references and the public headers that define those APIs (Khronos Vulkan Video, VA-API, vendor video SDKs) |
| Literature | Published papers and textbooks on signal processing, colour science, entropy coding and resampling |
| Own measurements | Results of running programs as black boxes: inputs, outputs, hashes, timings, error behaviour (see [Black-box observation](#black-box-observation)) |
| Conformance material | Published conformance and test streams with their expected results, under their own licences (see [docs/plan/milestones.md](docs/plan/milestones.md)) |
| General references | Dictionaries and encyclopedias, for documentation prose only (for example the origin of the project name); never a source for code or format behaviour |

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
measured.

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
| Spec writer | Public specifications; black-box observation of other programs | Spec notes in their own words: clause references, bit layouts, test vectors, measured behaviour |
| Implementer | Public specifications; spec notes; committed test fixtures | Code and tests that cite the clauses they implement |

The implementer never explores other implementations' behaviour directly.
Their contact with other programs is through fixtures the spec writer or the
test harness committed: inputs, expected outputs and hashes.

The pull request names who held which role.

### Black-box observation

The spec writer may run any program, including the FFmpeg command-line tool,
as a black box: feed it inputs, record outputs, hashes and error behaviour.
The record is a measurement and may be committed as a fixture. Reading the
program's source is not observation and stays forbidden. Whether its help
output and user documentation may supply option names is an
[open question](#open-questions); until it is decided, they may not.

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
- the inputs used, each with document and clause, and that each is an
  allowed input for the role the author held: an implementer lists only
  public specifications, spec notes and committed fixtures, and own
  measurements are spec-writer input only;
- who held the spec-writer and implementer roles for the touched components.

Two defences check it, so no single miss lets contaminated work land:

1. Review: the maintainer rejects a pull request whose attestation is missing,
   incomplete or contradicted by its content.
2. A mechanical check that fails a pull request whose attestation block is
   missing, has an unchecked box, or has an empty or placeholder field. It is
   planned for milestone M0 in
   [docs/plan/milestones.md](docs/plan/milestones.md), and it joins the
   required status checks in
   [.github/rulesets/main.json](.github/rulesets/main.json) when it lands, so
   a pull request cannot merge without passing it. Until then, review is the
   only defence, and the maintainer reads every attestation before merging.

## When contamination happens

If anyone finds that forbidden input reached alveus, whether through their own
work or someone else's:

1. Stop work on the affected component and say so in the pull request or an
   issue. Describe what was read and when, but do not quote or link the
   forbidden material.
2. The maintainer marks the affected files and commits.
3. A contributor who has not seen the material rewrites them from the
   specifications, or the change is reverted.
4. The contaminated contributor or session leaves the component, and the
   incident is recorded in a contamination log that the first incident
   creates under `docs/cleanroom/`.
5. Published history is not rewritten by default. The ruleset forbids force
   pushes to `main`, and existing clones and forks already hold the commits,
   so a rewrite would not remove the material. The contamination log names
   the affected commits, and no later work builds on them. If a case needs
   the material removed from history as well, for example after a takedown
   request, the maintainer decides it in a decision record under
   [docs/adr/](docs/adr/). That record names the rewrite procedure, the
   temporary ruleset change it needs, and the notice sent to known forks.

## Open questions

These are decided before the work that needs them starts, and recorded as
decision records under [docs/adr/](docs/adr/):

- **Normative reference code in specifications.** Some specifications publish
  code as their normative part, for example the Opus reference
  implementation in RFC 6716. Whether a spec writer may read that code, and
  how its licence carries over, is decided before the Opus milestone.
- **Command-line naming.** Whether option names for the command-line
  compatibility levels in
  [docs/plan/scope-matrix.md](docs/plan/scope-matrix.md) may come from FFmpeg's
  published user documentation or help output, or only from observed
  behaviour, is decided before compatibility level L1 starts. Until then,
  neither documentation nor help output is an input.
