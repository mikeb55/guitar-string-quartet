#!/usr/bin/env python3
"""
Generate Jimmy Wyble-style arrangements for all 9 album pieces.
Run: py scripts/generate_all_wyble_arrangements.py
"""
import sys
from pathlib import Path

# Add project root
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    harmony, expressions, dynamics
)
from music21.instrument import Guitar, Violin, Viola, Violoncello

COMPOSITIONS = BASE / "compositions"

CONFIGS = {
    "home-engine": {"title": "Home Engine (Wyble)", "source": "V9_Home_Engine_Scofield.musicxml",
        "key": -1, "tempo": 104, "time": (4, 4), "chord": "Dm9", "root": "D"},
    "sylva-narrative": {"title": "Sylva Narrative (Wyble)", "source": "V7_Sylva_Narrative_New_Intro.musicxml",
        "key": 2, "tempo": 72, "time": (5, 4), "chord": "Amaj7", "root": "A"},
    "northern-letters": {"title": "Northern Letters (Wyble)", "source": "V2_Northern_Letters_Final.musicxml",
        "key": 0, "tempo": 88, "time": (4, 4), "chord": "Cmaj7", "root": "C"},
    "glass-engine": {"title": "Glass Engine (Wyble)", "source": "V9_Glass_Engine_Atmospheric_Master.musicxml",
        "key": 0, "tempo": 66, "time": (4, 4), "chord": "Dm", "root": "D"},
    "eviscerating-angels": {"title": "Eviscerating Angels (Wyble)", "source": "V5_Eviscerating_Angels_Final.musicxml",
        "key": -1, "tempo": 76, "time": (5, 4), "chord": "Am", "root": "A"},
    "myrtles-prayer": {"title": "Myrtle's Prayer (Wyble)", "source": "V5_Myrtles_Prayer_Final.musicxml",
        "key": -1, "tempo": 84, "time": (4, 4), "chord": "Dm9", "root": "D"},
    "shifting-frames": {"title": "Shifting Frames (Wyble)", "source": "V2_Shifting_Frames_Final.musicxml",
        "key": 0, "tempo": 104, "time": (4, 4), "chord": "Cmaj7", "root": "C"},
    "labyrinth-of-quiet-motions": {"title": "Labyrinth of Quiet Motions (Wyble)", "source": "V3_Labyrinth_of_Quiet_Motions_Master.musicxml",
        "key": 0, "tempo": 78, "time": (4, 4), "chord": "Em", "root": "E"},
    "long-echo": {"title": "Long Echo (Wyble)", "source": "V2_Long_Echo_Final.musicxml",
        "key": 0, "tempo": 52, "time": (4, 4), "chord": "D", "root": "D"},
}


def n(pitch, dur=1.0):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    return x


def r(dur=1.0):
    return note.Rest(duration=duration.Duration(dur))


def wyble_pattern(bar, chord_sym, root):
    """Generic Wyble two-line pattern: dyads and single lines."""
    patterns = [
        [(chord_sym, 0.5, f"{root}4", f"{root}3"), (chord_sym, 1.5, None, None)],
        [(chord_sym, 0.5, None, f"{root}2"), (chord_sym, 1.0, f"{root}4", f"{root}3"), (chord_sym, 2.5, None, None)],
        [(chord_sym, 1.0, f"{root}4", f"{root}3"), (chord_sym, 3.0, None, None)],
        [(chord_sym, 0.5, None, f"{root}2"), (chord_sym, 0.5, f"{root}4", None), (chord_sym, 3.0, None, None)],
    ]
    return patterns[bar % 4]


def generate(slug, cfg):
    out_dir = COMPOSITIONS / slug / "wyble-arrangement" / "musicxml"
    out_dir.mkdir(parents=True, exist_ok=True)

    num, den = cfg["time"]
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = cfg["title"]
    s.metadata.composer = "Mike Bryant"

    parts = {}
    for name, inst, pname in [
        ("gtr", Guitar, "Guitar"), ("vn1", Violin, "Violin I"), ("vn2", Violin, "Violin II"),
        ("vla", Viola, "Viola"), ("vc", Violoncello, "Cello"),
    ]:
        p = stream.Part()
        p.partName = pname
        p.insert(0, inst())
        parts[name] = p

    num_bars = 16
    chord_sym = cfg["chord"]
    root = cfg["root"]
    if root == "A": root = "A"
    elif root == "C": root = "C"
    elif root == "D": root = "D"
    elif root == "E": root = "E"

    for m_num in range(1, num_bars + 1):
        mg = stream.Measure(number=m_num)
        mg.timeSignature = meter.TimeSignature(f"{num}/{den}")
        if m_num == 1:
            mg.insert(0, key.KeySignature(cfg["key"]))
            mg.insert(0, tempo.MetronomeMark(number=cfg["tempo"], referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mp"))
            mg.insert(0, expressions.RehearsalMark("A"))
        if m_num == 9:
            mg.insert(0, expressions.RehearsalMark("B"))

        mg.insert(0, harmony.ChordSymbol(chord_sym))
        for sym, dur, up, lo in wyble_pattern(m_num - 1, chord_sym, root):
            if up and lo:
                c = chord.Chord([up, lo])
                c.duration = duration.Duration(dur)
                mg.append(c)
            elif up:
                mg.append(n(up, dur))
            elif lo:
                mg.append(n(lo, dur))
            else:
                mg.append(r(dur))
        parts["gtr"].append(mg)

        for pname in ["vn1", "vn2", "vla"]:
            mx = stream.Measure(number=m_num)
            mx.timeSignature = meter.TimeSignature(f"{num}/{den}")
            mx.append(r(num))
            parts[pname].append(mx)

        mvc = stream.Measure(number=m_num)
        mvc.timeSignature = meter.TimeSignature(f"{num}/{den}")
        mvc.append(n(f"{root}2", 2))
        mvc.append(r(num - 2) if num > 2 else r(2))
        parts["vc"].append(mvc)

    for p in parts.values():
        s.append(p)

    out_path = out_dir / f"Wyble_{cfg['source']}"
    s.write("musicxml", fp=out_path)
    print(f"Generated: {out_path}")
    return out_path


def main():
    for slug, cfg in CONFIGS.items():
        generate(slug, cfg)
    print("All Wyble arrangements generated.")


if __name__ == "__main__":
    main()
