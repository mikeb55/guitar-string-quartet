#!/usr/bin/env python3
"""
Automatic Composition File Organiser

Moves composition files into correct folders by type.
Never deletes files. Uncertain items go to archive/.

Usage: py scripts/organise-compositions.py
       (run from workspace root)
"""
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Workspace root (parent of scripts/)
WORKSPACE = Path(__file__).resolve().parent.parent
COMPOSITIONS = WORKSPACE / "compositions"

# Folders to skip (templates, index, duplicates)
SKIP_FOLDERS = {"composition-template", ".git"}
# Skip folders containing " - Copy" (duplicate folders)
SKIP_FILES = {"_index.md"}

# File type → subfolder mapping
FILE_TYPE_MAP = {
    ".musicxml": "musicxml",
    ".xml": "musicxml",
    ".sib": "sibelius",
    ".mp4": "video",
    ".mov": "video",
    ".wmv": "video",
    ".wav": "audio",
    ".mp3": "audio",
    ".flac": "audio",
    ".aif": "audio",
    ".aiff": "audio",
    ".pdf": "pdf",
    ".mid": "sketches",
    ".midi": "sketches",
    ".txt": "sketches",
}

# Subfolders each composition folder should have
REQUIRED_SUBFOLDERS = [
    "musicxml", "sibelius", "video", "audio", "pdf", "sketches", "archive"
]

# Markdown files that stay in composition root (not moved)
ROOT_MD_FILES = {"README.md", "notes.md", "lead-sheet.md", "arrangement-plan.md", "revisions.md"}


def normalise_piece_name(filename: str) -> str:
    """
    Extract base composition name from filename.
    glass_engine_guitar_string_quartet_v3_gce9.musicxml → glass-engine
    drift_study_no1_v2.musicxml → drift-study-no1
    """
    name = Path(filename).stem  # remove extension
    name = name.lower()

    # Remove version patterns: v1, v2, v3, V1, V2, V3, v01, v02, etc.
    name = re.sub(r"\bv\d+\b", "", name, flags=re.I)
    name = re.sub(r"\bV\d+\b", "", name)

    # Remove GCE scores: gce9, gce8, gce_9, etc.
    name = re.sub(r"\bgce\d*\b", "", name, flags=re.I)

    # Remove copy, regenerated
    name = re.sub(r"\bcopy\b", "", name, flags=re.I)
    name = re.sub(r"\bregenerated\b", "", name, flags=re.I)
    name = re.sub(r"\bfixed\b", "", name, flags=re.I)

    # Remove instrument labels
    name = re.sub(r"\bguitar_string_quartet\b", "", name, flags=re.I)
    name = re.sub(r"\bguitar\b", "", name, flags=re.I)
    name = re.sub(r"\bstring_quartet\b", "", name, flags=re.I)
    name = re.sub(r"\bquartet\b", "", name, flags=re.I)

    # Clean up: collapse underscores/hyphens, trim
    name = re.sub(r"[_\s]+", "-", name)
    name = re.sub(r"-+", "-", name)  # collapse multiple hyphens
    name = name.strip("-").strip()

    if not name:
        return None
    return name


def get_target_subfolder(filepath: Path):
    """Return target subfolder for file type, or None if not a composition asset."""
    suffix = filepath.suffix.lower()
    return FILE_TYPE_MAP.get(suffix)


def ensure_composition_structure(piece_folder: Path) -> None:
    """Create composition folder and required subfolders if missing."""
    piece_folder.mkdir(parents=True, exist_ok=True)
    for sub in REQUIRED_SUBFOLDERS:
        (piece_folder / sub).mkdir(exist_ok=True)


def log_archive_in_readme(piece_folder: Path, filename: str, reason: str = "uncertain placement") -> None:
    """Append archive note to composition README.md."""
    readme = piece_folder / "README.md"
    note = f"- **Archived:** {filename} ({reason}) — {datetime.now().strftime('%Y-%m-%d')}\n"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        if "## Archive Log" not in content:
            content += "\n\n## Archive Log\n\n"
        if filename not in content:
            content += note
            readme.write_text(content, encoding="utf-8")
    else:
        readme.write_text(f"# {piece_folder.name}\n\n## Archive Log\n\n{note}", encoding="utf-8")


def get_latest_version(files: list[Path]) -> str:
    """Infer latest version from filenames (V7 > V6 > v3_gce9 > v2, etc.)."""
    if not files:
        return ""
    best = ""
    best_score = -1

    for f in files:
        name = f.stem.upper()
        score = 0
        # Prefer higher V numbers
        v_match = re.search(r"V(\d+)", name)
        if v_match:
            score = 1000 + int(v_match.group(1))
        # Then gce
        if "GCE" in name:
            gce_match = re.search(r"GCE(\d*)", name)
            score = max(score, 500 + (int(gce_match.group(1)) if gce_match and gce_match.group(1) else 9))
        # Then v numbers
        v_match = re.search(r"[_\s]V(\d+)", name, re.I)
        if v_match:
            score = max(score, 100 + int(v_match.group(1)))
        if score > best_score:
            best_score = score
            best = f.name
    return best or files[0].name


def scan_composition_assets() -> dict[str, dict]:
    """
    Scan all composition folders and collect asset info.
    Returns: {piece_name: {assets: {type: [files]}, latest: str, title: str}}
    """
    index = defaultdict(lambda: {"assets": defaultdict(list), "latest": "", "title": ""})

    for item in COMPOSITIONS.iterdir():
        if not item.is_dir() or item.name in SKIP_FOLDERS or item.name.startswith("."):
            continue
        if " - Copy" in item.name:
            continue

        piece_name = item.name
        # Human-readable title from folder name
        title = piece_name.replace("-", " ").title()
        if piece_name == "working-title-01":
            title = "working-title-01"
        elif piece_name == "composition-template":
            continue

        for sub in ["musicxml", "sibelius", "video", "audio", "pdf", "sketches", "archive"]:
            subpath = item / sub
            if subpath.is_dir():
                for f in subpath.iterdir():
                    if f.is_file() and f.suffix.lower() in {
                        ".musicxml", ".xml", ".sib", ".mp4", ".mov", ".wmv",
                        ".wav", ".mp3", ".flac", ".pdf", ".mid", ".midi"
                    }:
                        index[piece_name]["assets"][sub].append(f)
                        index[piece_name]["title"] = title

        # Compute latest per type
        for asset_type, files in index[piece_name]["assets"].items():
            if files and asset_type in ["musicxml", "sibelius"]:
                latest = get_latest_version(files)
                if latest and (not index[piece_name]["latest"] or asset_type == "musicxml"):
                    index[piece_name]["latest"] = latest

    return dict(index)


def move_loose_files() -> list[tuple[Path, Path, str]]:
    """
    Find files in compositions/ root and move to correct folders.
    Returns list of (src, dst, piece_name) for logging.
    """
    moved = []
    for item in COMPOSITIONS.iterdir():
        if not item.is_file():
            continue
        if item.name in SKIP_FILES or item.name.endswith(".md"):
            continue

        subfolder = get_target_subfolder(item)
        if not subfolder:
            # Unknown type → archive with piece name "unknown" or try to infer
            piece_name = normalise_piece_name(item.name)
            if not piece_name:
                piece_name = "unknown"
            target_folder = COMPOSITIONS / piece_name / "archive"
            ensure_composition_structure(COMPOSITIONS / piece_name)
            dst = target_folder / item.name
            try:
                if dst.exists():
                    if not item.samefile(dst):
                        print(f"  Skip {item.name}: destination exists")
                else:
                    shutil.move(str(item), str(dst))
                    moved.append((item, dst, piece_name))
                    log_archive_in_readme(COMPOSITIONS / piece_name, item.name, "unknown file type")
            except Exception as e:
                print(f"  Warning: could not move {item.name}: {e}")
            continue

        piece_name = normalise_piece_name(item.name)
        if not piece_name:
            piece_name = "unknown"
        target_folder = COMPOSITIONS / piece_name / subfolder
        ensure_composition_structure(COMPOSITIONS / piece_name)
        dst = target_folder / item.name
        try:
            if dst.exists():
                if not item.samefile(dst):
                    print(f"  Skip {item.name}: destination exists")
            else:
                shutil.move(str(item), str(dst))
                moved.append((item, dst, piece_name))
        except Exception as e:
            print(f"  Warning: could not move {item.name}: {e}")

    return moved


def update_index() -> None:
    """Update compositions/_index.md with current asset info."""
    data = scan_composition_assets()

    lines = [
        "# Compositions Index",
        "",
        "## Composition Logic",
        "",
        "**Guitar-first rule applies:** Generate guitar harmonic material first; build strings around it. See `rules/guitar-first-composition-rule.md`.",
        "",
        "## Adding a New Composition",
        "",
        "1. **Copy the template**",
        "   - Copy the entire `composition-template/` folder",
        "   - Paste into `compositions/` with the new composition's title as folder name",
        "   - Use lowercase, hyphenated names (e.g. `mist-over-still-waters`)",
        "",
        "2. **Update README.md**",
        "   - Replace placeholder with composition-specific description",
        "   - Add key, tempo, form overview",
        "",
        "3. **Develop the composition**",
        "   - `notes.md` — Ideas, sketches, development notes",
        "   - `lead-sheet.md` — Melody, chords, form",
        "   - `arrangement-plan.md` — Texture, roles, orchestration (use `prompts/arrangement-template.md`)",
        "",
        "4. **Generate MusicXML**",
        "   - Use `prompts/musicxml-generation-template.md`",
        "   - Output to `[composition-folder]/musicxml/[title]_v01.musicxml`",
        "",
        "5. **Revise**",
        "   - Apply GCE rubric (`rules/gce-rubric.md`)",
        "   - Use `prompts/revision-template.md`",
        "   - Log changes in `revisions.md`",
        "",
        "6. **Export**",
        "   - PDF to `pdf/`",
        "   - Audio to `audio/`",
        "   - Video to `video/`",
        "",
        "## Target Folder Structure (per composition)",
        "",
        "```",
        "<piece-folder>/",
        "  README.md",
        "  notes.md",
        "  lead-sheet.md",
        "  arrangement-plan.md",
        "  revisions.md",
        "  musicxml/",
        "  sibelius/",
        "  video/",
        "  pdf/",
        "  audio/",
        "  sketches/",
        "  archive/",
        "```",
        "",
        "## Active Compositions",
        "",
        "| Folder | Title | Asset Types | Latest Version | Notes |",
        "|--------|-------|-------------|----------------|-------|",
    ]

    # Add composition-template and working-title-01 if not in data
    for folder, title in [
        ("composition-template", "(template)"),
        ("working-title-01", "working-title-01"),
    ]:
        if folder not in data:
            data[folder] = {"assets": {}, "latest": "—", "title": title}

    # Sort: composition-template last, working-title-01, then alphabetically
    def sort_key(k):
        if k == "composition-template":
            return (2, k)
        if k == "working-title-01":
            return (1, k)
        return (0, k)

    for piece_name in sorted(data.keys(), key=sort_key):
        info = data[piece_name]
        if piece_name == "composition-template":
            lines.append(f"| {piece_name} | (template) | — | — | Do not use for real compositions |")
            continue

        asset_types = " ".join(sorted(info["assets"].keys())) if info["assets"] else "—"
        latest = info["latest"] or "—"
        notes = ""
        if info["assets"].get("archive"):
            notes = "Some files in archive"
        lines.append(f"| {piece_name} | {info['title']} | {asset_types} | {latest} | {notes} |")

    lines.extend([
        "",
        "## TODO",
        "",
        "— **Save new files directly into the correct composition folder** — When generating MusicXML, Sibelius exports, or video, save into `compositions/[piece-name]/musicxml/`, `sibelius/`, or `video/` rather than the compositions root.",
        "",
        "— **Run organiser:** `py scripts/organise-compositions.py` to move loose files into correct folders.",
        "",
    ])

    index_path = COMPOSITIONS / "_index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    os.chdir(WORKSPACE)
    print("Composition File Organiser")
    print("=" * 40)

    moved = move_loose_files()
    if moved:
        print("Moved files:")
        for src, dst, piece in moved:
            print(f"  {src.name} -> {piece}/{dst.parent.name}/")
    else:
        print("No loose files to move.")

    update_index()
    print("Updated compositions/_index.md")


if __name__ == "__main__":
    main()
