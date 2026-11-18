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
| M1 | M0 | Matroska and FFV1 form the smallest slice that covers demux, decode, encode and mux across M1 and M2; FFV1 is lossless, so the original frames are an exact test oracle. |
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
`cargo test` and `cargo deny` in `make verify-all`; the attestation check and
the provenance scan from [CLEANROOM.md](../../CLEANROOM.md#attestation); the
conformance manifest format.

**Exit criteria.**

1. `make verify-all` runs the Rust steps and exits 0 on the default branch.
2. The attestation check has committed fixtures in both directions: a
   complete attestation passes, and a missing block, an unchecked box and an
   empty or placeholder field each fail. The check runs again whenever a
   pull request's description is edited. A planted pull request without an
   attestation block fails the check on the forge, and so does one whose
   passing attestation is then deleted by an edit; each is closed unmerged
   once the failure is recorded. The check is then added to the required
   status checks in `.github/rulesets/main.json`.
3. The provenance scan fails a planted file whose header names FFmpeg as its
   copyright holder, passes the repository without it, and is then added to
   the required status checks in `.github/rulesets/main.json`.
4. `cargo deny check` rejects a planted dependency with an incompatible
   licence.
5. The `alveus-bits` reader has positive, negative and boundary tests, and its
   fuzz target runs for one CPU hour without a crash or hang.

## M1: Matroska demux and FFV1 decode, bit-exact

**Scope.** `alveus-ebml`; `alveus-matroska` demuxer for the elements the
codec mapping of FFV1 needs (EBML header, segment information, tracks,
clusters, simple blocks and block groups, lacing); `alveus-ffv1` decoder for
versions 0, 1 and 3 of RFC 9043, both entropy coder modes, every colour space
and bit depth RFC 9043 defines, slices and slice CRCs.

**Test material.**

- The CELLAR working group's Matroska test files
  (`ietf-wg-cellar/matroska-test-files` on GitHub). The repository declares
  no licence, and its readme names a licence only for the films the clips
  come from. The spec writer confirms the licence of the files themselves
  before the harness downloads or uses any of them. If none can be
  confirmed, the M1 Matroska set consists of files the spec writer produces
  by running a Matroska muxer as a black box instead.
- FFV1 streams that the spec writer produces by running an FFV1 encoder as a
  black box on raw frames that `alveus-conformance` generates. Because FFV1
  is lossless, those raw frames are the expected output. The spec notes
  define a test-vector matrix with one cell for every combination of
  version, coder mode, colour space and bit depth in M1 scope that RFC 9043
  permits, and the generated streams cover every cell.

**Exit criteria.**

1. Before implementation starts, the spec notes record the expected packet
   counts and timestamps of every file in the M1 Matroska set, and list the
   files that use features outside M1 scope. Every file that uses only
   in-scope features demuxes with packet counts and timestamps matching the
   spec notes. Only the listed files may fail, and each fails with a typed
   error that names the unsupported feature. No file causes a panic.
2. Every generated FFV1 stream, in the Matroska file the black-box encoder
   wrote, demuxes with `alveus-matroska` and decodes with `alveus-ffv1` to
   frames identical, byte for byte, to the raw frames it was made from.
3. The fuzz targets for EBML, Matroska and FFV1 run for one CPU hour each
   without a crash or hang.

## M2: FFV1 encode and Matroska mux, round trip

**Scope.** `alveus-ffv1` encoder; `alveus-matroska` muxer.

**Exit criteria.**

1. Encoding, muxing, demuxing and decoding reproduces the input frames
   exactly, for every generated input and every FFV1 version and coder mode
   that [scope-matrix.md](scope-matrix.md) lists for encoding (versions 0, 1
   and 3, both coder modes).
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
an exact oracle where it is present. It is not always present: section 8.2 of
RFC 9639 defines an all-zero value as "not known", and uncommon files 10 and
11 of the set start at a frame header or with unparsable data, so they carry
no STREAMINFO block at all. For every such stream, the spec writer records
the decoded-audio MD5 that two independent decoders, run as black boxes,
agree on, and commits it as a fixture.

**Exit criteria.**

1. Before implementation starts, the spec notes list the files in the subset
   and uncommon groups, which the set's readme calls valid FLAC, that use
   features outside M3 scope. Every other file in those groups decodes to
   audio whose MD5 matches its oracle: the STREAMINFO checksum where it is
   non-zero, otherwise the recorded fixture. Each listed file fails with a
   typed error that names the unsupported feature.
2. Every file in the faulty group fails with a typed error and no panic.
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
5. Converting through standard input and standard output gives the same
   frame hashes as converting between files.
6. Matroska files with PCM audio, uncompressed video and text tracks, which
   the spec writer produces by running a Matroska muxer as a black box, pass
   through demux and mux unchanged: the codec ID, codec private data, block
   payloads and timestamps of every track equal the input's.

## M5: Ogg demux and Opus decode

**Scope.** `alveus-ogg`; `alveus-opus` decoder; Opus in Ogg (RFC 7845) and in
Matroska.

**Inputs.** RFC 6716 publishes the Opus reference implementation as part of
the specification. Under
[ADR-0003](../adr/0003-normative-reference-code-in-specifications.md), only
the spec writer reads that code and describes its behaviour in spec notes;
the implementer never reads it.

**Exit criteria.**

1. The decoder passes the conformance procedure RFC 6716 defines, on every
   published test vector.
2. Ogg pages with a bad CRC or a broken sequence fail with a typed error and
   no panic.
3. The Ogg and Opus fuzz targets run for one CPU hour each without a crash or
   hang.
4. Each test vector, put into Matroska by a Matroska muxer that the spec
   writer runs as a black box, decodes to the same samples as the same
   stream in Ogg.

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
4. A sample of Argon streams, put into Matroska and into WebM by a muxer that
   the spec writer runs as a black box, decodes to the same output hashes as
   the streams on their own.

## M7: ISO base media file format demux

**Scope.** `alveus-isobmff` demuxer for AV1 and FLAC tracks.

**Test material.** Chosen and pinned when the milestone starts.

**Exit criteria.**

1. AV1 and FLAC streams in ISO base media files demux to the same packets as
   the same streams in Matroska.
2. Malformed box trees fail with a typed error and no panic.
3. The demuxer's fuzz target runs for one CPU hour without a crash or hang.
