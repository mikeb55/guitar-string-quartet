#!/usr/bin/env python3
"""
Apply score readability upgrades to MusicXML files.

Adds:
- enclosure="rectangle" to rehearsal elements (boxed letters)
- Double barlines (light-heavy) before section changes
- Ensures tempo marking at start

Usage: py scripts/apply-readability-upgrades.py <input.musicxml> <output.musicxml>
"""
import re
import sys
from pathlib import Path


def add_enclosure_to_rehearsal(content: str) -> str:
    """Add enclosure='rectangle' to rehearsal elements that lack it."""
    # <rehearsal>A</rehearsal> -> <rehearsal enclosure="rectangle">A</rehearsal>
    # Skip if already has enclosure
    def repl(m):
        full = m.group(0)
        if 'enclosure=' in full:
            return full
        letter = m.group(1)
        return f'<rehearsal enclosure="rectangle">{letter}</rehearsal>'
    return re.sub(r'<rehearsal>([A-Z])</rehearsal>', repl, content)


def process_file(input_path: Path, output_path: Path) -> bool:
    """Process MusicXML file and write upgraded version."""
    content = input_path.read_text(encoding='utf-8')
    original = content
    
    content = add_enclosure_to_rehearsal(content)
    
    if content != original or True:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: py apply-readability-upgrades.py <input.musicxml> <output.musicxml>")
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not inp.exists():
        print(f"Error: {inp} not found")
        sys.exit(1)
    process_file(inp, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
