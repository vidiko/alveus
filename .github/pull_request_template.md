# Pull Request

## Description

<!-- Summarize the changes and their architectural rationale. -->

## Clean-Room Attestation

<!-- Required for every pull request. See CLEANROOM.md. -->

- [ ] While preparing this change, I did not read, copy or translate FFmpeg
  or libav source, or source derived from it (forks, patch sets, ports,
  bindings, documentation in their source trees).
- [ ] Every input I used is listed below and is allowed for the role I held,
  as the Allowed inputs and Roles tables in CLEANROOM.md define it. As
  implementer, I used no measurements of my own: other programs' behaviour
  reached me only through spec notes and committed fixtures. A change that
  touches no component (documentation, plan) uses only the inputs the
  Allowed inputs table lists.

**Inputs used** (document and clause, spec note, or measurement):

-

**Roles** (who wrote the spec notes, who wrote the implementation, per
component touched):

-

**Past exposure to disclose** (or "none"):

-

## Pre-Merge Verification Checklist

- [ ] Local verification passed: `make verify-all`
- [ ] No new HISS / NASA Power-of-10 infractions (all new/modified functions
  $\le 60$ LOC)
- [ ] 3D Tests included (Positive, Negative, Boundary) for public APIs
- [ ] Agent contexts in sync: `standardsctl compile-context --verify`
- [ ] Commit messages adhere to Conventional Commits format
