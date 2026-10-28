"""Build WorkBuddy and Codex packages from the same style-switcher instructions."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "style-switcher"
DIST = ROOT / "dist"


def build():
    """Validate submission metadata and write both platform bundles."""
    source_text = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    if not source_text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    frontmatter, body = source_text[4:].split("\n---\n", 1)
    metadata = yaml.safe_load(frontmatter)
    required = (
        "name", "display_name", "display_name_en", "description",
        "description_zh", "description_en", "version", "author",
    )
    for key in required:
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f"Missing or invalid WorkBuddy field: {key}")
    if metadata["name"] != SOURCE.name:
        raise ValueError("Skill name and directory must match")

    profiles = sorted((SOURCE / "references").glob("*.md"))
    if len(profiles) != 10:
        raise ValueError("Expected exactly ten style profiles")
    common = {path.relative_to(SOURCE).as_posix(): path.read_bytes() for path in profiles}
    codex_metadata = {
        "name": metadata["name"],
        "description": metadata["description"],
        "metadata": {"author": metadata["author"], "version": metadata["version"]},
    }
    codex_text = "---\n" + yaml.safe_dump(codex_metadata, allow_unicode=True, sort_keys=False, width=1000) + "---\n" + body
    bundles = {
        "workbuddy": {"SKILL.md": source_text.encode("utf-8"), **common},
        "codex": {
            "SKILL.md": codex_text.encode("utf-8"),
            **common,
            "agents/openai.yaml": (SOURCE / "agents/openai.yaml").read_bytes(),
        },
    }
    DIST.mkdir(exist_ok=True)
    for platform, files in bundles.items():
        # Stable timestamps and ordering make repeated builds byte-identical.
        archive_path = DIST / f"style-switcher-{platform}.zip"
        with ZipFile(archive_path, "w") as archive:
            for name, content in sorted(files.items()):
                info = ZipInfo(f"style-switcher/{name}")
                info.compress_type = ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
                if platform == "codex":
                    target = DIST / "codex" / "style-switcher" / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
        print(f"{archive_path.name}: {len(files)} files, {archive_path.stat().st_size} bytes")


if __name__ == "__main__":
    build()
