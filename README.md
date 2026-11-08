# DrawAI Video Studio for Codex

A local Codex skill for editable, code-driven video projects using Remotion,
React and optional three.js/WebGL. It adapts the standalone engine from
[fourzkw/dsh-drawai](https://github.com/fourzkw/dsh-drawai); it does not require
DSH or its canvas plugin.

The upstream engine provides shot-based TSX projects, 124 shot cards, 14 style
recipes, still previews, pilot/final rendering, audio tools and quality checks.
This repository adds Codex packaging and a workflow that reviews real visual
references and direction frames before producing an original video.

## Install

Requires Node.js 20+ and npm. Python 3 is needed only for the installer below.
The installer refuses to overwrite an existing skill.

```sh
git clone https://github.com/tangyixiao/drawai-video-studio.git
cd drawai-video-studio
python tools/install.py
```

The skill is copied to `$CODEX_HOME/skills/drawai-video-studio`, or
`~/.codex/skills/drawai-video-studio` if `CODEX_HOME` is unset. It becomes
available on the next Codex turn. You can also use Codex's skill installer with
repository `tangyixiao/drawai-video-studio` and path `skills/drawai-video-studio`.

Prepare the small CLI dependencies in the **installed skill's** `scripts/`
directory, then inspect the environment:

```sh
npm ci --omit=dev --ignore-scripts --no-audit --no-fund
node wb.mjs doctor --json
node wb.mjs setup --install
```

`doctor` reports missing components; it does not prove rendering readiness
unless `ready` is true. Setup downloads the upstream asset pack and a separate
Remotion runtime. FFmpeg and Chrome/Edge are also required by relevant commands.
Initial downloads may take several hundred megabytes. Normal operation uses the
upstream caches under `~/.dsh/`; the folder name does not require DSH to be installed.
For proxies use the upstream documented environment variables; never disable TLS
verification to make a download succeed.

## Use in Codex

```text
Use $drawai-video-studio to turn this content into a 15-second product film.
Show a few visual directions using the real copy, then build a short pilot
in the chosen direction before completing the film.
```

Existing approved designs can be edited directly. For a new direction, use real
references and show compositions, typography and palette together. A passing
technical check is separate from visual approval.

For direct CLI use, run from the installed skill directory:

```sh
node scripts/wb.mjs create --dir ./my-film --spec 1920x1080@30 --duration 12
# Edit the storyboard and scene-N.tsx files.
node scripts/wb.mjs preview --dir ./my-film --at 1,3
node scripts/wb.mjs render --dir ./my-film --range 0,90 --wait
node scripts/wb.mjs render --dir ./my-film --wait
node scripts/wb.mjs qa --dir ./my-film
```

The generated project keeps its timeline, scenes and assets editable. See the
[upstream command reference](skills/drawai-video-studio/references/commands.md)
for audio, synchronization, style source, rendering and Jianying exports.

## Example: paper storyboard

[Paper storyboard](examples/paper-storyboard/README.md) implements a selected
light-paper direction with large black Chinese typography and staggered
storyboard layers. It is a six-second silent visual pilot, with editable TSX,
theme, timeline and an original AI-generated illustration. The example is
separate from the installable skill ZIP.

## Validation and limits

```sh
python -m unittest discover -s tests -v
npm ci --prefix skills/drawai-video-studio/scripts --omit=dev --ignore-scripts
node skills/drawai-video-studio/scripts/wb.mjs --help
node skills/drawai-video-studio/scripts/wb.mjs card list --json
node skills/drawai-video-studio/scripts/wb.mjs style list --json
```

CI checks distribution integrity, portable installation and CLI/catalog loading
on Windows, Linux and macOS. It does **not** run a production video render,
audition sound, judge aesthetics or test DSH plugin activation. A Windows local
smoke test produced a 960x540, 30 fps, 90-frame film; that is a renderer check,
not an example of a finished creative direction.

## Attribution

Original engine and standalone skill: **fourzkw / DrawAI**. Codex adaptation:
**Tangyixiao**. See [NOTICE.md](NOTICE.md) for the exact upstream revision and
adaptation scope. Adapter code is MIT; upstream and third-party licenses are
retained in place. This is an independent derivative, not an official upstream release.
