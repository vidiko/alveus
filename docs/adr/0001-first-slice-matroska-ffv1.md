# ADR-0001: First vertical slice is Matroska with FFV1

- **Status**: Accepted
- **Date**: 2026-11-18
- **Authors**: alveus maintainers

## Context

The plan in [docs/plan/milestones.md](../plan/milestones.md) starts with one
container and one codec working end to end. That first slice decides which
crates exist first and how the test harness checks output, so it should:

- exercise every stage of the pipeline: demux, decode, encode and mux;
- come with an exact test oracle, so a passing test means the output is
  correct, not just plausible;
- rest on published, freely readable specifications;
- lead towards the later milestones instead of being thrown away.

Candidates considered:

| Option | Specifications | Assessment |
| :--- | :--- | :--- |
| Matroska with FFV1 | RFC 9559, RFC 8794, RFC 9043 | Lossless video, so the source frames are the oracle. Matroska carries most later codecs. |
| Ogg with FLAC | RFC 3533, RFC 9639 | Lossless with a checksum oracle, but audio only, and Ogg carries few of the later codecs. |
| ISO base media with AV1 | ISO/IEC 14496-12, AOMedia AV1 specification | Highest user value, but AV1 is the largest component, and the oracle needs a conformance stream set. |
| YUV4MPEG2 with raw video | No standards-body specification | Small, but exercises no codec. |

## Decision

The first slice is Matroska demux with FFV1 decode (milestone M1), followed by
FFV1 encode with Matroska mux (milestone M2). FLAC follows in M3, reusing the
Matroska demuxer, and AV1 starts after the pipeline milestone M4.

## Consequences

- **Positive**: M2 completes the round trip of demux, decode, encode and
  mux; filters follow in M4. The EBML and Matroska
  crates carry FLAC, Opus and AV1 later. Lossless decoding gives exact tests
  from the first milestone.
- **Negative**: The first slice serves few end users; AV1, the codec with the
  widest use, waits until M6. FFV1 test streams come from an encoder run as a
  black box, because no published FFV1 conformance set exists yet.

**Revisit when** FFV1 test streams cannot be produced without inputs that
[CLEANROOM.md](../../CLEANROOM.md) forbids, or when the first consumer needs a
codec other than FFV1 before M4.
