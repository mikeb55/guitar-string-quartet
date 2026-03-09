#!/usr/bin/env python3
"""
Remove redundant time/key/divisions from MusicXML.
- Time signature: only in measure 1 of first part (or when meter changes).
- Key signature: only in measure 1 of first part (or when key changes).
- Divisions: only in measure 1 of each part (required for partwise).
"""
import re
import sys
from pathlib import Path

def fix_musicxml(in_path: Path, out_path: Path) -> None:
    with open(in_path, encoding="utf-8") as f:
        content = f.read()

    # Pattern 1: attributes block containing ONLY time (5/4) - measures 2+ in all parts
    # First part m1 has divisions+key+time, so this won't match it.
    time_only_block = re.compile(
        r'\n\s+<attributes>\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+</attributes>',
        re.MULTILINE
    )

    # Pattern 2: attributes with divisions+time (parts 2-5 measure 1) - remove time, keep divisions
    divisions_plus_time = re.compile(
        r'(<attributes>\s*\n\s+<divisions>\d+</divisions>)\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+(</attributes>)',
        re.MULTILINE
    )

    # Remove time-only blocks (redundant in every measure 2+)
    result = time_only_block.sub('', content)

    # In parts 2-5 measure 1: replace divisions+time with divisions only
    result = divisions_plus_time.sub(r'\1\n      \2', result)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Written: {out_path}")

if __name__ == "__main__":
    base = Path(__file__).parent / "musicxml"
    # Prefer V2 if present; otherwise use base Sylva_Narrative_No2
    src = base / "V2Sylva_Narrative_No2.musicxml"
    if not src.exists():
        src = base / "Sylva_Narrative_No2.musicxml"
    dst = base / "V3Sylva_Narrative_No2.musicxml"
    if len(sys.argv) >= 2:
        src = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        dst = Path(sys.argv[2])
    fix_musicxml(src, dst)
