# Pull Request

## Description

<!-- Summarize the changes and their architectural rationale. -->

## Clean-Room Attestation

<!-- Required for every pull request. See CLEANROOM.md. -->

- [ ] While preparing this change, I did not read, copy or translate FFmpeg
  or libav source, or source derived from it (forks, patch sets, ports,
  bindings, documentation in their source trees).
- [ ] Every input I used is a public specification, a spec note, a committed
  fixture or my own measurement, and is listed below.

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
