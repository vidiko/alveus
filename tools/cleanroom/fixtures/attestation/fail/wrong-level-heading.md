<!--
SPDX-FileCopyrightText: 2026 Lusoris <lusoris@pm.me>
SPDX-License-Identifier: EUPL-1.2
-->

# Pull Request

## Description

Heading uses level 3 (`### Clean-Room Attestation`) instead of level 2.

### Clean-Room Attestation

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

- CLEANROOM.md, section Attestation (check 2).

**Roles** (who wrote the spec notes, who wrote the implementation, per
component touched):

- No codec or container component touched.

**Past exposure to disclose** (or "none"):

- None.
