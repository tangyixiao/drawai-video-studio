"""Restore unchanged upstream files from the exact, verified source archive."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'f4932d75f96d89ef33ab861699534599d897c76c'
ARCHIVE_SHA256 = '914a1bac8ee8e004adc377523fb65af32add22b5094f5a9635d31e0cd3c5fdbc'
PREFIX = f'dsh-drawai-{COMMIT}/skills/workbuddy/'


def refresh(archive):
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError('Source archive does not match the pinned SHA-256')
    target = ROOT / 'skills' / 'drawai-video-studio'
    unchanged, adapted = {}, {}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            if not member.isfile() or not member.name.startswith(PREFIX):
                continue
            relative = PurePosixPath(member.name[len(PREFIX):])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Invalid source path')
            data = tar.extractfile(member).read()
            file_hash = hashlib.sha256(data).hexdigest()
            if str(relative) == 'SKILL.md':
                adapted[str(relative)] = file_hash
                continue
            path = target.joinpath(*relative.parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            unchanged[str(relative)] = file_hash
    if len(unchanged) != 528 or not adapted:
        raise ValueError('Unexpected upstream file set')
    manifest = {
        'repository': 'https://github.com/fourzkw/dsh-drawai',
        'commit': COMMIT,
        'sourceDirectory': 'skills/workbuddy',
        'sourceArchiveSha256': digest,
        'unchanged': unchanged,
        'adaptedOriginalHashes': adapted,
    }
    (ROOT / 'upstream-files.sha256.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'Restored {len(unchanged)} unchanged upstream files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    refresh(parser.parse_args().archive)
