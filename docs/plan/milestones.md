# Milestone ladder

The ladder starts with one container and one codec working end to end, then
widens one step at a time. Each milestone lists its scope, the test material
it is checked against, and exit criteria that a command or test can show.
Scope rows refer to [scope-matrix.md](scope-matrix.md); crates refer to
[architecture.md](architecture.md).

Each milestone becomes a forge milestone with the title shown in its heading.

## Order and dependencies

| Milestone | Depends on | Why this order |
| :--- | :--- | :--- |
| M0 | — | Gates and the clean-room check exist before the first line of codec code. |
| M1 | M0 | Matroska and FFV1 form the smallest slice that exercises every stage; FFV1 is lossless, so the original frames are an exact test oracle. |
| M2 | M1 | Writing what M1 reads closes the round trip. |
| M3 | M1 | FLAC adds audio and a second container, reusing the Matroska demuxer. |
| M4 | M2, M3 | The pipeline and command-line tool join the slices and serve the first consumer. |
| M5 | M4 | Ogg and Opus add a lossy codec with a published conformance procedure. |
| M6 | M4 | AV1 is the first lossy video decoder and the largest component; it starts once the pipeline is stable. |
| M7 | M6 | The ISO base media file format carries the AV1 streams M6 decodes. |

The first choice, Matroska with FFV1, is recorded with its alternatives in
[ADR-0001](../adr/0001-first-slice-matroska-ffv1.md).

## Spec notes come first

In every milestone from M1 on, the spec writer delivers spec notes for a
component before the implementer starts on it, as
[CLEANROOM.md](../../CLEANROOM.md#roles) requires. The notes pin the
specification edition and list the clauses the milestone covers.

## M0: Workspace, gates and clean-room attestation check

**Scope.** Cargo workspace with `alveus-core`, `alveus-io`, `alveus-bits` and
`alveus-conformance`; pinned toolchain; `cargo fmt`, `cargo clippy`,
`cargo test` and `cargo deny` in `make verify-all`; the attestation check from
[CLEANROOM.md](../../CLEANROOM.md#attestation); the conformance manifest
format.

**Exit criteria.**

1. `make verify-all` runs the Rust steps and exits 0 on the default branch.
2. A planted pull request without an attestation block fails the attestation
   check, and is closed unmerged once the failure is recorded.
3. `cargo deny check` rejects a planted dependency with an incompatible
   licence.
4. The `alveus-bits` reader has positive, negative and boundary tests, and its
   fuzz target runs for one CPU hour without a crash or hang.

## M1: Matroska demux and FFV1 decode, bit-exact

**Scope.** `alveus-ebml`; `alveus-matroska` demuxer for the elements the
codec mapping of FFV1 needs (EBML header, segment information, tracks,
clusters, simple blocks and block groups, lacing); `alveus-ffv1` decoder for
versions 0, 1 and 3 of RFC 9043, both entropy coder modes, every colour space
and bit depth RFC 9043 defines, slices and slice CRCs.

**Test material.**

- The CELLAR working group's Matroska test files
  (`ietf-wg-cellar/matroska-test-files` on GitHub). Its licence is confirmed
  before any file is committed; until then the harness downloads the files
  into a local cache.
- FFV1 streams that the spec writer produces by running an FFV1 encoder as a
  black box on raw frames that `alveus-conformance` generates. Because FFV1
  is lossless, those raw frames are the expected output.

**Exit criteria.**

1. Every Matroska test file either demuxes, with packet counts and timestamps
   matching the expected values in the spec notes, or fails with a typed
   error that names the unsupported feature. No file causes a panic.
2. Every generated FFV1 stream decodes to frames identical, byte for byte, to
   the raw frames it was made from.
3. The fuzz targets for EBML, Matroska and FFV1 run for one CPU hour each
   without a crash or hang.

## M2: FFV1 encode and Matroska mux, round trip

**Scope.** `alveus-ffv1` encoder; `alveus-matroska` muxer.

**Exit criteria.**

1. Encoding, muxing, demuxing and decoding reproduces the input frames
   exactly, for every generated input and every FFV1 version and coder mode
   the encoder supports.
2. An independent Matroska validator, run as a black box, reports no errors
   on files alveus writes. The testing page names and pins the validator.
3. An independent FFV1 decoder, run as a black box, decodes alveus's output to
   the same frames.

## M3: FLAC decode in native FLAC and Matroska

**Scope.** `alveus-flac` decoder and native FLAC demuxer; FLAC tracks in
Matroska.

**Test material.** The CELLAR working group's FLAC test files
(`ietf-wg-cellar/flac-test-files` on GitHub, CC0-1.0). RFC 9639 stores an MD5
checksum of the decoded audio in each stream's STREAMINFO block, which gives
an exact oracle.

**Exit criteria.**

1. Every file the set marks as valid decodes to audio whose MD5 matches its
   STREAMINFO checksum.
2. Every file the set marks as faulty fails with a typed error and no panic.
3. A FLAC stream in Matroska decodes to the same samples as the same stream in
   a native FLAC file.
4. The FLAC fuzz target runs for one CPU hour without a crash or hang.

## M4: Pipeline, CLI level L0 and raw frame output

**Scope.** `alveus-pipeline`, `alveus-filters`, `alveus-y4m` and
`alveus-cli` at compatibility level L0; pipes; PCM, uncompressed video and
text passthrough in Matroska.

**First consumer.** Video quality measurement: a VMAF (Video Multi-Method
Assessment Fusion, a perceptual quality metric) tool reads alveus-decoded
frames through YUV4MPEG2 output or the Rust frame interface. The interface
contract is a follow-up page listed in [README.md](README.md).

**Exit criteria.**

1. The command-line tool converts a Matroska FFV1 file to YUV4MPEG2 and back
   to Matroska FFV1, and the frame hashes at every step equal the decoder's.
2. Each pixel format conversion matches reference values computed in double
   precision from the ITU-R matrices, within the tolerance its spec note
   states.
3. A test with more parallel slices than workers shows the pipeline never
   runs more workers than its configured maximum.
4. A VMAF score computed from alveus-decoded frames equals the score computed
   from the same file decoded by an independent decoder run as a black box.

## M5: Ogg demux and Opus decode

**Blocked by** the open question on normative reference code in
[CLEANROOM.md](../../CLEANROOM.md#open-questions), because RFC 6716 publishes
the Opus reference implementation as part of the specification.

**Scope.** `alveus-ogg`; `alveus-opus` decoder; Opus in Ogg (RFC 7845) and in
Matroska.

**Exit criteria.**

1. The decoder passes the conformance procedure RFC 6716 defines, on every
   published test vector.
2. Ogg pages with a bad CRC or a broken sequence fail with a typed error and
   no panic.
3. The Ogg and Opus fuzz targets run for one CPU hour each without a crash or
   hang.

## M6: AV1 decode with Argon Streams conformance

**Scope.** `alveus-av1` decoder for the Main profile at 8 and 10 bits; AV1 in
Matroska and WebM. This milestone is split into smaller milestones when M4
lands.

**Test material.** Argon Streams AV1, a conformance stream set covering the
AV1 specification, which Graphcore open-sourced through the Alliance for Open
Media in September 2022.

**Exit criteria.**

1. Every Argon stream within the Main profile decodes with output hashes
   matching the set's expected values.
2. An independent AV1 decoder, run as a black box, produces the same frames
   on a sample of real-world streams.
3. The AV1 fuzz target runs for one CPU hour without a crash or hang.

## M7: ISO base media file format demux

**Scope.** `alveus-isobmff` demuxer for AV1 and FLAC tracks.

**Test material.** Chosen and pinned when the milestone starts.

**Exit criteria.**

1. AV1 and FLAC streams in ISO base media files demux to the same packets as
   the same streams in Matroska.
2. Malformed box trees fail with a typed error and no panic.
3. The demuxer's fuzz target runs for one CPU hour without a crash or hang.
