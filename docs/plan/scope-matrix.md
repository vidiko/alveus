# Scope matrix

This matrix lists what alveus plans to support, from which specification, and
in which milestone. Every row names its specification so a contributor knows
where to start; the clean-room rules in [CLEANROOM.md](../../CLEANROOM.md)
decide what else they may read.

## How to read the tiers

| Tier | Meaning |
| :--- | :--- |
| **P0** | Part of the first vertical slices (milestones M1 to M3). |
| **P1** | Planned next, with a milestone (M4 to M7). |
| **P2** | Planned, not scheduled. Gets a milestone when a P1 row lands or a user needs it. |
| **P3** | Considered, no plan. Revisited on request. |
| **X** | Out of scope. A change needs a decision record under [docs/adr/](../adr/). |

Milestone numbers refer to [milestones.md](milestones.md). Specification
editions are pinned when a row's milestone starts, in the spec notes for that
component.

## Containers

| Container | Specification | Read (demux) | Write (mux) |
| :--- | :--- | :--- | :--- |
| Matroska | RFC 9559, on EBML (RFC 8794); codec mappings from the Internet-Draft `draft-ietf-cellar-codec` | P0, M1 | P0, M2 |
| WebM | Matroska subset defined by the WebM project's container guidelines | P1, M6 | P2 |
| Native FLAC | RFC 9639 | P0, M3 | P2 |
| Ogg | RFC 3533; Opus mapping RFC 7845 | P1, M5 | P2 |
| ISO base media file format (MP4) | ISO/IEC 14496-12; AV1 binding from the AOMedia AV1 Codec ISO Media File Format Binding | P1, M7 | P2 |
| YUV4MPEG2 (Y4M) raw video | No standards-body specification; the spec writer documents the header grammar from public descriptions and measurement | P1, M4 | P1, M4 |
| RIFF WAVE | Vendor specification | P2 | P2 |
| MPEG-2 transport stream | ITU-T H.222.0 (ISO/IEC 13818-1) | P2 | P3 |
| Other legacy containers | — | P3 | X |

## Video codecs

| Codec | Specification | Decode | Encode |
| :--- | :--- | :--- | :--- |
| FFV1 versions 0, 1, 3 | RFC 9043 | P0, M1 | P0, M2 |
| FFV1 version 4 | Internet-Draft `draft-ietf-cellar-ffv1-v4`, not published as an RFC | X until published | X until published |
| Uncompressed video in Matroska | Codec mapping draft (`V_UNCOMPRESSED`) | P1, M4 | P1, M4 |
| AV1 | AOMedia AV1 Bitstream and Decoding Process Specification | P1, M6 | X |
| VP9 | VP9 Bitstream and Decoding Process Specification | P2 | X |
| VP8 | RFC 6386 | P2 | X |
| H.264 | ITU-T H.264 (ISO/IEC 14496-10) | P2 | X |
| H.265 | ITU-T H.265 (ISO/IEC 23008-2) | P3 | X |
| H.266 | ITU-T H.266 (ISO/IEC 23090-3) | P3 | X |
| MPEG-2 video | ITU-T H.262 (ISO/IEC 13818-2) | P3 | X |

Lossy encoders are out of scope: mature encoders exist, and alveus can reach
them through its encoder interface later without writing one. Patent
licensing of the ITU-T codecs is checked before a release ships them; it does
not change their tier.

## Audio codecs

| Codec | Specification | Decode | Encode |
| :--- | :--- | :--- | :--- |
| FLAC | RFC 9639 | P0, M3 | P2 |
| PCM, integer and float | Matroska codec mapping draft; RIFF WAVE | P1, M4 | P1, M4 |
| Opus | RFC 6716; Ogg mapping RFC 7845; Matroska codec mapping draft | P1, M5 | X |
| Vorbis | Xiph Vorbis I specification | P2 | X |
| MPEG-1 and MPEG-2 Audio Layer III | ISO/IEC 11172-3, ISO/IEC 13818-3 | P3 | X |
| AAC | ISO/IEC 14496-3 | P3 | X |
| AC-3 and E-AC-3 | ETSI TS 102 366 | P3 | X |

## Subtitles and text

| Format | Specification | Read | Write |
| :--- | :--- | :--- | :--- |
| Matroska text tracks, passthrough | Codec mapping draft (`S_TEXT/UTF8`) | P1, M4 | P1, M4 |
| WebVTT | W3C WebVTT | P2 | P2 |

## Filters

| Filter | Specification | Tier |
| :--- | :--- | :--- |
| Pixel format and colour conversion | ITU-R BT.601, BT.709, BT.2020; code points from ITU-T H.273 | P1, M4 |
| Crop and pad | — | P1, M4 |
| Audio sample format conversion | — | P1, M4 |
| Scaling | Resampling kernels from published literature | P2 |
| Frame rate and timestamp operations | — | P2 |
| Audio resampling | Published literature on band-limited interpolation | P2 |
| Channel remixing | — | P3 |
| Deinterlacing, overlay, text rendering, tone mapping | — | P3 |

Pixel format conversion comes first because the first consumer of decoded
frames is quality measurement (see M4 in [milestones.md](milestones.md)),
which needs frames in a defined layout and colour space.

## Protocols and I/O

| Protocol | Specification | Tier |
| :--- | :--- | :--- |
| Local files | — | P0, M1 |
| Pipes (standard input and output) | — | P1, M4 |
| HTTP and HTTPS with byte ranges | RFC 9110, RFC 9112; TLS 1.3 (RFC 8446) through a reviewed dependency | P2 |
| HTTP Live Streaming, read | RFC 8216 | P2 |
| MPEG-DASH, read | ISO/IEC 23009-1 | P3 |
| RTP | RFC 3550 | P3 |
| RTSP 2.0 | RFC 7826 | P3 |
| Other streaming protocols | — | P3 |

Every I/O call carries a deadline, as the repository standard requires
(HISS-02 in [AGENTS.md](../../AGENTS.md)).

## Hardware APIs

Hardware acceleration starts after the software paths it accelerates are
complete and tested, so every hardware path has a software reference to
compare against.

| API | Specification | Tier |
| :--- | :--- | :--- |
| Vulkan Video, decode | Khronos Vulkan specification, video extensions | P2 |
| VA-API, decode | VA-API reference and public headers | P2 |
| NVIDIA Video Codec SDK | Vendor SDK documentation and headers | P3 |
| Intel Video Processing Library | Vendor documentation and headers | P3 |
| V4L2 memory-to-memory codec interface | Linux kernel documentation | P3 |
| Apple VideoToolbox | Vendor documentation | P3 |
| Microsoft Media Foundation, Direct3D 12 Video | Vendor documentation | P3 |

Vulkan Video ranks first because one API covers several vendors.

## Command-line compatibility levels

alveus ships its own command-line tool. Compatibility with FFmpeg's command
line is graded in levels, so a user knows how much of an existing command
carries over:

| Level | Meaning | Tier |
| :--- | :--- | :--- |
| **L0** | alveus's own grammar (`alveus <verb> ...`), documented in its own help. No compatibility claim. | P1, M4 |
| **L1** | A listed subset of common FFmpeg-style options (input, output, stream selection, codec choice, overwrite) accepted as aliases. Behaviour follows alveus's own specification, not FFmpeg's. | P2 |
| **L2** | A corpus of real command lines, each with its expected result, accepted and checked by black-box comparison. | P3 |
| **L3** | Drop-in replacement, including filter-graph syntax and identical output. | X |

Level L1 waits for the command-line naming question in
[CLEANROOM.md](../../CLEANROOM.md#open-questions).
