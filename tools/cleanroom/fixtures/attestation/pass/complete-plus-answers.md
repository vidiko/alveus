<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# Pull Request

## Description

Add the mechanical clean-room attestation check and its fixture corpus.

## Clean-Room Attestation

<!-- Required for every pull request. See CLEANROOM.md. -->

- [x] While preparing this change, I did not read, copy or translate FFmpeg
  or libav source, or source derived from it (forks, patch sets, ports,
  bindings, documentation in their source trees).
- [x] Every input I used is listed below and is allowed for the role I held,
  as the Allowed inputs and Roles tables in CLEANROOM.md define it. If I held
  the implementer role, I used only the inputs marked for both roles and no
  measurements of my own: other programs' behaviour reached me only through
  spec notes and committed fixtures. If I held the spec-writer role, every
  black-box measurement I made is listed below. A change that touches no
  component (documentation, plan) uses only the inputs the Allowed inputs
  table lists.

**Inputs used** (document and clause, spec note, or measurement):

+ CLEANROOM.md, section Attestation (check 2).
+ docs/plan/milestones.md, milestone M0 exit criterion 2.

**Roles** (who wrote the spec notes, who wrote the implementation, per
component touched):

+ No codec or container component touched (CI tooling over pull request text).

**Past exposure to disclose** (or "none"):

+ Read RFC 9043 and RFC 9559 in prior specification review; no FFmpeg or libav
  source exposure.

## Pre-Merge Verification Checklist

- [x] Local verification passed: `make verify-all`
- [x] No new HISS / NASA Power-of-10 infractions (all new/modified functions
  $\le 60$ LOC)
- [x] 3D Tests included (Positive, Negative, Boundary) for public APIs
- [x] Agent contexts in sync: `standardsctl compile-context --verify`
- [x] Commit messages adhere to Conventional Commits format
