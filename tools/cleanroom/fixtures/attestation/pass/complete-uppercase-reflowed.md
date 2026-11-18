<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# Pull Request

## Description

Reflowed checkboxes with uppercase X and nested sub-bullets under inputs.

## Clean-Room Attestation

- [X] While preparing this change, I did not read, copy or translate FFmpeg or libav source, or source derived from it (forks, patch sets, ports, bindings, documentation in their source trees).
- [X] Every input I used is listed below and is allowed for the role I held, as the Allowed inputs and Roles tables in CLEANROOM.md define it. If I held the implementer role, I used only the inputs marked for both roles and no measurements of my own: other programs' behaviour reached me only through spec notes and committed fixtures. If I held the spec-writer role, every black-box measurement I made is listed below. A change that touches no component (documentation, plan) uses only the inputs the Allowed inputs table lists.

**Inputs used** (document and clause, spec note, or measurement):

- RFC 8794 (Extensible Binary Meta Language):
  - Section 4, Variable-Size Integer.
  - Section 7, Element Data.
- docs/plan/milestones.md, milestone M1 exit criterion 1.

**Roles** (who wrote the spec notes, who wrote the implementation, per
component touched):

- Spec writer: operator session (spec note committed in prior PR).
- Implementer: fresh clean-room implementation lane.

**Past exposure to disclose** (or "none"):

- none
