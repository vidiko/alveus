<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->
<!-- markdownlint-disable MD013 MD033 MD041 -->

<div align="center">

  <img src="docs/assets/alveus-readme-banner.svg" alt="alveus: clean-room media framework in Rust" height="120" />

  <!-- README-STANDARD badge block: one group, fixed order -->
  <!-- 1 release/version -->
  [![Release](https://img.shields.io/static/v1?label=release&message=none%20yet%20%C2%B7%20planning&style=for-the-badge&color=6e7781&labelColor=111a35)](docs/plan/milestones.md)
  <!-- 2 CI/build -->
  [![Verification gate](https://img.shields.io/github/actions/workflow/status/vidiko/alveus/ci.yml?branch=main&event=push&style=for-the-badge&labelColor=111a35&label=Verification%20gate)](https://github.com/vidiko/alveus/actions/workflows/ci.yml)
  [![REUSE](https://img.shields.io/github/actions/workflow/status/vidiko/alveus/reuse.yml?branch=main&event=push&style=for-the-badge&labelColor=111a35&label=REUSE)](https://github.com/vidiko/alveus/actions/workflows/reuse.yml)
  [![Docs](https://img.shields.io/github/actions/workflow/status/vidiko/alveus/pages.yml?branch=main&event=push&style=for-the-badge&labelColor=111a35&label=Docs)](https://github.com/vidiko/alveus/actions/workflows/pages.yml)
  <!-- 3 security/scorecard -->
  [![Security policy](https://img.shields.io/badge/Security-Policy-3b82f6?style=for-the-badge&labelColor=111a35)](SECURITY.md)
  [![CodeRabbit](https://img.shields.io/badge/Reviews-CodeRabbit-8b5cf6?style=for-the-badge&logo=coderabbit&logoColor=white&labelColor=111a35)](https://coderabbit.ai)
  [![Copilot](https://img.shields.io/badge/Reviews-Copilot-8b5cf6?style=for-the-badge&logo=githubcopilot&logoColor=white&labelColor=111a35)](.github/rulesets/main.json)
  <!-- 4 standards -->
  [![HISS-21](https://img.shields.io/badge/Standards-HISS--21-06b6d4?style=for-the-badge&logo=nasa&labelColor=111a35)](AGENTS.md)
  [![Clean room](https://img.shields.io/badge/Clean_room-Policy-06b6d4?style=for-the-badge&labelColor=111a35)](CLEANROOM.md)
  [![Conventional Commits](https://img.shields.io/badge/Commits-Conventional-8b5cf6?style=for-the-badge&logo=conventionalcommits&logoColor=white&labelColor=111a35)](CONTRIBUTING.md)
  <!-- 5 licence -->
  [![License](https://img.shields.io/badge/License-EUPL--1.2-3b82f6?style=for-the-badge&labelColor=111a35)](LICENSE)
  <!-- 6 support -->
  [![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-8b5cf6?style=for-the-badge&logo=githubsponsors&logoColor=white&labelColor=111a35)](https://github.com/sponsors/lusoris)
  [![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-8b5cf6?style=for-the-badge&logo=kofi&logoColor=white&labelColor=111a35)](https://ko-fi.com/lusoris)

  **Clean-room media framework in Rust, written from public specifications.**

  *Planning stage: no framework code exists yet; milestone M0 sets up the
  workspace and gates, and M1 starts Matroska demuxing with FFV1 decoding.*

</div>

alveus is a planned media framework in Rust: containers, codecs, filters and
a command-line tool, written clean-room from public specifications
([CLEANROOM.md](CLEANROOM.md)). **Status: planning.** There is no framework
code yet. The plan is in [docs/plan/](docs/plan/README.md). Milestone M0 sets
up the workspace and the gates, and the first media milestone, M1, is Matroska
demuxing with FFV1 decoding ([milestones](docs/plan/milestones.md)).

*alveus* (written in lower case: alveus) is a Latin noun meaning a hollow or
cavity, and from that a trough, the hull of a ship, and the bed or channel of
a river — a river-channel sense that fits a framework that streams flow
through. It derives from Latin *alvus*, "belly", and English keeps the word as
a rare legal term for a river's bed or channel (source:
[Wiktionary, "alveus"](https://en.wiktionary.org/wiki/alveus)). Pronunciation
is **AL-weh-us** (with the last vowel as in English *put*; IPA [ˈaɫ.we.ʊs]) in
Classical Latin and **AL-vee-us** (IPA /ˈæl.vi.əs/) in English.

**[📖 Documentation](https://vidiko.github.io/alveus/)** · [Documentation source](docs/)

---

## 🎯 Why alveus

alveus sets out to build a media framework around explicit provenance, modular
crates and verifiable conformance ([docs/plan/README.md](docs/plan/README.md)).

| Aspect | How alveus handles it |
| :--- | :--- |
| Clean-room provenance | Contributors work from public specifications and from black-box measurements that a separate spec writer records, with an attestation on every pull request ([CLEANROOM.md](CLEANROOM.md)). |
| One crate per component | The planned Cargo workspace gives each container, codec and shared concern its own `alveus-<name>` crate so callers link only what they need ([docs/plan/architecture.md](docs/plan/architecture.md)). |
| Verifiable exit criteria | Media milestones close on an exact oracle (bit-exact frames, a conformance stream set or a stored checksum) and on fuzz targets that run for one CPU hour without a crash or hang ([docs/plan/milestones.md](docs/plan/milestones.md)). |
| High-integrity Rust | All planned code follows the HISS-21 rules: no recursion, bounded loops, explicit I/O deadlines, no allocation in hot loops, typed errors, and `unsafe` only in SIMD modules and the C interface, each block with a `// SAFETY:` proof ([AGENTS.md](AGENTS.md), [docs/plan/architecture.md](docs/plan/architecture.md)). |
| Licensing and REUSE | The repository is licensed under EUPL-1.2 ([LICENSE](LICENSE)), with per-file copyright and licence metadata checked by `reuse lint` ([REUSE.toml](REUSE.toml)). |

## 🚀 Get started

There is nothing to install yet because alveus is in the planning stage and has
no framework crates ([docs/plan/README.md](docs/plan/README.md)). To explore
the plan and verify the repository locally:

1. Read the [milestone ladder](docs/plan/milestones.md) and the
   [scope matrix](docs/plan/scope-matrix.md) to see what is planned and in
   which order.
2. Clone the repository and run the repository gate ([Makefile](Makefile)):

   ```bash
   git clone https://github.com/vidiko/alveus.git
   cd alveus
   make verify-all
   ```

## 🧩 At a glance

A planned conversion runs through five stages between a byte source and a byte
sink, or copies packets directly from demuxer to muxer
([docs/plan/architecture.md](docs/plan/architecture.md)).

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif', 'fontSize': '15px', 'primaryColor': '#111a35', 'primaryTextColor': '#e2e8f0', 'primaryBorderColor': '#3b82f6', 'lineColor': '#3b82f6', 'edgeLabelBackground': '#111a35', 'tertiaryColor': '#0b1020'}}}%%
flowchart TD
  classDef input fill:#0b1020,stroke:#06b6d4,stroke-width:2px,color:#e2e8f0
  classDef step fill:#111a35,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0
  classDef decide fill:#111a35,stroke:#8b5cf6,stroke-width:2px,color:#e2e8f0

  src["Byte source"]:::input
  demux["Demuxer"]:::step
  dec["Decoder"]:::step
  filt["Filters"]:::step
  enc["Encoder"]:::step
  mux["Muxer"]:::step
  sink["Byte sink"]:::input

  src -->|bytes| demux
  demux -->|packets| dec
  dec -->|frames| filt
  filt -->|frames| enc
  enc -->|packets| mux
  mux -->|bytes| sink
  demux -.->|"packets (copy)"| mux
```

See [docs/plan/architecture.md](docs/plan/architecture.md) for the planned
crate table and trait interfaces.

## 📚 Guides and reference

| Page | What it answers |
| :--- | :--- |
| [Documentation site](https://vidiko.github.io/alveus/) | Published overview, project plan and architectural decision records ([mkdocs.yml](mkdocs.yml)). |
| [docs/plan/README.md](docs/plan/README.md) | How the project plan is organised and which plan pages are still to be written. |
| [docs/plan/milestones.md](docs/plan/milestones.md) | What is built in which order from M0 to M7, and the exit criteria that gate each milestone. |
| [docs/plan/scope-matrix.md](docs/plan/scope-matrix.md) | Which containers, codecs, filters, protocols and hardware APIs are planned, from which specification and at which tier. |
| [docs/plan/architecture.md](docs/plan/architecture.md) | How the Cargo workspace is split into crates, the traits between stages, and the HISS rules every crate follows. |
| [docs/adr/README.md](docs/adr/README.md) | Index of append-only Architectural Decision Records covering the first vertical slice, CLI observation and normative reference code. |
| [CLEANROOM.md](CLEANROOM.md) | Allowed and forbidden inputs, the spec-writer and implementer role split, pull-request attestation and contamination handling. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | High-Integrity Systems Standard (HISS) rules, 3D testing discipline, Conventional Commits and local verification. |
| [SECURITY.md](SECURITY.md) | Supported versions and how to report a vulnerability privately. |

## 🤝 Contribute

1. Read [CLEANROOM.md](CLEANROOM.md). It decides what you may read before you
   write anything.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the repository standard, commit
   format and test discipline.
3. Run the repository gate before opening a pull request:

   ```bash
   make verify-all
   ```

4. Fill in the clean-room attestation in the pull request template.

## 💖 Support

- **Security vulnerabilities**: report privately under
  [SECURITY.md](SECURITY.md) rather than opening a public issue.
- **Questions and bugs**: open an issue on
  [GitHub Issues](https://github.com/vidiko/alveus/issues).
- **Sponsorship**: support the project in any amount through
  [GitHub Sponsors](https://github.com/sponsors/lusoris) or
  [Ko-fi](https://ko-fi.com/lusoris); no support contract or issue priority is
  sold.

## 📈 Roadmap and releases

The milestone ladder builds one vertical slice at a time
([docs/plan/milestones.md](docs/plan/milestones.md)):

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'ui-sans-serif, Segoe UI, Helvetica, Arial, sans-serif', 'fontSize': '15px', 'primaryColor': '#111a35', 'primaryTextColor': '#e2e8f0', 'primaryBorderColor': '#3b82f6', 'lineColor': '#3b82f6', 'edgeLabelBackground': '#111a35', 'tertiaryColor': '#0b1020'}}}%%
flowchart TD
  classDef input fill:#0b1020,stroke:#06b6d4,stroke-width:2px,color:#e2e8f0
  classDef step fill:#111a35,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0
  classDef decide fill:#111a35,stroke:#8b5cf6,stroke-width:2px,color:#e2e8f0

  M0["M0 Workspace, gates, clean room"]:::input
  M1["M1 Matroska demux & FFV1 decode"]:::step
  M2["M2 FFV1 encode & Matroska mux"]:::step
  M3["M3 FLAC decode (FLAC & Matroska)"]:::step
  M4["M4 Pipeline, CLI L0 & raw frames"]:::step
  M5["M5 Ogg demux and Opus decode"]:::step
  M6["M6 AV1 decode (Argon Streams)"]:::step
  M7["M7 ISO base media format demux"]:::step

  M0 --> M1
  M1 --> M2
  M1 --> M3
  M2 --> M4
  M3 --> M4
  M4 --> M5
  M4 --> M6
  M6 --> M7
```

- Milestone scope, test material and exit criteria:
  [docs/plan/milestones.md](docs/plan/milestones.md).
- Issue tracking by milestone:
  [GitHub milestones](https://github.com/vidiko/alveus/milestones).
- No releases yet.

## Upstream and licence

alveus has no upstream code base: it is written clean-room from public
specifications under [CLEANROOM.md](CLEANROOM.md). For milestones M1 to M7
the [scope matrix](docs/plan/scope-matrix.md) names RFC 8794 (EBML), RFC 9559
(Matroska), RFC 9043 (FFV1), RFC 9639 (FLAC), RFC 3533 (Ogg), RFC 6716 (Opus),
the AOMedia AV1 Bitstream and Decoding Process Specification, and ISO/IEC
14496-12 (ISO base media file format); it lists every planned specification.

alveus is licensed under the European Union Public Licence 1.2
([LICENSE](LICENSE)). Licence and copyright information for every file
follows the [REUSE](https://reuse.software) specification; `reuse lint`
checks it.

## Standards & Governance

This repository declares the High-Integrity Systems Standard (HISS-21) in
[AGENTS.md](AGENTS.md). The `make verify-all` target defined in
[Makefile](Makefile) is the repository gate.

<!-- praetor:readme-governance:start -->
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
<!-- praetor:readme-governance:end -->
