"""Create a skill ZIP from source, excluding installed dependencies and outputs."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = 'drawai-video-studio'
VERSION = '0.1.1'
EXCLUDED = {'node_modules', '.runtime', '.out', '__pycache__', '.git'}


def package(output: Path):
    source = ROOT / 'skills' / SKILL
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            relative = path.relative_to(source)
            if any(part in EXCLUDED for part in relative.parts) or path.suffix == '.pyc':
                continue
            if path.is_symlink():
                raise ValueError(f'Release source contains a symlink: {relative}')
            if path.is_file():
                archive.write(path, str(Path(SKILL) / relative))
        archive.write(ROOT / 'LICENSE', f'{SKILL}/ADAPTER-LICENSE')
        archive.write(ROOT / 'NOTICE.md', f'{SKILL}/ADAPTER-NOTICE.md')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / f'{SKILL}-v{VERSION}.zip')
    print(package(parser.parse_args().output))
