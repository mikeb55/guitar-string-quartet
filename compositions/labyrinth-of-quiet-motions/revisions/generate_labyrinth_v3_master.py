#!/usr/bin/env python3
"""
Labyrinth of Quiet Motions V3 Master
Micro-refinement of V2 — GCE 9.8–10

Refinements:
- Section C: extend densest climax by 3 measures; more contrary motion
- Registral contrast: Vn1 climbs to G7/E7 while others thin (one moment)
- B→C transition: brief unison gesture (m.40) that fragments into C
"""
import os
import xml.etree.ElementTree as ET
from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    expressions, dynamics
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

# === FORM: C +3 measures ===
def section(m):
    if m <= 18: return "A"
    if m <= 40: return "B"
    if m <= 86: return "C"
    if m <= 106: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 19
    if sec == "C": return m - 41
    if sec == "D": return m - 87
    return m - 107

# === GUITAR ===
def guitar_a(bar):
    frags = [
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3"), ("E3", "G3")],
        [("E3", "G3", "A3"), ("D4",), ("G3", "A3"), ("E3", "G3")],
        [("G3", "A3"), ("E3", "D3"), ("A3", "G3"), ("E3", "G3")],
        [("E3", "G3"), ("A3",), ("G3", "A3", "D4"), ("E3", "G3")],
        [("Bb2", "Db3"), ("Eb3", "Ab3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("E3", "G3"), ("rest",), ("G3", "A3"), ("E3", "G3")],
    ]
    return frags[bar % 6]

def guitar_b(bar, m):
    if m == 40:
        return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]
    frags = [
        [("E3", "G3", "A3"), ("D4", "A3"), ("G3", "A3"), ("E3", "G3")],
        [("F3", "A3"), ("G3", "C4"), ("A3", "G3"), ("F3", "A3")],
        [("Bb2", "Db3", "Eb3"), ("Ab3", "Eb3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3", "D4"), ("E3", "G3")],
        [("C3", "Eb3"), ("F3", "Bb3"), ("Eb3", "F3"), ("C3", "Eb3")],
        [("E3", "G3", "A3"), ("rest",), ("G3", "A3"), ("E3", "G3")],
    ]
    return frags[bar % 6]

def guitar_c(bar, m):
    if bar in (18, 19):
        return [
            [("E3", "G3"), ("A3", "D4"), ("G3", "A3"), ("E3", "G3")],
            [("E3", "G3"), ("A3",), ("G3", "A3"), ("E3", "G3")],
        ][bar - 18]
    frags = [
        [("E3", "G3", "A3"), ("D4", "A3"), ("G3", "A3", "D4"), ("E3", "G3")],
        [("Bb2", "Db3", "Eb3"), ("Ab3", "Eb3", "Ab3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("F3", "A3", "G3"), ("C4", "G3"), ("A3", "G3", "C4"), ("F3", "A3")],
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3"), ("E3", "G3", "A3")],
        [("C3", "Eb3", "F3"), ("Bb3", "F3"), ("Eb3", "F3", "Bb3"), ("C3", "Eb3")],
        [("G2", "Bb2", "C3"), ("F3", "C3"), ("Bb2", "C3"), ("G2", "Bb2")],
        [("E3", "G3"), ("A3", "D4"), ("G3", "A3", "D4"), ("E3", "G3")],
        [("Bb2", "Db3"), ("Eb3", "Ab3"), ("Db3", "Eb3"), ("Bb2", "Db3")],
        [("E3", "G3", "A3"), ("D4", "A3"), ("G3", "A3"), ("E3", "G3")],
        [("F3", "A3"), ("G3", "C4"), ("Eb3", "F3"), ("C3", "Eb3")],
    ]
    return frags[bar % 10]

def guitar_d(bar):
    if bar < 6:
        frags = [
            [("E3", "G3"), ("A3",), ("G3", "A3"), ("rest",)],
            [("E3", "G3"), ("rest",), ("G3", "A3"), ("rest",)],
            [("E3", "G3"), ("rest",), ("rest",), ("E3", "G3")],
            [("rest",), ("G3", "A3"), ("rest",), ("rest",)],
            [("E3", "G3"), ("A3",), ("rest",), ("rest",)],
            [("E3", "G3"), ("rest",), ("G3", "A3"), ("rest",)],
        ]
        return frags[bar % 6]
    if bar < 12:
        frags = [
            [("E3", "G3"), ("rest",), ("rest",), ("rest",)],
            [("rest",), ("G3", "A3"), ("rest",), ("rest",)],
            [("E3", "G3"), ("rest",), ("rest",), ("rest",)],
        ]
        return frags[bar % 3]
    return [("E3", "G3"), ("rest",), ("rest",), ("rest",)] if bar % 2 == 0 else [("rest",), ("rest",), ("G3", "A3"), ("rest",)]

def guitar_e(bar):
    if bar < 4:
        return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]
    if bar < 8:
        return [("rest",), ("G3", "A3"), ("rest",), ("rest",)]
    if bar < 14:
        return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]
    if bar == 14:
        return [("rest",), ("rest",), ("rest",), ("rest",)]
    return [("E3", "G3"), ("rest",), ("rest",), ("rest",)]

def guitar_content(sec, bar, m):
    if sec == "A": frags = guitar_a(bar)
    elif sec == "B": frags = guitar_b(bar, m)
    elif sec == "C": frags = guitar_c(bar, m)
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

# === VIOLIN I: Registral contrast at bar 68 (m.68) ===
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
        if m == 40:
            return [n("E5", 1), r(3)]
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
        if bar in (18, 19):
            return [
                [n("E5", 1), n("G5", 1), n("A5", 1), n("D6", 1)],
                [n("D6", 1.5), r(0.5), n("A5", 1), r(1)],
            ][bar - 18]
        if bar == 27:
            return [n("G7", 2), n("E7", 2)]
        if bar in (26, 28):
            return [r(4)]
        lines = [
            [n("E5", 0.5), n("G5", 0.5), n("A5", 0.5), n("D6", 0.5), n("A5", 1), r(1)],
            [n("Bb5", 1), n("Eb6", 1), n("Ab5", 1), r(1)],
            [n("D6", 0.5), n("A5", 0.5), n("G5", 1), n("E5", 1), r(1)],
            [n("E5", 1), n("G5", 1), n("A5", 1), n("D6", 1)],
            [n("F5", 1), n("A5", 0.5), n("G5", 0.5), n("C6", 1), r(1)],
            [n("G5", 1), n("Bb5", 1), n("C6", 1), r(1)],
            [n("E5", 1), n("G5", 1), n("A5", 0.5), n("D6", 0.5), r(1)],
            [n("Bb5", 1), n("Eb6", 0.5), n("Ab5", 0.5), r(2)],
            [n("E5", 0.5), n("G5", 0.5), n("A5", 1), n("D6", 1), r(1)],
            [n("D6", 1), n("A5", 1), n("G5", 0.5), n("E5", 0.5), r(1)],
        ]
        return lines[bar % 10]
    if sec == "D":
        if bar < 8:
            return [n("E5", 2), r(1), n("G5", 0.5), r(0.5)]
        if bar < 14:
            return [n("A5", 1), r(2), n("D5", 0.5), r(0.5)]
        if bar < 18:
            return [n("E5", 2), r(2)]
        return [r(4)]
    if sec == "E":
        if bar < 4:
            return [n("E6", 4)]
        if bar < 8:
            return [r(2), n("G5", 2)]
        if bar < 14:
            return [n("E6", 4)]
        if bar == 14:
            return [r(4)]
        return [n("E6", 4)]
    return [r(4)]

# === VIOLIN II: Unison at m.40; thin at registral contrast ===
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
        if m == 40:
            return [n("E5", 1), r(3)]
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
        if bar in (18, 19):
            return [
                [n("E4", 1), n("G4", 1), n("A4", 1), n("D5", 1)],
                [r(1), n("A4", 1), n("G4", 1), r(1)],
            ][bar - 18]
        if bar in (26, 27, 28):
            return [r(4)]
        lines = [
            [n("A4", 0.5), n("G4", 0.5), n("E4", 1), n("D5", 1), r(1)],
            [n("Eb5", 1), n("Ab4", 1), n("Db5", 1), r(1)],
            [r(0.5), n("A4", 1), n("G4", 1), n("E5", 1), r(0.5)],
            [n("E4", 1), n("G4", 1), n("A4", 1), n("D5", 1)],
            [n("G4", 1), n("C5", 1), r(1), n("A4", 1)],
            [n("Bb4", 1), n("C5", 1), n("F5", 1), r(1)],
            [n("D5", 1), n("A4", 1), n("G4", 0.5), n("E4", 0.5), r(1)],
            [n("Eb5", 1), n("Ab4", 1), n("Db5", 1), r(1)],
            [n("A4", 0.5), n("G4", 0.5), n("E4", 1), n("D5", 1), r(1)],
            [n("D5", 1), n("A4", 1), n("G4", 0.5), n("E4", 0.5), r(1)],
        ]
        return lines[bar % 10]
    if sec == "D":
        if bar < 14:
            return [r(1), n("G4", 1), r(1), n("A4", 1)]
        return [r(4)]
    if sec == "E":
        if bar < 6:
            return [r(2), n("A5", 2)]
        if bar == 14:
            return [r(4)]
        return [r(4)]
    return [r(4)]

# === VIOLA: Unison at m.40; thin at registral contrast ===
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
        if m == 40:
            return [n("E4", 1), r(3)]
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
        if bar in (18, 19):
            return [
                [n("E4", 1), n("G4", 1), n("A4", 1), n("D5", 1)],
                [n("D4", 1), n("A4", 1), n("G4", 1), r(1)],
            ][bar - 18]
        if bar in (26, 27, 28):
            return [r(4)]
        lines = [
            [n("E4", 0.5), n("G4", 0.5), n("A4", 0.5), n("D5", 0.5), n("A4", 1), r(1)],
            [n("Bb4", 1), n("Eb4", 1), n("Ab4", 1), r(1)],
            [n("D4", 1), n("A4", 1), n("G4", 1), r(1)],
            [n("E4", 1), n("G4", 1), n("A4", 1), n("D4", 1)],
            [n("F4", 1), n("A4", 1), n("G4", 1), r(1)],
            [n("Bb3", 1), n("C4", 1), n("F4", 1), r(1)],
            [n("D5", 0.5), n("A4", 0.5), n("G4", 1), n("E4", 1), r(1)],
            [n("Eb4", 1), n("Ab4", 1), n("Db4", 1), r(1)],
            [n("E4", 0.5), n("G4", 0.5), n("A4", 1), n("D5", 1), r(1)],
            [n("D4", 1), n("A4", 0.5), n("G4", 0.5), n("E4", 1), r(1)],
        ]
        return lines[bar % 10]
    if sec == "D":
        if bar < 16:
            return [n("E4", 2), n("G4", 1), r(1)]
        return [r(4)]
    if sec == "E":
        if bar < 6:
            return [n("E4", 2), r(2)]
        if bar == 14:
            return [r(4)]
        return [r(4)]
    return [r(4)]

# === CELLO: Unison at m.40 ===
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
        if m == 40:
            return [n("E2", 1), r(3)]
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
        if bar in (26, 27, 28):
            return [n("E2", 2), r(2)]
        lines = [
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("Bb1", 1), n("Eb2", 1), n("Ab2", 1), r(1)],
            [n("D2", 1), n("A2", 1), n("G2", 1), r(1)],
            [n("E2", 2), n("A2", 1), r(1)],
            [n("F2", 1), n("C3", 1), n("Bb2", 1), r(1)],
            [n("G2", 2), n("C3", 1), r(1)],
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("Bb1", 1), n("Eb2", 1), n("Ab2", 1), r(1)],
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("D2", 1), n("A2", 1), n("G2", 1), r(1)],
        ]
        return lines[bar % 10]
    if sec == "D":
        if bar < 14:
            return [n("E2", 2), r(1), n("A2", 1)]
        if bar < 20:
            return [n("E2", 2), r(2)]
        return [r(4)]
    if sec == "E":
        if bar == 14:
            return [r(4)]
        return [n("E2", 4)]
    return [r(4)]

# === TEXTURE ===
def use_reduced_texture(m, sec):
    if sec == "A":
        return m in (3, 4, 7, 8, 12, 13, 17)
    if sec == "B":
        return m in (22, 23, 28, 29, 35, 36)
    if sec == "C":
        return m in (48, 49, 58, 59, 68, 69, 78, 79)
    if sec == "D":
        return m >= 98
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

    section_starts = [1, 19, 41, 87, 107]
    section_labels = ["A", "B", "C", "D", "E"]
    section_double_barlines = [18, 40, 86, 106]

    for m in range(1, 123):
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
        elif m == 87:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 107:
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
    out_dir = os.path.join(base, "..", "musicxml")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "V3_Labyrinth_of_Quiet_Motions_Master.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")

if __name__ == "__main__":
    main()
