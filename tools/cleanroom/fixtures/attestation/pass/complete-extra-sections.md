<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# Pull Request

## Context

Background section before the attestation block with an unchecked task:

- [ ] Optional follow-up task outside the attestation block.

## Description

Verify that extra sections and checkboxes outside the block do not affect it.

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

- RFC 9043 (FFV1 Video Coding Format Version 0, 1, and 3), section 3.

**Roles** (who wrote the spec notes, who wrote the implementation, per
component touched):

- Spec writer: fresh spec lane (`docs/specs/ffv1.md`).

**Past exposure to disclose** (or "none"):

- None.

## Pre-Merge Verification Checklist

- [ ] Local verification passed: `make verify-all`
- [x] 3D Tests included (Positive, Negative, Boundary) for public APIs

## Rollout Notes

No runtime changes outside CI.
