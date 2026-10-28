"""Validate the two installable skill bundles, not model output quality."""

import re
import unittest
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

import yaml


ROOT = Path(__file__).resolve().parents[1]
STYLES = {
    "wong-kar-wai", "stephen-chow", "jiang-wen", "feng-xiaogang", "gu-long",
    "jin-yong", "qiong-yao", "lu-xun", "zhao-benshan", "shakespeare",
}
WORKBUDDY_FIELDS = {
    "name", "display_name", "display_name_en", "description", "description_zh",
    "description_en", "version", "author",
}


def read_bundle(platform):
    path = ROOT / "dist" / f"style-switcher-{platform}.zip"
    assert path.is_file(), f"Missing installable bundle: {path.name}"
    with ZipFile(path) as archive:
        assert archive.testzip() is None, "Corrupt ZIP member"
        names = archive.namelist()
        assert len(names) == len(set(names)), "Duplicate ZIP paths"
        for name in names:
            parts = PurePosixPath(name).parts
            assert parts[0] == "style-switcher" and ".." not in parts, "Unsafe ZIP path"
        files = {name.removeprefix("style-switcher/"): archive.read(name) for name in names}
    frontmatter, body = files["SKILL.md"].decode("utf-8").removeprefix("---\n").split("\n---\n", 1)
    return yaml.safe_load(frontmatter), body, files


class SkillPackagesTest(unittest.TestCase):
    def test_workbuddy_submission_metadata(self):
        metadata, _, files = read_bundle("workbuddy")
        self.assertTrue(WORKBUDDY_FIELDS <= metadata.keys())
        for key in WORKBUDDY_FIELDS:
            self.assertIsInstance(metadata[key], str, key)
            self.assertTrue(metadata[key].strip(), key)
        self.assertEqual(metadata["name"], "style-switcher")
        self.assertRegex(metadata["version"], r"^\d+\.\d+\.\d+$")
        for language in ("zh", "en"):
            examples = metadata[f"examples_{language}"]
            self.assertEqual(len(examples), 3)
            self.assertTrue(all(isinstance(item, str) and item for item in examples))
        self.assertNotIn("agents/openai.yaml", files)

    def test_codex_standard_metadata(self):
        metadata, _, files = read_bundle("codex")
        self.assertEqual(set(metadata), {"name", "description", "metadata"})
        self.assertEqual(metadata["name"], "style-switcher")
        self.assertLessEqual(len(metadata["description"]), 1024)
        self.assertTrue(all(isinstance(value, str) for value in metadata["metadata"].values()))
        ui = yaml.safe_load(files["agents/openai.yaml"])
        self.assertIn("$style-switcher", ui["interface"]["default_prompt"])
        self.assertTrue(25 <= len(ui["interface"]["short_description"]) <= 64)

    def test_complete_self_contained_profiles(self):
        for platform in ("workbuddy", "codex"):
            with self.subTest(platform=platform):
                _, body, files = read_bundle(platform)
                profiles = {Path(name).stem for name in files if name.startswith("references/")}
                self.assertEqual(profiles, STYLES)
                links = re.findall(r"references/[a-z-]+\.md", body)
                self.assertEqual(set(links), {f"references/{style}.md" for style in STYLES})
                self.assertTrue(all(link in files for link in links))
                self.assertFalse(any(name.startswith(("scripts/", "templates/")) for name in files))
                self.assertFalse(any(Path(name).suffix in {".py", ".js", ".sh", ".env"} for name in files))

    def test_platforms_share_identical_behavior(self):
        _, workbuddy_body, workbuddy_files = read_bundle("workbuddy")
        _, codex_body, codex_files = read_bundle("codex")
        self.assertEqual(workbuddy_body, codex_body)
        for style in STYLES:
            key = f"references/{style}.md"
            self.assertEqual(workbuddy_files[key], codex_files[key])


if __name__ == "__main__":
    unittest.main()
