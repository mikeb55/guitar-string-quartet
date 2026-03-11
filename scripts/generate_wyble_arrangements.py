#!/usr/bin/env python3
"""
Generate Jimmy Wyble-style alternate arrangements for the guitar + string quartet album.

Wyble principle: Guitar becomes a two-line contrapuntal engine.
- Independent upper and lower voices
- Contrary motion, oblique motion, parallel 3rds/6ths
- Dyadic harmony, implied harmony from line interaction
- No dense comping, no stacked jazz chords

Output: compositions/<slug>/wyble-arrangement/musicxml/Wyble_<source>.musicxml
"""
import os
from pathlib import Path

try:
    from music21 import (
        stream, note, chord, duration, tempo, key, metadata, meter,
        harmony, expressions, dynamics, layout
    )
    from music21.instrument import Guitar, Violin, Viola, Violoncello
except ImportError:
    print("music21 required: pip install music21")
    raise

BASE = Path(__file__).resolve().parent.parent
COMPOSITIONS = BASE / "compositions"


def n(pitch, dur=1.0):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    return x


def r(dur=1.0):
    x = note.Rest()
    x.duration = duration.Duration(dur)
    return x


def two_voice(upper, lower, dur=1.0):
    """Create two independent guitar voices (Wyble style)."""
    u = n(upper, dur) if upper else r(dur)
    l = n(lower, dur) if lower else r(dur)
    u.offset = 0
    l.offset = 0
    return u, l


def make_score(title, composer="Mike Bryant"):
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = title
    s.metadata.composer = composer
    return s


# === PIECE DEFINITIONS ===
# Each piece: key, tempo, time_sig, sections, harmony_map, wyble_upper/lower generators

PIECES = {
    "home-engine": {
        "title": "Home Engine (Wyble)",
        "source": "V9_Home_Engine_Scofield.musicxml",
        "key": "D",
        "mode": "minor",
        "tempo": 104,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Dm9"),
            ("B", 8, "Dm9"),
            ("C", 8, "Dm9"),
            ("D", 4, "Dm9"),
            ("Coda", 4, "Dm9"),
        ],
    },
    "sylva-narrative": {
        "title": "Sylva Narrative (Wyble)",
        "source": "V7_Sylva_Narrative_New_Intro.musicxml",
        "key": "A",
        "mode": "major",
        "tempo": 72,
        "time": (5, 4),
        "sections": [
            ("A", 8, "Amaj7"),
            ("B", 8, "Amaj7"),
            ("C", 8, "Dmaj7"),
            ("D", 4, "Amaj7"),
        ],
    },
    "northern-letters": {
        "title": "Northern Letters (Wyble)",
        "source": "V2_Northern_Letters_Final.musicxml",
        "key": "C",
        "mode": "major",
        "tempo": 88,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Cmaj7"),
            ("B", 8, "Cmaj7"),
            ("C", 8, "Fmaj7"),
            ("D", 4, "Cmaj7"),
        ],
    },
    "glass-engine": {
        "title": "Glass Engine (Wyble)",
        "source": "V9_Glass_Engine_Atmospheric_Master.musicxml",
        "key": "D",
        "mode": "minor",
        "tempo": 66,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Dm"),
            ("B", 8, "Fm"),
            ("C", 8, "Dm"),
            ("D", 4, "Dm"),
        ],
    },
    "eviscerating-angels": {
        "title": "Eviscerating Angels (Wyble)",
        "source": "V5_Eviscerating_Angels_Final.musicxml",
        "key": "A",
        "mode": "minor",
        "tempo": 76,
        "time": (5, 4),
        "sections": [
            ("A", 8, "Am"),
            ("B", 8, "Am"),
            ("C", 8, "Am"),
            ("D", 4, "Am"),
        ],
    },
    "myrtles-prayer": {
        "title": "Myrtle's Prayer (Wyble)",
        "source": "V5_Myrtles_Prayer_Final.musicxml",
        "key": "D",
        "mode": "minor",
        "tempo": 84,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Dm9"),
            ("B", 8, "Dm9"),
            ("C", 8, "Dm9"),
            ("D", 4, "Dm9"),
        ],
    },
    "shifting-frames": {
        "title": "Shifting Frames (Wyble)",
        "source": "V2_Shifting_Frames_Final.musicxml",
        "key": "C",
        "mode": "major",
        "tempo": 104,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Cmaj7"),
            ("B", 8, "Dm7"),
            ("C", 8, "Cmaj7"),
            ("D", 4, "Cmaj7"),
        ],
    },
    "labyrinth-of-quiet-motions": {
        "title": "Labyrinth of Quiet Motions (Wyble)",
        "source": "V3_Labyrinth_of_Quiet_Motions_Master.musicxml",
        "key": "C",
        "mode": "major",
        "tempo": 78,
        "time": (4, 4),
        "sections": [
            ("A", 8, "Em"),
            ("B", 8, "Am"),
            ("C", 8, "Em"),
            ("D", 4, "C"),
        ],
    },
    "long-echo": {
        "title": "Long Echo (Wyble)",
        "source": "V2_Long_Echo_Final.musicxml",
        "key": "C",
        "mode": "major",
        "tempo": 52,
        "time": (4, 4),
        "sections": [
            ("A", 8, "D"),
            ("B", 8, "E"),
            ("C", 8, "D"),
            ("D", 4, "D"),
        ],
    },
}


def wyble_two_lines(bar, section, chord_sym, key_root, mode):
    """
    Generate Wyble-style two-line guitar: upper and lower voices.
    Contrary motion, oblique motion, dyadic implication.
    """
    # Map chord to scale tones (simplified)
    upper = None
    lower = None
    if mode == "minor":
        # Dm: upper = 3rd, 7th, 9th; lower = root, 5th
        if "D" in chord_sym or "Dm" in chord_sym:
            if bar % 4 == 0: upper, lower = "F4", "D3"
            elif bar % 4 == 1: upper, lower = "C4", "A3"
            elif bar % 4 == 2: upper, lower = "E4", "D3"
            else: upper, lower = "A4", "C4"
        elif "A" in chord_sym or "Am" in chord_sym:
            if bar % 4 == 0: upper, lower = "C4", "A2"
            elif bar % 4 == 1: upper, lower = "G4", "E3"
            else: upper, lower = "B4", "A3"
        elif "F" in chord_sym or "Fm" in chord_sym:
            if bar % 4 == 0: upper, lower = "Ab4", "F3"
            else: upper, lower = "Eb4", "C3"
        elif "E" in chord_sym or "Em" in chord_sym:
            upper, lower = "G4", "E3"
        else:
            upper, lower = "C4", "A3"
    else:
        # Major
        if "C" in chord_sym or "Cmaj" in chord_sym:
            if bar % 4 == 0: upper, lower = "E4", "C3"
            elif bar % 4 == 1: upper, lower = "B4", "G3"
            else: upper, lower = "G4", "E3"
        elif "A" in chord_sym or "Amaj" in chord_sym:
            if bar % 4 == 0: upper, lower = "C#4", "A2"
            else: upper, lower = "G#4", "E3"
        elif "D" in chord_sym or "Dmaj" in chord_sym:
            upper, lower = "F#4", "D3"
        elif "F" in chord_sym or "Fmaj" in chord_sym:
            upper, lower = "A4", "F3"
        else:
            upper, lower = "E4", "C3"
    return upper, lower


def generate_wyble_arrangement(slug, spec):
    """Generate Wyble arrangement for one piece."""
    out_dir = COMPOSITIONS / slug / "wyble-arrangement" / "musicxml"
    out_dir.mkdir(parents=True, exist_ok=True)

    score = make_score(spec["title"])
    num, den = spec["time"]
    ts = meter.TimeSignature(f"{num}/{den}")
    k = key.Key(spec["key"], spec["mode"])
    t = tempo.MetronomeMark(number=spec["tempo"])

    # Guitar part with two voices
    guitar = stream.Part()
    guitar.insert(0, Guitar())
    guitar.insert(0, ts)
    guitar.insert(0, k)
    guitar.insert(0, t)

    # String parts (simplified: sustained pads)
    vln1 = stream.Part()
    vln1.insert(0, Violin())
    vln1.insert(0, ts)
    vln1.insert(0, k)

    vln2 = stream.Part()
    vln2.insert(0, Violin())
    vln2.insert(0, ts)
    vln2.insert(0, k)

    viola = stream.Part()
    viola.insert(0, Viola())
    viola.insert(0, ts)
    viola.insert(0, k)

    cello = stream.Part()
    cello.insert(0, Violoncello())
    cello.insert(0, ts)
    cello.insert(0, k)

    offset = 0
    for sec_name, num_bars, chord_sym in spec["sections"]:
        for bar in range(num_bars):
            # Rehearsal at section start
            if bar == 0:
                guitar.insert(offset, expressions.RehearsalMark(sec_name))

            # Add chord symbol
            h = harmony.ChordSymbol(chord_sym)
            guitar.insert(offset, h)

            # Wyble two-line guitar
            upper, lower = wyble_two_lines(bar, sec_name, chord_sym, spec["key"], spec["mode"])
            dur = num  # quarter = 1 beat
            if bar % 2 == 0:
                guitar.insert(offset, n(upper, dur) if upper else r(dur))
                guitar.insert(offset, n(lower, dur) if lower else r(dur))
            else:
                # Rest for contrast
                guitar.insert(offset, r(dur))
            offset += num

            # Strings: sparse (every 4 bars)
            if bar % 4 == 0 and bar < num_bars - 1:
                cello.insert(offset - num, n(f"{spec['key']}2", num * 2))


    score.insert(0, guitar)
    score.insert(0, vln1)
    score.insert(0, vln2)
    score.insert(0, viola)
    score.insert(0, cello)

    out_name = f"Wyble_{spec['source']}"
    out_path = out_dir / out_name
    score.write("musicxml", fp=out_path)
    print(f"Generated: {out_path}")
    return out_path


def ensure_dirs():
    """Create wyble-arrangement directory structure for all pieces."""
    for slug in PIECES:
        base = COMPOSITIONS / slug / "wyble-arrangement"
        for sub in ["musicxml", "pdf", "notes", "revisions"]:
            (base / sub).mkdir(parents=True, exist_ok=True)
        print(f"Ensured: {base}")


def main():
    ensure_dirs()
    for slug, spec in PIECES.items():
        generate_wyble_arrangement(slug, spec)
    print("Done. Wyble arrangements generated.")


if __name__ == "__main__":
    main()
