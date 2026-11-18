<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# alveus

alveus is a planned media framework in Rust: containers, codecs, filters and
a command-line tool, written clean-room from public specifications.

**Status: planning.** There is no framework code yet. The plan is in
[docs/plan/](docs/plan/README.md). Milestone M0 sets up the workspace and
the gates, and the first media milestone, M1, is Matroska demuxing with FFV1
decoding ([milestones](docs/plan/milestones.md)).

## The name

*alveus* is a Latin noun meaning a hollow or cavity, and from that a trough,
the hull of a ship, and the bed or channel of a river. It derives from Latin
*alvus*, "belly". English keeps the word as a rare legal term for a river's
bed or channel. Source:
[Wiktionary, "alveus"](https://en.wiktionary.org/wiki/alveus).

The river-channel sense fits a framework that streams flow through.

Pronunciation:

- Classical Latin: **AL-weh-us**, with the last vowel as in English *put*;
  IPA [ˈaɫ.we.ʊs].
- English: **AL-vee-us**, IPA /ˈæl.vi.əs/.

The project writes the name in lower case: alveus.

## Clean room

alveus contains no code read, copied or translated from FFmpeg, libav or
anything derived from them. Contributors work from public specifications.
Spec writers add measurements made by running programs as black boxes, and
implementers receive those only as spec notes and committed fixtures. Every
pull request attests this.
[CLEANROOM.md](CLEANROOM.md) holds the rules, the roles and the attestation.

## Contributing

1. Read [CLEANROOM.md](CLEANROOM.md). It decides what you may read before you
   write anything.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the repository standard, commit
   format and test discipline.
3. Run the repository gate before opening a pull request:

   ```bash
   make verify-all
   ```

4. Fill in the clean-room attestation in the pull request template.

## Licence

alveus is licensed under the European Union Public Licence 1.2
([LICENSE](LICENSE)). Licence and copyright information for every file
follows the [REUSE](https://reuse.software) specification; `reuse lint`
checks it.

<!-- praetor:readme-governance:start -->
[![HISS Adopted][praetor-hiss-badge]][praetor-hiss-agents]

Praetor manages this repository's declared governance policy. This managed
block records adoption state; it is not a verification certificate.

**Verification**: `make verify-all` runs the repository's configured
verification cascade.

**HISS Audit**: `praetorctl audit` enforces policy, generated-surface
integrity, and the debt ratchet.

**Context Sync**: `praetorctl compile-context --verify` verifies every
generated agent context against `AGENTS.md`.

**Debt Baseline**: `.standards-baseline.json` anchors the debt ratchet at
0 recorded infractions; audit forbids growth.

[praetor-hiss-badge]: https://img.shields.io/badge/Standards-HISS%20Adopted-blue
[praetor-hiss-agents]: https://github.com/vidiko/alveus/blob/HEAD/AGENTS.md
<!-- praetor:readme-governance:end -->
