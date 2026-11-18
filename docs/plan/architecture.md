# Crate architecture

alveus is a Cargo workspace of small crates. Each crate owns one format, one
codec or one shared concern, so a user links only what they need and a
contributor can work on one component without touching the others.

This page describes the planned layout. None of these crates exist yet; M0 in
[milestones.md](milestones.md) creates the workspace, and each later
milestone adds the crates it names.

## Data flow

A conversion runs through the same five stages, whichever formats are
involved:

```text
byte source -> demuxer -> decoder -> filters -> encoder -> muxer -> byte sink
                  |                                           ^
                  +--------------- packets (copy) ------------+
```

- A **demuxer** turns bytes into packets, one stream at a time, each with a
  timestamp in that stream's time base.
- A **decoder** turns packets into frames: video pictures or blocks of audio
  samples.
- **Filters** turn frames into frames.
- An **encoder** turns frames into packets, and a **muxer** turns packets into
  bytes.
- Copying a stream without re-encoding passes packets from demuxer to muxer
  directly.

## Crates

| Crate | Owns | First milestone |
| :--- | :--- | :--- |
| `alveus-core` | Shared types: rational time bases and timestamps, stream and media descriptions, packets, frames, sample and pixel formats, colour metadata (ITU-T H.273 code points), the error type | M0 |
| `alveus-io` | Byte sources and sinks with explicit deadlines, bounded reads, seeking | M0 |
| `alveus-bits` | Bit readers and writers, variable-length integer and Golomb-family codes | M0 |
| `alveus-ebml` | EBML elements (RFC 8794): reading, writing, schema-driven validation | M1 |
| `alveus-matroska` | Matroska demuxer and muxer (RFC 9559) | demuxer M1, muxer M2 |
| `alveus-ffv1` | FFV1 decoder and encoder (RFC 9043) | decoder M1, encoder M2 |
| `alveus-flac` | FLAC decoder and native FLAC demuxer (RFC 9639) | M3 |
| `alveus-pipeline` | Stage wiring, bounded queues, the worker pool, stream selection | M4 |
| `alveus-filters` | Pixel format, colour and sample format conversion; crop and pad | M4 |
| `alveus-y4m` | YUV4MPEG2 reader and writer | M4 |
| `alveus-cli` | The `alveus` command-line tool | M4 |
| `alveus-ogg` | Ogg demuxer (RFC 3533) | M5 |
| `alveus-opus` | Opus decoder (RFC 6716) | M5 |
| `alveus-av1` | AV1 decoder | M6 |
| `alveus-isobmff` | ISO base media file format demuxer (ISO/IEC 14496-12) | M7 |
| `alveus-conformance` | Test harness: stream manifests, download cache, hash and frame comparison. Not published. | M0 |

Later rows of [scope-matrix.md](scope-matrix.md) add crates by the same
rule: one format or codec per crate, named `alveus-<name>`. Hardware
acceleration gets one crate per API (for example `alveus-hw-vulkan`), and a C
interface, if one is built, gets `alveus-ffi`.

## Interfaces between crates

Each stage is a trait in `alveus-core`, and each format or codec crate
implements the traits for its component:

- `Demuxer` and `Muxer` exchange packets with stream indices and timestamps.
- `Decoder` and `Encoder` use a send-and-receive model: the caller sends one
  packet or frame, then receives zero or more outputs. Draining at the end of
  a stream is an explicit call, not a special packet.
- `Filter` takes and returns frames, with its output format known before the
  first frame.
- Format detection is a function per container crate that scores the first
  bytes of an input. The pipeline asks every linked container crate and picks
  the highest score. When two crates return the same highest score,
  detection fails with an ambiguity error that names both formats, and the
  caller then names the format explicitly.

Components are registered at compile time through Cargo features. There is no
plugin loading at run time: the repository standard bans dynamic code
execution (HISS-08 in [AGENTS.md](../../AGENTS.md)).

## Rules every crate follows

The repository standard in [AGENTS.md](../../AGENTS.md) applies to all code.
For a media framework, these rules shape the design most:

| Rule | How alveus meets it |
| :--- | :--- |
| No recursion (HISS-01) | Nested structures such as EBML elements are parsed with an explicit stack whose depth has a fixed maximum. |
| Bounded loops and I/O deadlines (HISS-02) | Every parse loop is bounded by the remaining element or packet size, or by a configured limit. Every read and write through `alveus-io` takes a deadline. |
| No allocation in hot loops (HISS-03) | Frame and packet buffers come from pools sized when a stream opens. Per-pixel and per-sample loops do not allocate. |
| Bounded concurrency (HISS-06) | One worker pool per pipeline, with an explicit maximum size. Codecs that allow parallel decoding, such as FFV1 slices, schedule work on that pool. |
| Errors with context (HISS-07) | Each crate returns typed errors that name the stream, position and specification clause involved. No `unwrap` or `expect` outside tests. |
| `unsafe` with proof (HISS-09) | Crates forbid `unsafe` code, except SIMD modules and the C interface. Every `unsafe` block there carries a `// SAFETY:` proof. |
| Append-only public API (HISS-14) | Public items are added, not changed. A breaking change carries a `!` commit subject and a `Migration:` footer. |
| Three-sided tests (HISS-15) | Every public interface has positive, negative and boundary tests; parsers are also fuzzed. |

## SIMD

Every SIMD routine has a plain scalar version, and the scalar version is the
reference. Tests compare SIMD and scalar output bit for bit on the same
inputs. The CPU features in use are detected at run time, and the scalar path
is always available.

## Dependencies

A dependency is added only after a licence check (compatible with EUPL-1.2)
and a provenance check: a crate that ports, translates or binds to FFmpeg or
libav is never added (see [CLEANROOM.md](../../CLEANROOM.md)). Every new crate
in `Cargo.lock`, direct or transitive, gets both checks.

- The licence check is mechanical: M0 sets up `cargo-deny`, which fails on a
  licence, source or banned crate outside the policy.
- The provenance check is a review, because a licence field cannot show
  whether a crate is a port. The reviewer of the pull request that adds the
  crate to `Cargo.lock` records the check in that pull request. A crate found
  to be a port goes on the `cargo-deny` ban list, so from then on the check
  is mechanical for it.

Every dependency is pinned in the committed lockfile (HISS-11).

## Toolchain

The workspace uses Rust edition 2024 and the toolchain pinned in
`rust-toolchain.toml`, both set in M0. The minimum supported Rust version is
the pinned toolchain until the first release states otherwise.
