#!/usr/bin/env python3
"""
Generate Wyble arrangement for Myrtle's Prayer.
Output: compositions/myrtles-prayer/Wyble_Arrangement/
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from music21 import converter
from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    harmony, expressions, dynamics
)
from music21.instrument import Guitar, Violin, Viola, Violoncello

SOURCE = BASE / "compositions/myrtles-prayer/musicxml/V5_Myrtles_Prayer_Final.musicxml"
OUT_DIR = BASE / "compositions/myrtles-prayer/Wyble_Arrangement/musicxml"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Dm9: D F A C E  |  Gm9: G Bb D F A
# Wyble dyads: upper (3rd/7th/9th) + lower (root/5th)
DIV = 10080  # quarter
HALF = 20160
WHOLE = 40320


def n(pitch, dur=1.0):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    return x


def r(dur=1.0):
    return note.Rest(duration=duration.Duration(dur))


def dyad(up, lo, dur):
    c = chord.Chord([up, lo])
    c.duration = duration.Duration(dur)
    return c


# Per-chord Wyble dyads: (upper, lower) for Dm9 and Gm9
# Contrary/oblique motion; avoid block chords
Dm9_dyads = [
    ("F4", "D3"),   # 3rd + root
    ("E4", "A3"),   # 9th + 5th
    ("C4", "D3"),   # 7th + root
    ("F4", "A3"),   # 3rd + 5th
]
Gm9_dyads = [
    ("Bb4", "G3"),
    ("A4", "D4"),
    ("F4", "G3"),
    ("Bb4", "D4"),
]


def get_chord_for_measure(score, m_num):
    gtr_part = score.parts[0]
    measures = list(gtr_part.getElementsByClass(stream.Measure))
    if m_num > len(measures):
        return None
    m = measures[m_num - 1]
    h = m.getElementsByClass(harmony.ChordSymbol)
    return h[0].figure if h else None


def wyble_guitar_measure(m_num, chord_sym, bar_idx, has_rehearsal, reh_letter, dyn):
    """Create one measure of Wyble two-line guitar."""
    mg = stream.Measure(number=m_num)
    if m_num == 1:
        mg.timeSignature = meter.TimeSignature("4/4")
        mg.insert(0, key.KeySignature(-1))
        mg.insert(0, tempo.MetronomeMark(number=84, referent=note.Note(type='quarter')))
    if has_rehearsal:
        mg.insert(0, expressions.RehearsalMark(reh_letter))
    if dyn:
        mg.insert(0, dynamics.Dynamic(dyn))

    if not chord_sym:
        mg.append(r(4))
        return mg

    if "Dm9" in chord_sym or chord_sym == "Dm9":
        pairs = Dm9_dyads
    elif "Gm9" in chord_sym or chord_sym == "Gm9":
        pairs = Gm9_dyads
    else:
        pairs = Dm9_dyads

    up, lo = pairs[bar_idx % 4]
    # Wyble: sparse - dyad on beat 1, rest or single line
    mg.insert(0, harmony.ChordSymbol(chord_sym))
    mg.append(dyad(up, lo, 1.0))
    mg.append(r(1.0))
    mg.append(n(up, 0.5))
    mg.append(n(lo, 0.5))
    mg.append(r(1.0))
    return mg


def string_measure(m_num, part_name, chord_sym, bar_idx):
    """Light string support: sustained or sparse."""
    mx = stream.Measure(number=m_num)
    if m_num == 1:
        mx.timeSignature = meter.TimeSignature("4/4")
    if chord_sym and "Dm9" in chord_sym:
        root, fifth = "D", "A"
    elif chord_sym and "Gm9" in chord_sym:
        root, fifth = "G", "D"
    else:
        root, fifth = "D", "A"

    if part_name == "Cello":
        mx.append(n(f"{root}2", 2))
        mx.append(r(2))
    elif part_name in ("Viola", "Violin II"):
        if bar_idx % 2 == 0 and chord_sym:
            mx.append(n(f"{fifth}3", 4))
        else:
            mx.append(r(4))
    else:
        mx.append(r(4))
    return mx


def main():
    score = converter.parse(str(SOURCE))
    measures = list(score.parts[0].getElementsByClass(stream.Measure))
    num_measures = len(measures)

    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Myrtle's Prayer (Wyble Arrangement)"
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

    for m_num in range(1, num_measures + 1):
        chord_sym = get_chord_for_measure(score, m_num)
        bar_idx = m_num - 1

        has_reh = False
        reh_letter = None
        dyn = None
        src_m = measures[m_num - 1]
        for rn in src_m.getElementsByClass(expressions.RehearsalMark):
            c = rn.content
            if c in ("A", "B", "C"):
                has_reh = True
                reh_letter = c
        for d in src_m.getElementsByClass(dynamics.Dynamic):
            dyn = str(d.value)

        mg = wyble_guitar_measure(m_num, chord_sym, bar_idx, has_reh, reh_letter, dyn)
        parts["gtr"].append(mg)

        for pkey, pname in [("vn1", "Violin I"), ("vn2", "Violin II"), ("vla", "Viola"), ("vc", "Cello")]:
            mx = string_measure(m_num, pname, chord_sym, bar_idx)
            parts[pkey].append(mx)

    for p in parts.values():
        s.append(p)

    out_path = OUT_DIR / "Wyble_V5_Myrtles_Prayer_Final.musicxml"
    s.write("musicxml", fp=out_path)
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    main()
