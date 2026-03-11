#!/usr/bin/env python3
"""
Unreliable Gravity V1 – Andrew Hill Harmonic Engine
Orbit Album – Guitar + String Quartet

Dark, harmonically unstable chamber work. Tonal centres form and dissolve.
Core motif: C4-Db4-G4 (minor 2nd → tritone). Non-functional harmony.
~5–6 min at ♩=63. 80 bars, 4/4.

Sections: A(1-16) Unstable emergence, B(17-32) Harmonic drift,
C(33-56) Motivic accumulation, D(57-64) Gravitational collapse,
E(65-80) Suspended aftermath.
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
    if m <= 16: return "A"
    if m <= 32: return "B"
    if m <= 56: return "C"
    if m <= 64: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 17
    if sec == "C": return m - 33
    if sec == "D": return m - 57
    return m - 65

# Andrew Hill: Em, Bbmaj, C#min, Fmaj, clusters. Roots by m3/tritone.
def chord_for_section(sec, bar, m):
    cycle = (m - 1) // 4
    if sec == "A":
        opts = ["Em", "Bbmaj7", "C#m", "Fmaj7"]
        return opts[(bar + cycle) % 4]
    if sec == "B":
        opts = ["Bbmaj7", "C#m", "Fmaj7", "Em", "Gmaj7"]
        return opts[(bar + cycle) % 5]
    if sec == "C":
        opts = ["C#m", "Fmaj7", "Em", "Bbmaj7", "Db7", "Fmaj7"]
        return opts[(bar + cycle) % 6]
    if sec == "D":
        return "cluster" if bar % 2 == 1 else "Em"
    return "Em"

# === CORE MOTIF: C4-Db4-G4 (m2 → tritone). Inversion: G4-Db4-C4. Frag: C-Db, Db-G ===

# === GUITAR: Harmonic instigator — dark dyads, incomplete chords, sparse ===
def guitar_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 2, 5, 8, 11, 14):
            return [r(4)], None
        blocks = [("E3", "B3"), ("Bb3", "F4"), ("C#3", "G#3"), ("F3", "C4")]
        pit = blocks[bar % 4]
        return [c(pit, 2), r(2)], chord_for_section(sec, bar, m)
    if sec == "B":
        if bar in (1, 4, 7, 10, 13):
            return [r(4)], None
        blocks = [("Bb3", "D4"), ("C#4", "G#4"), ("F3", "A3"), ("E3", "G3"), ("G3", "B3")]
        pit = blocks[bar % 5]
        return [c(pit, 2.5), r(1.5)], chord_for_section(sec, bar, m)
    if sec == "C":
        if bar in (0, 2, 5, 8, 11, 14, 17, 20):
            return [r(4)], None
        blocks = [("C#3", "G#3"), ("F3", "C4"), ("E3", "B3"), ("Bb3", "F4"), ("Db3", "Ab3")]
        pit = blocks[bar % 5]
        return [c(pit, 2), r(2)], chord_for_section(sec, bar, m)
    if sec == "D":
        if bar in (0, 2):
            return [r(4)], None
        blocks = [("E3", "Bb3"), ("C#4", "G4"), ("Bb3", "E4")]
        pit = blocks[bar % 3]
        return [c(pit, 1), r(1), c((pit[0], pit[1]), 1), r(1)], chord_for_section(sec, bar, m)
    if sec == "E":
        if bar in (0, 1, 3, 5, 7, 9, 11, 13, 15):
            return [r(4)], None
        if bar == 15:
            return [c(("E4", "B4"), 3), r(1)], "Em"
        blocks = [("E3", "B3"), ("Bb3", "F4"), ("E4", "B4")]
        pit = blocks[bar % 3]
        return [c(pit, 2.5), r(1.5)], chord_for_section(sec, bar, m)
    return [r(4)], None

# === VIOLIN I: Fragmented melodic statements — motif C-Db-G (G5-Db5-C5) ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 3, 6, 9, 12):
            return [n("G5", 1.5), r(0.5), n("Db5", 1), r(1)]
        if bar in (2, 5, 8):
            return [r(1), n("C5", 1), n("Db5", 1.5), r(0.5)]
        return [r(4)]
    if sec == "B":
        if bar in (1, 5, 9, 13):
            return [n("Bb5", 1), r(1), n("F#5", 1.5), r(0.5)]
        if bar in (3, 8, 12):
            return [r(0.5), n("G5", 1), n("Db5", 2), r(0.5)]
        return [r(4)]
    if sec == "C":
        if bar in (0, 3, 7, 11, 15, 19):
            return [n("G5", 2), r(1), n("Db5", 1)]
        if bar in (5, 10, 16):
            return [c(("C5", "Db5"), 1), r(2), n("G5", 1)]
        return [r(4)]
    if sec == "D":
        if bar in (1, 2, 3, 4, 5, 6):
            return [c(("G5", "Bb5", "Db6"), 1.5), r(0.5), n("C6", 1.5), r(0.5)]
        return [r(4)]
    if sec == "E":
        if bar in (2, 6, 10, 14):
            return [n("G5", 2.5), r(1.5)]
        if bar in (4, 8, 12):
            return [r(1), n("Db5", 2), r(1)]
        return [r(4)]
    return [r(4)]

# === VIOLIN II: Delayed echoes of motif ===
def violin2_content(sec, bar, m):
    if sec == "A":
        if bar in (2, 6, 10, 14):
            return [r(1), n("C5", 1), r(1), n("Db5", 1)]
        return [r(4)]
    if sec == "B":
        if bar in (2, 6, 10, 14):
            return [r(0.5), n("G4", 1), n("Db4", 1), r(1.5)]
        return [r(4)]
    if sec == "C":
        if bar in (1, 5, 9, 13, 17):
            return [r(1), n("G4", 1.5), r(1.5)]
        return [r(4)]
    if sec == "D":
        if bar in (2, 4, 6):
            return [n("Bb4", 1), r(1), n("F4", 1.5), r(0.5)]
        return [r(4)]
    if sec == "E":
        if bar in (3, 7, 11):
            return [n("G4", 2), r(2)]
        if bar == 15:
            return [n("B5", 2), r(2)]
        return [r(4)]
    return [r(4)]

# === VIOLA: Chromatic inner-voice instability ===
def viola_content(sec, bar, m):
    block = (m - 1) // 5
    if sec == "A":
        lines = [
            [n("C4", 1), n("Db4", 1), r(1), n("G4", 1)],
            [n("E4", 1), n("Eb4", 1), r(1), n("Bb3", 1)],
            [n("G3", 1), r(1), n("C#4", 1), n("D4", 1)],
            [n("Bb3", 1), n("A3", 1), r(1), n("F4", 1)],
        ]
        return lines[(bar + block) % 4]
    if sec == "B":
        lines = [
            [n("D4", 1), n("Db4", 1), r(1), n("Ab3", 1)],
            [n("F4", 1), n("E4", 1), r(1), n("C4", 1)],
            [n("Bb3", 1), n("B3", 1), r(1), n("F#4", 1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "C":
        lines = [
            [n("C#4", 1), n("C4", 1), r(1), n("G#3", 1)],
            [n("F4", 1), n("Gb4", 0.5), n("F4", 0.5), r(2)],
            [n("E4", 1), n("Eb4", 1), r(1), n("Bb3", 1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "D":
        if bar in (1, 3, 5):
            return [c(("C4", "Eb4", "Gb4"), 1.5), r(0.5), n("Bb3", 1.5), r(0.5)]
        return [r(4)]
    if sec == "E":
        if bar in (0, 2, 4, 6, 8):
            return [n("E4", 2), r(2)]
        return [r(4)]
    return [r(4)]

# === CELLO: Slow gravitational bass, sudden shifts ===
def cello_content(sec, bar, m):
    block = (m - 1) // 5
    if sec == "A":
        patterns = [
            [n("E2", 2), r(2)],
            [n("Bb2", 1), n("E2", 1), r(2)],
            [n("C#2", 2), r(2)],
            [n("F2", 1), n("Bb2", 1), r(2)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "B":
        patterns = [
            [n("Bb2", 2), r(2)],
            [n("C#2", 1), n("F2", 1), r(2)],
            [n("E2", 2), r(2)],
            [n("G2", 1), n("Bb2", 1), r(2)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "C":
        patterns = [
            [n("C#2", 2), r(2)],
            [n("F2", 1), n("Bb2", 1), r(2)],
            [n("E2", 2), r(2)],
            [n("Db2", 1), n("F2", 1), r(2)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "D":
        if bar in (0, 1):
            return [n("E2", 1), n("Bb2", 1), n("E2", 1), r(1)]
        if bar in (2, 3):
            return [n("C#3", 1), n("G2", 1), n("Bb2", 1), r(1)]
        return [n("E2", 2), r(2)]
    if sec == "E":
        if bar < 14:
            return [n("E2", 2), r(2)] if bar % 2 == 0 else [n("Bb2", 2), r(2)]
        return [n("E3", 4)]
    return [r(4)]

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

    section_starts = [1, 17, 33, 57, 65]
    section_labels = ["A", "B", "C", "D", "E"]
    dyn_map = {
        1: "pp", 10: "p", 17: "mp", 33: "mp", 45: "mf", 57: "f",
        60: "ff", 65: "mf", 70: "p", 75: "pp", 78: "pp"
    }
    harm_moment = 78

    last_chord_sym = None
    for m in range(1, 81):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mm = tempo.MetronomeMark(number=63, referent=note.Note(type='quarter'))
            mm.text = "Slowly, unstable"
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

        if m in (16, 32, 56, 64):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for pname, content_list in [
            ("vla", viola_content(sec, bar, m)),
            ("vn1", violin1_content(sec, bar, m)),
            ("vn2", violin2_content(sec, bar, m)),
            ("vc", cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("4/4")
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
        r'\n\s+<attributes>\s*\n\s+<time>\s*\n\s+<beats>4</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+</attributes>',
        re.MULTILINE
    )
    div_plus_time = re.compile(
        r'(<attributes>\s*\n\s+<divisions>\d+</divisions>)\s*\n\s+<time>\s*\n\s+<beats>4</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+(</attributes>)',
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
    out_ecm = os.path.join(ws_root, "ECM-Orbit-Album-2027", "Compositions", "Unreliable_Gravity", "V1_Unreliable_Gravity.musicxml")
    os.makedirs(os.path.dirname(out_ecm), exist_ok=True)

    out_local = os.path.join(comp_root, "musicxml", "V1_Unreliable_Gravity.musicxml")
    os.makedirs(os.path.dirname(out_local), exist_ok=True)

    for out in [out_ecm, out_local]:
        score.write('musicxml', fp=out)
        fix_redundant(out)
        print(f"Exported: {out}")

if __name__ == "__main__":
    main()
