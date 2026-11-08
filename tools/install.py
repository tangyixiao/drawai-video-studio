"""Install the source skill without overwriting an existing installation."""
import argparse
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL = 'drawai-video-studio'


def install(destination: Path) -> Path:
    target = destination.expanduser().resolve() / SKILL
    if target.exists():
        raise FileExistsError(f'Skill already exists; preserve or move it before installing: {target}')
    source = ROOT / 'skills' / SKILL
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('node_modules', '.runtime', '.out', '__pycache__', '*.pyc'))
    shutil.copy2(ROOT / 'NOTICE.md', target / 'ADAPTER-NOTICE.md')
    shutil.copy2(ROOT / 'LICENSE', target / 'ADAPTER-LICENSE')
    return target


def main():
    default = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=default, help='Parent skills directory')
    args = parser.parse_args()
    try:
        target = install(args.dest)
    except FileExistsError as error:
        parser.exit(1, str(error) + '\n')
    print(f'Installed {SKILL} to {target}')
    print('Available on the next Codex turn. Prepare CLI dependencies as described in README.md.')


if __name__ == '__main__':
    main()
