#!/usr/bin/env python3
"""
Unreliable Gravity V2 – Andrew Hill Harmonic Engine (7/4, GCE 9.6+)
Orbit Album – Guitar + String Quartet

Full upgrade: 7/4 (4+3), guitar-first, motivic integration, texture variation.
52 bars, ♩=62. ~5.5 min.

Sections: A(1-12) Unstable emergence, B(13-24) Harmonic drift,
C(25-38) Motivic accumulation (guitar drives), D(39-42) Gravitational collapse,
E(43-52) Suspended aftermath.
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

def section(m):
    if m <= 12: return "A"
    if m <= 24: return "B"
    if m <= 38: return "C"
    if m <= 42: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 13
    if sec == "C": return m - 25
    if sec == "D": return m - 39
    return m - 43

def chord_for_section(sec, bar, m):
    cycle = (m - 1) // 3
    if sec == "A":
        opts = ["Em", "Bbmaj7", "C#m", "Fmaj7", "Em", "Gmaj7"]
        return opts[(bar + cycle) % 6]
    if sec == "B":
        opts = ["Bbmaj7", "C#m", "Fmaj7", "Em", "Db7", "Fmaj7", "Bbmaj7"]
        return opts[(bar + cycle) % 7]
    if sec == "C":
        opts = ["C#m", "Fmaj7", "Em", "Bbmaj7", "Gmaj7", "Db7", "Em", "Fmaj7"]
        return opts[(bar + cycle) % 8]
    if sec == "D":
        return "cluster" if bar % 2 == 1 else "Em"
    return "Em"

# === GUITAR V2: Guitar-first — dyads, triads, sustained colour, drives C ===
def guitar_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 3, 7, 10):
            return [r(7)], None
        blocks = [
            [c(("E3", "B3"), 3), r(4)],
            [c(("Bb3", "F4", "D4"), 4), r(3)],
            [c(("C#3", "G#3"), 2), r(2), c(("C#3", "G#3"), 2), r(1)],
            [c(("F3", "A3", "C4"), 4), r(3)],
        ]
        return blocks[bar % 4], chord_for_section(sec, bar, m)
    if sec == "B":
        if bar in (1, 5, 9):
            return [r(7)], None
        if bar in (3, 7):
            return [c(("Bb3", "F4"), 1), r(1), c(("C#4", "G#4"), 1), r(1), c(("F3", "C4"), 1.5), r(1.5)], chord_for_section(sec, bar, m)
        blocks = [
            [c(("Bb3", "D4"), 3), r(2), c(("Bb3", "F4"), 2)],
            [c(("C#4", "G#4", "E4"), 4), r(3)],
            [c(("F3", "A3"), 2), r(2), c(("E3", "G3"), 2), r(1)],
            [c(("G3", "B3", "D4"), 4), r(3)],
        ]
        return blocks[bar % 4], chord_for_section(sec, bar, m)
    if sec == "C":
        if bar in (0, 4, 9, 13):
            return [r(7)], None
        if bar in (5, 6):
            return [c(("C4", "Db4"), 2), r(2), c(("G3", "B3"), 2), r(1)], chord_for_section(sec, bar, m)
        blocks = [
            [c(("C#3", "G#3", "B3"), 4), r(3)],
            [c(("F3", "C4"), 2), c(("E3", "B3"), 3), r(2)],
            [c(("Bb3", "F4"), 3), r(2), c(("Db3", "Ab3"), 2)],
            [c(("E3", "G3", "B3"), 4), r(3)],
            [c(("F3", "A3"), 2), r(2), c(("Bb3", "D4"), 2), r(1)],
        ]
        return blocks[bar % 5], chord_for_section(sec, bar, m)
    if sec == "D":
        if bar in (0, 2):
            return [r(7)], None
        return [c(("E3", "Bb3"), 2), r(2), c(("C#4", "G4"), 2), r(1)], chord_for_section(sec, bar, m)
    if sec == "E":
        if bar in (0, 1, 3, 5, 7):
            return [r(7)], None
        if bar == 9:
            return [c(("E4", "B4"), 5), r(2)], "Em"
        blocks = [
            [c(("E3", "B3"), 4), r(3)],
            [c(("Bb3", "F4"), 3), r(4)],
            [c(("E4", "G4", "B4"), 4), r(3)],
        ]
        return blocks[bar % 3], chord_for_section(sec, bar, m)
    return [r(7)], None

# === VIOLIN I: Fragmented narrative, motif G5-Db5-C5 ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 3, 7, 10):
            return [n("G5", 2.5), r(1), n("Db5", 2), r(1.5)]
        if bar in (2, 5, 9):
            return [r(2), n("C5", 2), n("Db5", 2), r(1)]
        return [r(7)]
    if sec == "B":
        if bar in (1, 5, 9):
            return [n("Bb5", 2), r(2), n("F#5", 2), r(1)]
        if bar in (3, 8):
            return [r(1), n("G5", 2), n("Db5", 3), r(1)]
        return [r(7)]
    if sec == "C":
        if bar in (5, 6):
            return [r(2), n("G5", 2), n("Db5", 2), r(1)]
        if bar in (1, 4, 8, 12):
            return [n("G5", 2), r(2), n("Db5", 2), r(1)]
        if bar in (3, 7, 11):
            return [c(("C5", "Db5"), 2), r(3), n("G5", 2)]
        return [r(7)]
    if sec == "D":
        if bar in (1, 2, 3):
            return [c(("G5", "Bb5", "Db6"), 2.5), r(1), n("C6", 2.5), r(1)]
        return [r(7)]
    if sec == "E":
        if bar in (0, 1):
            return [n("G4", 3), r(2), n("Db4", 2)]
        if bar in (2, 5, 8):
            return [n("G5", 4), r(3)]
        if bar in (4, 7):
            return [r(2), n("Db5", 4), r(1)]
        return [r(7)]
    return [r(7)]

# === VIOLIN II: Delayed echoes, off-axis answers ===
def violin2_content(sec, bar, m):
    if sec == "A":
        if bar in (2, 6, 10):
            return [r(2), n("C5", 2), r(2), n("Db5", 1)]
        return [r(7)]
    if sec == "B":
        if bar in (2, 6, 10):
            return [r(1), n("G4", 2), n("Db4", 2), r(2)]
        return [r(7)]
    if sec == "C":
        if bar in (2, 6, 10):
            return [r(2), n("G4", 2.5), r(2.5)]
        return [r(7)]
    if sec == "D":
        if bar in (2, 3):
            return [n("Bb4", 2), r(2), n("F4", 2.5), r(0.5)]
        return [r(7)]
    if sec == "E":
        if bar in (3, 6):
            return [n("G4", 4), r(3)]
        if bar == 9:
            return [n("B5", 4), r(3)]
        return [r(7)]
    return [r(7)]

# === VIOLA: Chromatic inner tension, contrary motion ===
def viola_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        lines = [
            [n("C4", 2), n("Db4", 2), r(2), n("G4", 1)],
            [n("E4", 2), n("Eb4", 2), r(2), n("Bb3", 1)],
            [n("G3", 2), r(2), n("C#4", 2), n("D4", 1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "B":
        lines = [
            [n("D4", 2), n("Db4", 2), r(2), n("Ab3", 1)],
            [n("F4", 2), n("E4", 2), r(2), n("C4", 1)],
            [n("Bb3", 2), n("B3", 2), r(2), n("F#4", 1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "C":
        lines = [
            [n("C#4", 2), n("C4", 2), r(2), n("G#3", 1)],
            [n("F4", 2), n("Gb4", 1), n("F4", 1), r(3)],
            [n("E4", 2), n("Eb4", 2), r(2), n("Bb3", 1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "D":
        if bar in (1, 3):
            return [c(("C4", "Eb4", "Gb4"), 2.5), r(1), n("Bb3", 2.5), r(1)]
        return [r(7)]
    if sec == "E":
        if bar in (0, 2, 4, 6, 8):
            return [n("E4", 4), r(3)]
        return [r(7)]
    return [r(7)]

# === CELLO: Gravity lines, register leap in D ===
def cello_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        patterns = [
            [n("E2", 4), r(3)],
            [n("Bb2", 2), n("E2", 2), r(3)],
            [n("C#2", 4), r(3)],
            [n("F2", 2), n("Bb2", 2), r(3)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "B":
        patterns = [
            [n("Bb2", 4), r(3)],
            [n("C#2", 2), n("F2", 2), r(3)],
            [n("E2", 4), r(3)],
            [n("Db2", 2), n("F2", 2), r(3)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "C":
        patterns = [
            [n("C#2", 4), r(3)],
            [n("F2", 2), n("Bb2", 2), r(3)],
            [n("E2", 4), r(3)],
            [n("G2", 2), n("Bb2", 2), r(3)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "D":
        if bar in (0, 1):
            return [n("E2", 2), n("Bb2", 2), n("E2", 2), r(1)]
        if bar in (2, 3):
            return [n("C#3", 2), n("G2", 2), n("Bb2", 2), r(1)]
        return [n("E2", 4), r(3)]
    if sec == "E":
        if bar < 8:
            return [n("E2", 4), r(3)] if bar % 2 == 0 else [n("Bb2", 4), r(3)]
        return [n("E3", 7)]
    return [r(7)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Unreliable Gravity"
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

    section_starts = [1, 13, 25, 39, 43]
    section_labels = ["A", "B", "C", "D", "E"]
    dyn_map = {
        1: "pp", 5: "p", 13: "mp", 25: "mp", 32: "mf", 39: "f",
        41: "ff", 43: "mf", 47: "p", 50: "pp"
    }
    harm_moment = 50

    last_chord_sym = None
    for m in range(1, 53):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("7/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mm = tempo.MetronomeMark(number=62, referent=note.Note(type='quarter'))
            mm.text = "Slowly, unstable (4+3)"
            mg.insert(0, mm)

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in dyn_map:
            mg.insert(0, dynamics.Dynamic(dyn_map[m]))
        if m == harm_moment:
            mg.insert(0, expressions.TextExpression("harmonics"))

        chord_sym = chord_for_section(sec, bar, m)
        if chord_sym and chord_sym != "cluster" and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym

        content, _ = guitar_content(sec, bar, m)
        for e in content:
            mg.append(e)

        if m in (12, 24, 38, 42):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for pname, content_list in [
            ("vla", viola_content(sec, bar, m)),
            ("vn1", violin1_content(sec, bar, m)),
            ("vn2", violin2_content(sec, bar, m)),
            ("vc", cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("7/4")
            if m == 1:
                mx.insert(0, key.KeySignature(0))
            if pname == "vn2" and m == harm_moment:
                mx.insert(0, expressions.TextExpression("harmonics"))
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
        r'\n\s+<attributes>\s*\n\s+<time>\s*\n\s+<beats>7</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+</attributes>',
        re.MULTILINE
    )
    div_plus_time = re.compile(
        r'(<attributes>\s*\n\s+<divisions>\d+</divisions>)\s*\n\s+<time>\s*\n\s+<beats>7</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+(</attributes>)',
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
    comp_root = os.path.abspath(os.path.join(base, ".."))
    ws_root = os.path.abspath(os.path.join(base, "..", "..", ".."))
    out_ecm = os.path.join(ws_root, "ECM-Orbit-Album-2027", "Compositions", "Unreliable_Gravity", "V2_Unreliable_Gravity_7-4.musicxml")
    os.makedirs(os.path.dirname(out_ecm), exist_ok=True)

    out_local = os.path.join(comp_root, "musicxml", "V2_Unreliable_Gravity_7-4.musicxml")
    os.makedirs(os.path.dirname(out_local), exist_ok=True)

    for out in [out_ecm, out_local]:
        score.write('musicxml', fp=out)
        fix_redundant(out)
        print(f"Exported: {out}")

if __name__ == "__main__":
    main()
