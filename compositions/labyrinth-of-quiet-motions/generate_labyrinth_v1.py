#!/usr/bin/env python3
"""
Labyrinth of Quiet Motions V1
Polyphonic Labyrinth / Counterpoint Hybrid
Target: GCE ≥ 9.8

Form: A (Emergence) B (Expansion) C (Labyrinth Core) D (Dissolution) E (Suspended Ending)
Motivic cell: m3 + M2 + P4 — developed through inversion, augmentation, fragmentation, voice exchange
Duration: 5–6 min at ♩ = 78
"""
import os
import xml.etree.ElementTree as ET
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

# === MOTIVIC CELL: m3 + M2 + P4 ===
# Prime: E-G-A-D (E-G m3, G-A M2, A-D P4)
# Inversion: D-A-G-E
# Transpositions used: E-G-A-D, Bb-Db-Eb-Ab, F-A-G-C, C-Eb-F-Bb, G-Bb-C-F
MOTIVE_PRIME = ("E4", "G4", "A4", "D5")
MOTIVE_INV = ("D4", "A4", "G4", "E5")
MOTIVE_FRAG = [("E4", "G4"), ("G4", "A4"), ("A4", "D5"), ("D5", "A4"), ("A4", "G4"), ("G4", "E4")]

def motive_transpose(pitches, semis):
    from music21 import pitch
    out = []
    for p in pitches:
        pt = pitch.Pitch(p)
        pt.transpose(semis, inPlace=True)
        out.append(pt.nameWithOctave)
    return tuple(out)

# === FORM ===
def section(m):
    if m <= 18: return "A"
    if m <= 40: return "B"
    if m <= 78: return "C"
    if m <= 98: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 19
    if sec == "C": return m - 41
    if sec == "D": return m - 79
    return m - 99

# === GUITAR: 40% dyads, 30% triadic, 20% single-line, 10% sustained ===
def guitar_a(bar):
    """A: Emergence — thin polyphonic threads"""
    frags = [
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3"), ("E3", "G3")],
        [("E3", "G3", "A3"), ("D4",), ("G3", "A3"), ("E3", "G3")],
        [("G3", "A3"), ("E3", "D3"), ("A3", "G3"), ("E3", "G3")],
        [("E3", "G3"), ("A3",), ("G3", "A3", "D4"), ("E3", "G3")],
        [("Bb2", "Db3"), ("Eb3", "Ab3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("E3", "G3"), ("rest"), ("G3", "A3"), ("E3", "G3")],
    ]
    return frags[bar % 6]

def guitar_b(bar):
    """B: Expansion — dyadic movement, inner-voice weaving"""
    frags = [
        [("E3", "G3", "A3"), ("D4", "A3"), ("G3", "A3"), ("E3", "G3")],
        [("F3", "A3"), ("G3", "C4"), ("A3", "G3"), ("F3", "A3")],
        [("Bb2", "Db3", "Eb3"), ("Ab3", "Eb3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3", "D4"), ("E3", "G3")],
        [("C3", "Eb3"), ("F3", "Bb3"), ("Eb3", "F3"), ("C3", "Eb3")],
        [("E3", "G3", "A3"), ("rest"), ("G3", "A3"), ("E3", "G3")],
    ]
    return frags[bar % 6]

def guitar_c(bar):
    """C: Labyrinth Core — maximum density, triadic fragments, dyads"""
    frags = [
        [("E3", "G3", "A3"), ("D4", "A3"), ("G3", "A3", "D4"), ("E3", "G3")],
        [("Bb2", "Db3", "Eb3"), ("Ab3", "Eb3", "Ab3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("F3", "A3", "G3"), ("C4", "G3"), ("A3", "G3", "C4"), ("F3", "A3")],
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3"), ("E3", "G3", "A3")],
        [("C3", "Eb3", "F3"), ("Bb3", "F3"), ("Eb3", "F3", "Bb3"), ("C3", "Eb3")],
        [("G2", "Bb2", "C3"), ("F3", "C3"), ("Bb2", "C3"), ("G2", "Bb2")],
    ]
    return frags[bar % 6]

def guitar_d(bar):
    """D: Dissolution — voices peel away"""
    if bar < 8:
        frags = [
            [("E3", "G3"), ("A3",), ("G3", "A3"), ("rest",)],
            [("E3", "G3"), ("rest",), ("G3", "A3"), ("rest",)],
            [("E3", "G3"), ("rest",), ("rest",), ("E3", "G3")],
            [("rest",), ("G3", "A3"), ("rest",), ("rest",)],
        ]
        return frags[bar % 4]
    frags = [
        [("E3", "G3"), ("rest",), ("rest",), ("rest",)],
        [("rest",), ("rest",), ("G3", "A3"), ("rest",)],
    ]
    return frags[bar % 2]

def guitar_e(bar):
    """E: Suspended Ending — soft guitar dyad"""
    if bar < 4:
        return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]
    if bar < 8:
        return [("rest",), ("G3", "A3"), ("rest",), ("rest",)]
    return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]

def guitar_content(sec, bar, m):
    if sec == "A": frags = guitar_a(bar)
    elif sec == "B": frags = guitar_b(bar)
    elif sec == "C": frags = guitar_c(bar)
    elif sec == "D": frags = guitar_d(bar)
    else: frags = guitar_e(bar)

    out = []
    for f in frags:
        if f == ("rest",) or f == "rest":
            out.append(r(1))
        elif len(f) == 1:
            out.append(n(f[0], 1))
        elif len(f) == 2:
            out.append(c(f, 1))
        else:
            out.append(c(f, 1))
    return out

# === VIOLIN I: Primary melodic narrative ===
def violin1_content(sec, bar, m):
    if sec == "A":
        lines = [
            [r(1), n("E5", 1), n("G5", 1), n("A5", 1)],
            [n("D6", 1.5), r(0.5), n("A5", 1), r(1)],
            [r(2), n("G5", 1), n("A5", 0.5), r(0.5)],
            [n("E5", 2), r(0.5), n("G5", 0.5), r(1)],
            [n("A5", 1), r(1), n("D5", 1), r(1)],
            [r(1), n("G5", 1.5), r(0.5), n("E5", 1)],
        ]
        return lines[bar % 6]
    if sec == "B":
        lines = [
            [n("E5", 0.5), n("G5", 0.5), n("A5", 1), n("D6", 1)],
            [n("A5", 1), n("G5", 1), r(1), n("E5", 1)],
            [n("Bb5", 1), n("Db6", 0.5), n("Eb6", 0.5), r(2)],
            [n("D6", 1.5), r(0.5), n("A5", 1), r(1)],
            [n("F5", 1), n("A5", 1), n("G5", 1), r(1)],
            [n("E5", 2), n("G5", 0.5), n("A5", 0.5), r(1)],
        ]
        return lines[bar % 6]
    if sec == "C":
        lines = [
            [n("E5", 0.5), n("G5", 0.5), n("A5", 0.5), n("D6", 0.5), n("A5", 1), r(1)],
            [n("Bb5", 1), n("Eb6", 1), n("Ab5", 1), r(1)],
            [n("D6", 0.5), n("A5", 0.5), n("G5", 1), n("E5", 1), r(1)],
            [n("E5", 1), n("G5", 1), n("A5", 1), n("D6", 1)],
            [n("F5", 1), n("A5", 0.5), n("G5", 0.5), n("C6", 1), r(1)],
            [n("G5", 1), n("Bb5", 1), n("C6", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "D":
        if bar < 10:
            return [n("E5", 2), r(1), n("G5", 0.5), r(0.5)]
        if bar < 16:
            return [n("A5", 1), r(2), n("D5", 0.5), r(0.5)]
        return [r(4)]
    if sec == "E":
        if bar < 4:
            return [n("E6", 4)]
        if bar < 8:
            return [r(2), n("G5", 2)]
        return [n("E6", 4)]
    return [r(4)]

# === VIOLIN II: Secondary counterline, rhythmic displacement ===
def violin2_content(sec, bar, m):
    if sec == "A":
        lines = [
            [n("C5", 1), r(0.5), n("E5", 1), r(1.5)],
            [r(1), n("A4", 1), n("G4", 1), r(1)],
            [n("D5", 1.5), r(0.5), n("A4", 1), r(1)],
            [r(0.5), n("G4", 1), n("A4", 1), r(1.5)],
            [n("E5", 1), r(2), n("G4", 0.5), r(0.5)],
            [r(1), n("A4", 1.5), r(0.5), n("E5", 1)],
        ]
        return lines[bar % 6]
    if sec == "B":
        lines = [
            [r(0.5), n("G4", 1), n("A4", 1), r(1.5)],
            [n("D5", 1), n("A4", 1), r(1), n("G4", 1)],
            [n("Eb5", 1), r(1), n("Ab4", 1), r(1)],
            [r(1), n("A4", 1.5), n("G4", 0.5), r(1)],
            [n("F4", 1), n("A4", 1), r(2)],
            [n("E5", 0.5), r(0.5), n("G4", 1), n("A4", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "C":
        lines = [
            [n("A4", 0.5), n("G4", 0.5), n("E4", 1), n("D5", 1), r(1)],
            [n("Eb5", 1), n("Ab4", 1), n("Db5", 1), r(1)],
            [r(0.5), n("A4", 1), n("G4", 1), n("E5", 1), r(0.5)],
            [n("E4", 1), n("G4", 1), n("A4", 1), n("D5", 1)],
            [n("G4", 1), n("C5", 1), r(1), n("A4", 1)],
            [n("Bb4", 1), n("C5", 1), n("F5", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "D":
        if bar < 12:
            return [r(1), n("G4", 1), r(1), n("A4", 1)]
        return [r(4)]
    if sec == "E":
        if bar < 6:
            return [r(2), n("A5", 2)]
        return [r(4)]
    return [r(4)]

# === VIOLA: Inner-voice engine, harmonic friction ===
def viola_content(sec, bar, m):
    if sec == "A":
        lines = [
            [n("E4", 1), n("G4", 1), r(1), n("A4", 1)],
            [n("D4", 1.5), r(0.5), n("A3", 1), r(1)],
            [n("G4", 1), n("A4", 1), n("D4", 1), r(1)],
            [r(1), n("E4", 1), n("G4", 1), r(1)],
            [n("A3", 1), n("G3", 1), n("E3", 1), r(1)],
            [n("E4", 1.5), r(0.5), n("G4", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "B":
        lines = [
            [n("G4", 0.5), n("A4", 0.5), n("D5", 1), n("E4", 1)],
            [n("A4", 1), n("G4", 1), n("E4", 1), r(1)],
            [n("Db4", 1), n("Eb4", 1), n("Ab4", 1), r(1)],
            [n("D4", 1), n("A4", 1), r(1), n("G4", 1)],
            [n("F4", 1), n("G4", 1), n("C4", 1), r(1)],
            [n("E4", 1), n("G4", 0.5), n("A4", 0.5), n("D4", 1)],
        ]
        return lines[bar % 6]
    if sec == "C":
        lines = [
            [n("E4", 0.5), n("G4", 0.5), n("A4", 0.5), n("D5", 0.5), n("A4", 1), r(1)],
            [n("Bb4", 1), n("Eb4", 1), n("Ab4", 1), r(1)],
            [n("D4", 1), n("A4", 1), n("G4", 1), r(1)],
            [n("E4", 1), n("G4", 1), n("A4", 1), n("D4", 1)],
            [n("F4", 1), n("A4", 1), n("G4", 1), r(1)],
            [n("Bb3", 1), n("C4", 1), n("F4", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "D":
        if bar < 14:
            return [n("E4", 2), n("G4", 1), r(1)]
        return [r(4)]
    if sec == "E":
        if bar < 6:
            return [n("E4", 2), r(2)]
        return [r(4)]
    return [r(4)]

# === CELLO: Slow harmonic gravity, pivot tones ===
def cello_content(sec, bar, m):
    if sec == "A":
        lines = [
            [n("E2", 2), n("A2", 1), r(1)],
            [n("D2", 2), r(1), n("A2", 1)],
            [n("E2", 1), n("G2", 1), n("A2", 1), r(1)],
            [n("D2", 2), n("E2", 1), r(1)],
            [n("Bb1", 2), n("Eb2", 1), r(1)],
            [n("E2", 2), r(2)],
        ]
        return lines[bar % 6]
    if sec == "B":
        lines = [
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("D2", 2), n("A2", 1), r(1)],
            [n("Bb1", 2), n("Eb2", 1), r(1)],
            [n("E2", 1), n("G2", 1), n("A2", 1), r(1)],
            [n("F2", 2), n("C2", 1), r(1)],
            [n("E2", 2), n("A2", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "C":
        lines = [
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("Bb1", 1), n("Eb2", 1), n("Ab2", 1), r(1)],
            [n("D2", 1), n("A2", 1), n("G2", 1), r(1)],
            [n("E2", 2), n("A2", 1), r(1)],
            [n("F2", 1), n("C3", 1), n("Bb2", 1), r(1)],
            [n("G2", 2), n("C3", 1), r(1)],
        ]
        return lines[bar % 6]
    if sec == "D":
        if bar < 12:
            return [n("E2", 2), r(1), n("A2", 1)]
        if bar < 18:
            return [n("E2", 2), r(2)]
        return [r(4)]
    if sec == "E":
        return [n("E2", 4)]
    return [r(4)]

# === TEXTURE: reduced vs full (30% reduced) ===
def use_reduced_texture(m, sec):
    if sec == "A":
        return m in (3, 4, 7, 8, 12, 13, 17)
    if sec == "B":
        return m in (22, 23, 28, 29, 35, 36)
    if sec == "C":
        return m in (45, 46, 54, 55, 63, 64, 72, 73)
    if sec == "D":
        return m >= 85
    if sec == "E":
        return True
    return False

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Labyrinth of Quiet Motions"
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

    section_starts = [1, 19, 41, 79, 99]
    section_labels = ["A", "B", "C", "D", "E"]
    section_double_barlines = [18, 40, 78, 98]

    for m in range(1, 113):
        sec = section(m)
        bar = bar_in(m, sec)
        reduced = use_reduced_texture(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=78, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("pp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))

        if m == 41:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 79:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 99:
            mg.insert(0, dynamics.Dynamic("pp"))

        g_content = guitar_content(sec, bar, m)
        for e in g_content:
            mg.append(e)

        if m in section_double_barlines:
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        vn1_c = violin1_content(sec, bar, m)
        vn2_c = violin2_content(sec, bar, m)
        vla_c = viola_content(sec, bar, m)
        vc_c = cello_content(sec, bar, m)

        if reduced:
            if m % 3 == 0:
                vn2_c = [r(4)]
            if m % 3 == 1:
                vla_c = [r(4)]
            if m % 3 == 2:
                vn1_c = [r(4)]

        for name, content in [
            ("vn1", vn1_c),
            ("vn2", vn2_c),
            ("vla", vla_c),
            ("vc", vc_c),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("4/4")
            for e in content:
                mx.append(e)
            parts[name].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def engrave_clean_time_sigs(path):
    """Remove redundant <time> — emit only at meter change points."""
    tree = ET.parse(path)
    root = tree.getroot()
    parts = root.findall("part")
    first_part = True
    for part in parts:
        last_time = None
        for i, measure in enumerate(part.findall("measure")):
            attrs = measure.find("attributes")
            if attrs is None:
                continue
            time_el = attrs.find("time")
            if time_el is None:
                continue
            beats_el = time_el.find("beats")
            bt_el = time_el.find("beat-type")
            if beats_el is None or bt_el is None:
                continue
            current = (beats_el.text, bt_el.text)
            is_first = (i == 0) and first_part
            if is_first:
                last_time = current
                continue
            divs = attrs.find("divisions")
            key_el = attrs.find("key")
            if divs is None and key_el is None and current == last_time:
                attrs.remove(time_el)
                if len(attrs) == 0:
                    measure.remove(attrs)
            else:
                last_time = current
        first_part = False
    tree.write(path, encoding="unicode", default_namespace="", method="xml", xml_declaration=False)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    doctype = '<!DOCTYPE score-partwise  PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'
    if "<!DOCTYPE" not in content:
        content = '<?xml version="1.0" encoding="utf-8"?>\n' + doctype + "\n" + content
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    score = build_score()
    base = os.path.dirname(__file__)
    out_dir = os.path.join(base, "musicxml")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "V1_Labyrinth_of_Quiet_Motions.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")

if __name__ == "__main__":
    main()
