#!/usr/bin/env python3
"""
Eviscerating Angels V5 – Final
GCE 9.6+ target. Fully convincing dark narrative.

V4 → V5: Extended climax, motivic consolidation, smoother transitions,
stronger viola, textural collapse, dynamic long arc.
78 bars: A(1-18) B(19-36) C(37-60) D(61-78)
"""
import os
from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    harmony, expressions, dynamics
)
from music21.bar import Barline
from music21.instrument import Guitar, Violin, Viola, Violoncello

def n(pitch, dur=1.0):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    return x

def c(pitches, dur=1.0):
    x = chord.Chord(pitches)
    x.duration = duration.Duration(dur)
    return x

def r(dur=1.0):
    x = note.Rest()
    x.duration = duration.Duration(dur)
    return x

# Phase map: A(1-18) B(19-36) C(37-60) D(61-78) — 78 bars total
def phase(m):
    if m <= 18: return "A"
    if m <= 36: return "B"
    if m <= 60: return "C"
    return "D"

def bar_in_phase(m):
    ph = phase(m)
    if ph == "A": return m - 1
    if ph == "B": return m - 19
    if ph == "C": return m - 37
    return m - 61

def section(m):
    return phase(m)

def bar_in(m, sec):
    return bar_in_phase(m)

def chord_symbol_for(pitches):
    if not pitches or pitches == "rest":
        return None
    if isinstance(pitches, str):
        pitches = (pitches,)
    pit_str = "+".join(sorted(str(p) for p in pitches))
    if "A3" in pit_str and "E4" in pit_str: return "Am"
    if "E4" in pit_str and "B4" in pit_str: return "E5"
    if "G3" in pit_str and "D4" in pit_str: return "G"
    if "D4" in pit_str and "F#4" in pit_str: return "D5"
    if "B3" in pit_str and "D4" in pit_str: return "Bm"
    if "C#4" in pit_str and "G#4" in pit_str: return "C#m"
    return "Am"

# === CORE MOTIF: A3-E4-G4 (E5-G5-A5 in violin). Fragments: A-E, E-G ===

# === GUITAR V5: Sparse — dark dyads, punctuations, occasional motif fragment ===
def guitar_content(sec, bar, m):
    ph = phase(m)
    bar_ph = bar_in_phase(m)
    if ph == "A":
        if bar_ph in (0, 2, 5, 8, 11, 14):
            return [r(5)], None
        blocks = [("A3", "E4"), ("E4", "G4"), ("G3", "D4"), ("A3", "E4")]
        pit = blocks[bar_ph % 4]
        return [c(pit, 2.5), r(2.5)], chord_symbol_for(pit)
    if ph == "B":
        if bar_ph in (1, 4, 7, 10, 14, 17):
            return [r(5)], None
        blocks = [("E3", "B3"), ("A3", "E4"), ("D4", "F#4"), ("E4", "B4")]
        pit = blocks[bar_ph % 4]
        return [c(pit, 2), r(3)], chord_symbol_for(pit)
    if ph == "C":
        if bar_ph in (2, 5, 9, 13, 17, 20):
            return [r(5)], None
        blocks = [("A3", "E4", "G4"), ("E3", "B3", "G4"), ("D4", "F#4"), ("E4", "G#4", "B4")]
        pit = blocks[bar_ph % 4]
        if len(pit) == 3:
            return [c(pit, 2), r(1), c((pit[0], pit[1]), 2)], chord_symbol_for(pit)
        return [c(pit, 2.5), r(2.5)], chord_symbol_for(pit)
    if ph == "D":
        if bar_ph in (0, 1, 3, 5, 7, 9, 11, 13, 15, 17):
            return [r(5)], None
        if bar_ph in (2, 6, 10):
            return [c(("A3", "E4"), 2), r(3)], chord_symbol_for(("A3", "E4"))
        return [c(("G3", "D4"), 2.5), r(2.5)], chord_symbol_for(("G3", "D4"))

# === VIOLIN I: Primary motif — E5-G5-A5 clearly stated, transformations ===
def violin1_content(sec, bar, m):
    ph = phase(m)
    bar_ph = bar_in_phase(m)
    if ph == "A":
        if bar_ph in (0, 1, 3, 6, 9, 12):
            return [n("E5", 2), r(1), n("G5", 1.5), r(0.5)]
        if bar_ph in (2, 5, 8, 11):
            return [r(1), n("A5", 1), n("E5", 2), r(1)]
        if bar_ph in (4, 7, 10, 13):
            return [n("G5", 1.5), r(1), n("E5", 2), r(0.5)]
        return [r(5)]
    if ph == "B":
        if bar_ph in (0, 2, 5, 8, 11, 14):
            return [n("G5", 1), r(1), n("B5", 1.5), r(1.5)]
        if bar_ph in (3, 7, 10, 15):
            return [c(("E5", "G5"), 1), r(2), n("A5", 1.5), r(0.5)]
        if bar_ph in (4, 9, 13):
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        return [r(5)]
    if ph == "C":
        if bar_ph < 18:
            return [c(("E5", "G5", "B5"), 1), r(0.5), n("A5", 2), r(1.5)]
        if bar_ph < 22:
            return [n("B5", 0.75), n("A5", 0.75), n("G5", 0.75), n("E5", 1), r(1.75)]
        return [c(("E5", "G5"), 2), r(3)]
    if ph == "D":
        if bar_ph in (0, 6, 12):
            return [n("G5", 2.5), r(1), n("E5", 1), r(0.5)]
        if bar_ph in (3, 9):
            return [n("D5", 2), r(1), n("F#5", 1.5), r(0.5)]
        return [r(5)]
    return [r(5)]

# === VIOLIN II: Echo responses — motif fragments (E-G, G-A) ===
def violin2_content(sec, bar, m):
    ph = phase(m)
    bar_ph = bar_in_phase(m)
    if ph == "A":
        if bar_ph in (2, 5, 8, 11):
            return [r(1), n("D5", 1), r(1), n("F#5", 1.5), r(0.5)]
        if bar_ph in (4, 7, 10):
            return [n("B4", 1.5), r(3.5)]
        return [r(5)]
    if ph == "B":
        if bar_ph in (1, 4, 7, 10, 13):
            return [r(1), n("B4", 1), n("D5", 1), r(2)]
        if bar_ph in (3, 8, 12):
            return [n("G4", 1), r(2), n("B4", 1.5), r(0.5)]
        return [r(5)]
    if ph == "C":
        if bar_ph in (1, 4, 7, 10, 13, 16):
            return [n("E5", 1), r(1), n("G5", 1.5), r(1.5)]
        if bar_ph in (3, 6, 9, 12):
            return [c(("G4", "B4", "D5"), 1.5), r(3.5)]
        return [r(5)]
    if ph == "D":
        if bar_ph in (2, 8):
            return [n("E5", 1.5), r(3.5)]
        return [r(5)]
    return [r(5)]

# === VIOLA V5: Activated — contrary motion, displacement, tension resolving down ===
def viola_content(sec, bar, m, block):
    ph = phase(m)
    bar_ph = bar_in_phase(m)
    if m == 36:
        return [n("E4", 5)]
    if m == 60:
        return [n("A3", 5)]
    if ph == "A":
        lines = [
            [n("B3", 1), n("A3", 1), r(1), n("E4", 1.5), r(0.5)],
            [n("G4", 1), r(1), c(("A3", "E4"), 2), r(1)],
            [n("D4", 1), n("C4", 1), r(1), n("G4", 1.5), r(0.5)],
            [n("E4", 0.5), r(0.5), c(("G3", "B3"), 2.5), r(1.5)],
        ]
        return lines[(bar_ph + block) % 4]
    if ph == "B":
        lines = [
            [n("E4", 1), n("D4", 1), r(1), n("G#4", 1.5), r(0.5)],
            [n("A4", 1), r(1), c(("C#4", "E4"), 2), r(1)],
            [n("D4", 1), n("C4", 1), r(1), n("F#4", 1.5), r(0.5)],
            [n("G4", 1), r(1), c(("B3", "D4"), 2), r(1)],
            [r(0.5), n("C#4", 1), n("B3", 1), r(1), n("E4", 1.5)],
        ]
        return lines[(bar_ph + block) % 5]
    if ph == "C":
        lines = [
            [c(("B3", "D4", "F#4"), 1.5), r(0.5), n("E4", 1.5), r(1.5)],
            [n("C#4", 1), n("B3", 1), r(1), c(("E4", "G#4"), 1.5), r(0.5)],
            [n("D4", 1), n("C4", 1), r(1), n("G4", 2), r(1)],
            [n("G3", 1), n("A3", 1), r(1), c(("B3", "D4"), 2), r(1)],
            [r(1), n("F#4", 0.75), n("E4", 0.75), n("D4", 1), r(1.5)],
        ]
        return lines[(bar_ph + block) % 5]
    if ph == "D":
        lines = [
            [n("A3", 2.5), r(2.5)],
            [n("E4", 1), r(1), n("D4", 2), r(1)],
            [c(("B3", "D4"), 2), r(3)],
        ]
        return lines[(bar_ph + block) % 3]
    return [r(5)]

# === CELLO V5: Gravity + climax tension + collapse pedal + motif variation ===
def cello_content(sec, bar, m):
    ph = phase(m)
    bar_ph = bar_in_phase(m)
    if ph == "A":
        if bar_ph in (0, 1, 2, 4, 5, 7, 8, 10, 13):
            return [n("E2", 2), r(3)]
        return [n("A2", 1), n("E2", 2), r(2)]
    if ph == "B":
        if bar_ph in (0, 2, 4, 6, 8, 10, 12, 14):
            return [n("E2", 1), n("A2", 1), r(3)]
        return [n("E2", 2), r(3)]
    if ph == "C":
        if bar_ph < 20:
            return [n("E2", 1), n("A2", 1), n("E2", 1.5), r(1.5)]
        if bar_ph < 24:
            return [n("E2", 0.75), n("A2", 0.75), n("E2", 0.75), n("B2", 1), r(1.75)]
        return [n("A2", 2), r(3)]
    if ph == "D":
        if bar_ph in (0, 6, 12):
            return [n("A2", 1.5), n("E3", 1), n("G3", 1.5), r(1)]
        return [n("E2", 2), r(3)] if bar_ph % 2 == 0 else [n("A2", 2), r(3)]
    return [r(5)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Eviscerating Angels"
    s.metadata.composer = "Mike Bryant"

    parts = {}
    for name, inst, pname in [
        ("gtr", Guitar, "Guitar"),
        ("vn1", Violin, "Violin I"),
        ("vn2", Violin, "Violin II"),
        ("vla", Viola, "Viola"),
        ("vc", Violoncello, "Cello"),
    ]:
        p = stream.Part()
        p.partName = pname
        p.insert(0, inst())
        parts[name] = p

    last_chord_sym = None
    total_bars = 78
    for m in range(1, total_bars + 1):
        sec = section(m)
        bar = bar_in(m, sec)
        block = (m - 1) // 6

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))
            mm = tempo.MetronomeMark(number=76, referent=note.Note(type='quarter'))
            mm.text = "Slowly, dark and tense"
            mg.insert(0, mm)
            mg.insert(0, dynamics.Dynamic("pp"))

        if m in (1, 19, 37, 61):
            rm = expressions.RehearsalMark({1: "A", 19: "B", 37: "C", 61: "D"}[m])
            mg.insert(0, rm)

        dyn_map = {
            1: "pp", 15: "p", 25: "mp", 37: "mf", 45: "f", 50: "ff",
            58: "f", 61: "mp", 65: "p", 72: "pp"
        }
        if m in dyn_map:
            mg.insert(0, dynamics.Dynamic(dyn_map[m]))

        content, chord_sym = guitar_content(sec, bar, m)
        if chord_sym and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        for e in content:
            mg.append(e)
        parts["gtr"].append(mg)

        if m in (18, 36, 60):
            mg.rightBarline = Barline('double')

        for pname, content_list in [
            ("vla", viola_content(sec, bar, m, block)),
            ("vn1", violin1_content(sec, bar, m)),
            ("vn2", violin2_content(sec, bar, m)),
            ("vc", cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("5/4")
            if m == 1:
                mx.insert(0, key.KeySignature(-1))
            for e in content_list:
                mx.append(e)
            parts[pname].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def fix_redundant(path):
    import re
    with open(path, encoding="utf-8") as f:
        content = f.read()
    time_only = re.compile(
        r'\n\s+<attributes>\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+</attributes>',
        re.MULTILINE
    )
    div_plus_time = re.compile(
        r'(<attributes>\s*\n\s+<divisions>\d+</divisions>)\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+(</attributes>)',
        re.MULTILINE
    )
    content = time_only.sub('', content)
    content = div_plus_time.sub(r'\1\n      \2', content)
    content = re.sub(r'<rehearsal enclosure="none"', r'<rehearsal enclosure="rectangle"', content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    score = build_score()
    base = os.path.dirname(__file__)
    ws_root = os.path.abspath(os.path.join(base, "..", "..", ".."))
    out_ecm = os.path.join(ws_root, "ECM-Orbit-Album-2027", "Compositions", "Eviscerating_Angels", "V5_Eviscerating_Angels_Final.musicxml")
    os.makedirs(os.path.dirname(out_ecm), exist_ok=True)

    out_local = os.path.join(base, "musicxml", "V5_Eviscerating_Angels_Final.musicxml")
    os.makedirs(os.path.dirname(out_local), exist_ok=True)

    for out in [out_ecm, out_local]:
        score.write('musicxml', fp=out)
        fix_redundant(out)
        print(f"Exported: {out}")

if __name__ == "__main__":
    main()
