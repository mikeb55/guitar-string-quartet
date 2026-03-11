#!/usr/bin/env python3
"""
Shifting Frames V2 Final – Refinement Pass
Loads V1, applies focused refinements, exports V2_Shifting_Frames_Final.musicxml

Refinements:
1. Extend Section C polymetric core by 5 measures
2. Add rhythmic cell transformation (inverted accent 2+3+3) near climax
3. Add 3 measures to fragmented ending
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

# === SECTION BOUNDARIES (V2) ===
# A: 1-24, B: 25-52, C: 53-96 (+5), D: 97-115, E: 116-138 (+3)
def section(m):
    if m <= 24: return "A"
    if m <= 52: return "B"
    if m <= 96: return "C"
    if m <= 115: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 25
    if sec == "C": return m - 53
    if sec == "D": return m - 97
    return m - 116

# === GUITAR ===
def guitar_a(bar):
    if bar % 4 == 0:
        return [c(("D3", "A3"), 1.5), r(0.5), c(("E3", "G3"), 1.5), r(0.5)]
    if bar % 4 == 1:
        return [r(0.5), c(("D3", "A3"), 1.5), r(0.5), c(("G3", "B3"), 1.5)]
    if bar % 4 == 2:
        return [c(("E3", "A3"), 1), r(1), c(("D3", "F#3"), 1), r(1)]
    return [r(1), c(("D3", "A3"), 1.5), r(0.5), c(("E3", "G3"), 1)]

def guitar_b(bar):
    pats = [
        [c(("D3", "A3"), 1.5), r(0.5), c(("E3", "G3"), 1.5), r(0.5)],
        [r(0.5), c(("G3", "D4"), 1.5), r(0.5), c(("D3", "A3"), 1.5)],
        [c(("E3", "A3"), 1), c(("D3", "F#3"), 1), r(2)],
        [r(1), c(("D3", "A3"), 1.5), r(0.5), c(("E3", "B3"), 1)],
        [c(("D3", "G3"), 0.5), r(0.5), c(("A3", "D4"), 0.5), r(0.5), c(("E3", "G3"), 1), r(1)],
        [r(0.5), c(("D3", "A3"), 1.5), r(1), c(("G3", "B3"), 1)],
    ]
    return pats[bar % 6]

def guitar_c(bar):
    # Extended C: bars 39-43 get denser interlock with cello
    if bar >= 39:
        ext_pats = [
            [c(("D3", "A3"), 0.5), r(0.5), c(("E3", "G3"), 0.5), r(0.5), c(("D3", "A3"), 0.5), r(0.5), c(("G3", "B3"), 0.5), r(0.5)],
            [r(0.5), c(("D3", "F#3"), 1), c(("G3", "B3"), 1), r(1.5)],
            [c(("E3", "A3"), 0.5), r(0.5), c(("D3", "A3"), 0.5), r(0.5), c(("G3", "D4"), 1), r(1)],
            [c(("D3", "A3"), 1), r(0.5), c(("E3", "G3"), 1), r(0.5), c(("D3", "A3"), 1)],
            [r(0.5), c(("G3", "B3"), 1.5), r(0.5), c(("D3", "A3"), 1.5)],
        ]
        return ext_pats[bar - 39]
    pats = [
        [c(("D3", "A3"), 1.5), r(0.5), c(("E3", "G3"), 1.5), r(0.5)],
        [r(0.5), c(("D3", "F#3"), 1), c(("G3", "B3"), 1), r(1.5)],
        [c(("E3", "A3"), 0.5), r(0.5), c(("D3", "A3"), 0.5), r(0.5), c(("G3", "D4"), 1), r(1)],
        [c(("D3", "A3"), 1), r(0.5), c(("E3", "G3"), 1), r(0.5), c(("D3", "A3"), 1)],
        [r(0.5), c(("G3", "B3"), 1.5), r(0.5), c(("D3", "A3"), 1.5)],
        [c(("D3", "A3"), 0.5), r(0.5), c(("E3", "A3"), 0.5), r(0.5), c(("D3", "G3"), 0.5), r(0.5), c(("A3", "D4"), 0.5), r(0.5)],
    ]
    return pats[bar % 6]

def guitar_d(bar):
    if bar < 10:
        return [c(("D3", "A3"), 0.5), r(0.5), c(("E3", "G3"), 0.5), r(0.5), c(("D3", "A3"), 1), r(1)]
    return [r(1), c(("D3", "A3"), 1), r(2)]

def guitar_e(bar):
    if bar < 8:
        return [c(("D3", "A3"), 1.5), r(2.5)]
    if bar < 17:
        return [r(2), c(("E3", "G3"), 1), r(1)]
    # Extended fragmentation: bars 17-22
    if bar < 20:
        return [r(3), c(("D3", "A3"), 0.5), r(0.5)]
    if bar < 22:
        return [r(4)]
    return [r(4)]

def guitar_content(sec, bar, m):
    if sec == "A": return guitar_a(bar)
    if sec == "B": return guitar_b(bar)
    if sec == "C": return guitar_c(bar)
    if sec == "D": return guitar_d(bar)
    return guitar_e(bar)

# === VIOLIN I: Extended C with clearer rotation; transformed cell (2+3+3) in bar 41 ===
def violin1_a(bar):
    if bar % 3 == 0:
        return [n("E5", 1.5), r(0.5), n("G5", 1.5), r(0.5)]
    if bar % 3 == 1:
        return [r(0.5), n("A5", 1.5), r(0.5), n("E5", 1.5)]
    return [n("G5", 1), r(1), n("A5", 1), r(1)]

def violin1_b(bar):
    pats = [
        [n("E5", 1.5), r(0.5), n("G5", 1.5), r(0.5)],
        [r(1), n("A5", 1.5), r(0.5), n("E5", 1)],
        [n("G5", 0.5), r(0.5), n("A5", 1.5), r(0.5), n("E5", 0.5), r(0.5)],
        [r(0.5), n("E5", 1.5), r(0.5), n("G5", 1.5)],
        [n("A5", 1), r(1), n("G5", 1), r(1)],
        [n("E5", 0.5), r(0.5), n("G5", 0.5), r(0.5), n("A5", 1), r(1)],
    ]
    return pats[bar % 6]

def violin1_c(bar):
    # TRANSFORMED CELL (2+3+3 inverted accent) in bar 41 – Violin I carries it
    if bar == 41:
        return [n("E5", 1), r(0.5), n("G5", 1.5), r(0.5), n("A5", 1.5), r(0.5)]
    if bar >= 39:
        ext_pats = [
            [n("E5", 0.5), r(0.5), n("G5", 0.5), r(0.5), n("A5", 0.5), r(0.5), n("E5", 0.5), r(0.5)],
            [n("G5", 1), n("A5", 1), n("E5", 1), r(1)],
            [r(1), n("E5", 1.5), r(0.5), n("G5", 1)],
            [n("A5", 0.5), r(0.5), n("E5", 1.5), r(0.5), n("G5", 1)],
            [n("E5", 1), n("G5", 1), n("A5", 1), r(1)],
        ]
        idx = bar - 39 if bar < 41 else bar - 40
        return ext_pats[idx % 5]
    pats = [
        [n("E5", 1.5), r(0.5), n("G5", 1.5), r(0.5)],
        [r(0.5), n("A5", 1.5), r(0.5), n("E5", 1.5)],
        [n("G5", 0.5), r(0.5), n("A5", 0.5), r(0.5), n("E5", 0.5), r(0.5), n("G5", 0.5), r(0.5)],
        [n("E5", 1), n("G5", 1), n("A5", 1), r(1)],
        [r(1), n("E5", 1.5), r(0.5), n("G5", 1)],
        [n("A5", 0.5), r(0.5), n("E5", 1.5), r(0.5), n("G5", 1)],
    ]
    return pats[bar % 6]

def violin1_d(bar):
    if bar < 12:
        return [n("E5", 0.5), r(0.5), n("G5", 0.5), r(0.5), n("A5", 1), r(1)]
    return [r(4)]

def violin1_e(bar):
    if bar < 12:
        return [n("E5", 1.5), r(2.5)]
    if bar < 20:
        return [r(3), n("E5", 0.5), r(0.5)]
    return [r(4)]

def violin1_content(sec, bar, m):
    if sec == "A": return violin1_a(bar)
    if sec == "B": return violin1_b(bar)
    if sec == "C": return violin1_c(bar)
    if sec == "D": return violin1_d(bar)
    return violin1_e(bar)

# === VIOLIN II ===
def violin2_a(bar):
    if bar % 4 in (1, 3):
        return [r(1), n("C5", 1.5), r(0.5), n("E5", 1)]
    return [r(4)]

def violin2_b(bar):
    if bar % 3 == 0:
        return [r(0.5), n("G4", 1.5), r(0.5), n("A4", 1.5)]
    if bar % 3 == 1:
        return [n("E5", 1), r(1), n("G4", 1), r(1)]
    return [r(1.5), n("A4", 1.5), r(1)]

def violin2_c(bar):
    if bar >= 39:
        ext_pats = [
            [n("G4", 0.5), r(0.5), n("A4", 1.5), r(0.5), n("E5", 1)],
            [r(0.5), n("E5", 1.5), r(0.5), n("G4", 1.5)],
            [n("A4", 0.5), r(0.5), n("E5", 1), r(0.5), n("G4", 1), r(1)],
            [r(1), n("G4", 1.5), r(0.5), n("A4", 1)],
            [n("E5", 1), r(1), n("G4", 0.5), r(0.5), n("A4", 1)],
        ]
        return ext_pats[(bar - 39) % 5]
    if bar % 2 == 0:
        return [n("G4", 0.5), r(0.5), n("A4", 1.5), r(0.5), n("E5", 1)]
    return [r(0.5), n("E5", 1.5), r(0.5), n("G4", 1.5)]

def violin2_d(bar):
    if bar < 14:
        return [r(1), n("G4", 1), r(2)]
    return [r(4)]

def violin2_e(bar):
    if bar < 10:
        return [r(2), n("A4", 1), r(1)]
    if bar < 18:
        return [r(3.5), n("G4", 0.5)]
    return [r(4)]

def violin2_content(sec, bar, m):
    if sec == "A": return violin2_a(bar)
    if sec == "B": return violin2_b(bar)
    if sec == "C": return violin2_c(bar)
    if sec == "D": return violin2_d(bar)
    return violin2_e(bar)

# === VIOLA ===
def viola_a(bar):
    if bar % 4 in (0, 2):
        return [n("A3", 1.5), r(0.5), n("B3", 1.5), r(0.5)]
    return [r(4)]

def viola_b(bar):
    if bar % 2 == 0:
        return [n("E4", 1), r(1), n("G4", 1), r(1)]
    return [r(0.5), n("A4", 1.5), r(0.5), n("G4", 1.5)]

def viola_c(bar):
    if bar >= 39:
        return [n("A3", 0.5), r(0.5), n("B3", 1.5), r(0.5), n("E4", 1)]
    return [n("A3", 0.5), r(0.5), n("B3", 1.5), r(0.5), n("E4", 1)]

def viola_d(bar):
    if bar < 14:
        return [n("E4", 1.5), r(2.5)]
    return [r(4)]

def viola_e(bar):
    if bar < 12:
        return [r(1), n("A3", 1), r(2)]
    if bar < 19:
        return [r(2.5), n("B3", 0.5), r(1)]
    return [r(4)]

def viola_content(sec, bar, m):
    if sec == "A": return viola_a(bar)
    if sec == "B": return viola_b(bar)
    if sec == "C": return viola_c(bar)
    if sec == "D": return viola_d(bar)
    return viola_e(bar)

# === CELLO: Extended C with stronger interlock with guitar ===
def cello_a(bar):
    if bar % 2 == 0:
        return [n("D2", 2), n("A2", 1), r(1)]
    return [n("E2", 1.5), r(0.5), n("A2", 2)]

def cello_b(bar):
    pats = [
        [n("D2", 1.5), r(0.5), n("A2", 1.5), r(0.5)],
        [n("E2", 2), r(1), n("A2", 1)],
        [n("D2", 1), n("G2", 1), n("A2", 1), r(1)],
        [n("E2", 1.5), r(0.5), n("D2", 2)],
    ]
    return pats[bar % 4]

def cello_c(bar):
    # Extended C: denser interlock with guitar
    if bar >= 39:
        ext_pats = [
            [n("D2", 0.5), r(0.5), n("A2", 1.5), r(0.5), n("E2", 1)],
            [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("D2", 0.5), r(0.5), n("A2", 0.5), r(0.5), n("E2", 0.5), r(0.5), n("A2", 0.5), r(0.5)],
            [n("E2", 1.5), r(0.5), n("D2", 2)],
            [n("D2", 1), n("G2", 1), n("A2", 1), r(1)],
        ]
        return ext_pats[bar - 39]
    pats = [
        [n("D2", 1.5), r(0.5), n("A2", 1.5), r(0.5)],
        [n("E2", 1), n("A2", 1), n("D2", 1), r(1)],
        [n("D2", 0.5), r(0.5), n("A2", 1.5), r(0.5), n("E2", 1)],
        [n("E2", 1.5), r(0.5), n("D2", 2)],
    ]
    return pats[bar % 4]

def cello_d(bar):
    if bar < 16:
        return [n("D2", 2), r(2)]
    return [r(4)]

def cello_e(bar):
    if bar < 16:
        return [n("D2", 2), r(2)]
    if bar < 21:
        return [n("D2", 1.5), r(2.5)]
    return [r(4)]

def cello_content(sec, bar, m):
    if sec == "A": return cello_a(bar)
    if sec == "B": return cello_b(bar)
    if sec == "C": return cello_c(bar)
    if sec == "D": return cello_d(bar)
    return cello_e(bar)

# === UNISON MOMENTS ===
def is_unison_bar(m):
    return m in (53, 69, 85)

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Shifting Frames"
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

    section_starts = [1, 25, 53, 97, 116]
    section_labels = ["A", "B", "C", "D", "E"]
    section_barlines = [24, 52, 96, 115]

    for m in range(1, 139):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=104, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mf"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))

        if m == 53:
            mg.insert(0, dynamics.Dynamic("f"))
        elif m == 97:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 116:
            mg.insert(0, dynamics.Dynamic("p"))

        g_content = guitar_content(sec, bar, m)
        if is_unison_bar(m):
            g_content = [c(("E3", "G3"), 0.5), r(3.5)]
        for e in g_content:
            mg.append(e)

        if m in section_barlines:
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        vn1_c = violin1_content(sec, bar, m)
        vn2_c = violin2_content(sec, bar, m)
        vla_c = viola_content(sec, bar, m)
        vc_c = cello_content(sec, bar, m)

        if is_unison_bar(m):
            vn1_c = [n("E5", 0.5), r(3.5)]
            vn2_c = [n("E5", 0.5), r(3.5)]
            vla_c = [n("E4", 0.5), r(3.5)]
            vc_c = [n("E2", 0.5), r(3.5)]

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
    out_path = os.path.join(out_dir, "V2_Shifting_Frames_Final.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")
    print("Refinements: +5 measures C, transformed cell (2+3+3), +3 measures E.")

if __name__ == "__main__":
    main()
