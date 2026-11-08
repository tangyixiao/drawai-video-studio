# Provenance and scope

This is a Codex adaptation of the standalone Workbuddy skill from
[fourzkw/dsh-drawai](https://github.com/fourzkw/dsh-drawai), pinned to commit
`f4932d75f96d89ef33ab861699534599d897c76c`, source directory `skills/workbuddy`.

The video engine and CLI were written upstream, not by this adapter's author.
Their source is included unchanged, including `scripts/engine/VENDOR.json` and
all nested license/attribution files. `upstream-files.sha256.json` records every
upstream file and distinguishes adapter-edited documents from unchanged files.

Adapter changes: Codex-compatible frontmatter and UI metadata, portable path
instructions, reference-based visual review guidance, installation documentation,
distribution checks, and GitHub CI/release packaging.

The upstream MIT license and third-party notices are retained at
`skills/drawai-video-studio/LICENSE`. Shotcraft source notices and Apache-2.0
licensing remain in the vendored tree. Font, sample, texture and dependency
licenses remain separate; this adapter's MIT license does not relicense them.

No fonts, recordings, preview videos, reference screenshots, FFmpeg binaries,
browser binaries, or downloaded runtime dependencies are included in this
repository. Upstream setup downloads optional assets and rendering dependencies
from upstream sources on demand. Inspect their retained notices for reuse.

The installation smoke test is not a design showcase. This repository makes no
claim that a renderer, style catalog, technical test or CI result guarantees
visual quality.
