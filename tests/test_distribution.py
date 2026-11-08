import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'drawai-video-studio'


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DistributionTests(unittest.TestCase):
    def test_upstream_sources_and_notices_are_preserved(self):
        manifest = json.loads((ROOT / 'upstream-files.sha256.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['commit'], 'f4932d75f96d89ef33ab861699534599d897c76c')
        for relative, expected in manifest['unchanged'].items():
            with self.subTest(file=relative):
                self.assertEqual(hashlib.sha256((SKILL / relative).read_bytes()).hexdigest(), expected)
        self.assertIn('LICENSE', manifest['unchanged'])
        self.assertIn('scripts/engine/motion/shotcraft/LICENSE', manifest['unchanged'])

    def test_skill_is_portable_and_has_codex_metadata(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('name: drawai-video-studio', text)
        self.assertNotIn('C:/Users/', text)
        self.assertNotIn('C:\\Users\\', text)
        self.assertTrue((SKILL / 'agents' / 'openai.yaml').is_file())

    def test_installer_preserves_existing_installation(self):
        installer = load('install')
        with tempfile.TemporaryDirectory() as temporary:
            target = installer.install(Path(temporary) / 'skills with spaces')
            sentinel = target / 'user-note.txt'
            sentinel.write_text('keep this', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                installer.install(target.parent)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'keep this')
            self.assertTrue((target / 'ADAPTER-NOTICE.md').is_file())
            self.assertTrue((target / 'scripts' / 'wb.mjs').is_file())

    def test_release_has_correct_root_and_no_runtime_or_media(self):
        packager = load('package_release')
        with tempfile.TemporaryDirectory() as temporary:
            archive = packager.package(Path(temporary) / 'skill.zip')
            with zipfile.ZipFile(archive) as release:
                names = release.namelist()
            self.assertIn('drawai-video-studio/SKILL.md', names)
            self.assertIn('drawai-video-studio/ADAPTER-LICENSE', names)
            forbidden = {'.mp4', '.mp3', '.wav', '.ttf', '.woff', '.woff2', '.exe', '.dll', '.png', '.jpg'}
            for name in names:
                self.assertTrue(name.startswith('drawai-video-studio/'))
                self.assertFalse(set(Path(name).parts) & packager.EXCLUDED)
                self.assertNotIn(Path(name).suffix.lower(), forbidden)


if __name__ == '__main__':
    unittest.main()
