# Paper storyboard

A six-second silent visual pilot implementing the selected light-paper direction.
Text, paper layers, crop marks and proofing circle are editable TSX/CSS/SVG.
The illustration is an original AI-generated asset; it is included under this
repository's adapter license. It does not depict an existing character.

Prepare the installed skill's dependencies and upstream asset/runtime caches
using `wb setup --install` as described in the repository README. Then run the
installed skill's `scripts/wb.mjs` with the absolute path to this example:

```sh
node /path/to/installed/skill/scripts/wb.mjs preview --dir /path/to/this/example --frames 105
node /path/to/installed/skill/scripts/wb.mjs render --dir /path/to/this/example --wait
```

Rendering creates local font copies, an entry file and `.out/film.mp4`; these
generated files are excluded from Git. Specifications: 1440x810, 30fps, 180
frames. The composition is designed at that size; changing the aspect ratio
requires recomposition.

No sound or synchronization approval is implied. Automated quality checks
are separate from visual review.
