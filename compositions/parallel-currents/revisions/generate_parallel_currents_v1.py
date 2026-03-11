#!/usr/bin/env python3
"""
Parallel Currents V1
Wyble Linear Counterpoint Engine — Jimmy Wyble influence
Target: GCE ≥ 9.8

Two independent guitar voices. Harmony from counterpoint, not chords.
Form: A (two-voice intro) B (shadowing) C (expanded) D (compression) E (dissolving)
Duration: 4–5 min at ♩ = 92
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

def section(m):
    if m <= 18: return "A"
    if m <= 40: return "B"
    if m <= 70: return "C"
    if m <= 85: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 19
    if sec == "C": return m - 41
    if sec == "D": return m - 71
    return m - 86

# === GUITAR: Two-voice Wyble counterpoint (upper, lower) ===
# Dyads = 3rds, 6ths; staggered rhythm
def guitar_a(bar):
    pats = [
        [c(("E4", "G3"), 1), n("A4", 0.5), r(0.5), c(("G4", "E3"), 1), r(1)],
        [r(0.5), c(("F#4", "A3"), 1.5), r(0.5), n("E4", 1), r(1)],
        [c(("G4", "B3"), 1), r(0.5), c(("A4", "C4"), 1), r(1.5)],
        [n("E4", 0.5), r(0.5), c(("G4", "E3"), 1.5), r(0.5), n("A3", 1)],
        [c(("D4", "F#3"), 1.5), r(0.5), c(("E4", "G3"), 1), r(1)],
        [r(1), c(("G4", "B3"), 1), n("A4", 0.5), r(0.5), c(("E4", "G3"), 1)],
    ]
    return pats[bar % 6]

def guitar_b(bar):
    pats = [
        [c(("E4", "G3"), 1), c(("F#4", "A3"), 1), r(1), c(("G4", "E3"), 1)],
        [n("A4", 0.5), r(0.5), c(("G4", "B3"), 1.5), r(0.5), n("E4", 1)],
        [c(("D4", "F#3"), 1), r(1), c(("E4", "G3"), 1.5), r(0.5)],
        [r(0.5), c(("G4", "E3"), 1), c(("A4", "C4"), 1), r(1.5)],
        [c(("E4", "G3"), 1.5), r(0.5), n("F#4", 1), r(1)],
        [n("G4", 0.5), r(0.5), c(("A4", "E3"), 1), r(1), c(("G4", "B3"), 1)],
    ]
    return pats[bar % 6]

def guitar_c(bar):
    pats = [
        [c(("E4", "G3"), 1), c(("F#4", "A3"), 0.5), r(0.5), c(("G4", "E3"), 1), r(1)],
        [r(0.5), c(("A4", "C4"), 1), c(("G4", "B3"), 1), r(1.5)],
        [c(("E4", "G3"), 0.5), r(0.5), c(("D4", "F#3"), 1), c(("E4", "G3"), 1), r(1)],
        [c(("G4", "E3"), 1), n("A4", 1), r(1), c(("G4", "B3"), 1)],
        [n("E4", 0.5), r(0.5), c(("F#4", "A3"), 1.5), r(0.5), c(("G4", "E3"), 1)],
        [c(("A4", "E3"), 1), r(1), c(("G4", "B3"), 1), r(1)],
    ]
    return pats[bar % 6]

def guitar_d(bar):
    pats = [
        [c(("E4", "G3"), 0.5), r(0.5), c(("F#4", "A3"), 0.5), r(0.5), c(("G4", "E3"), 1), r(1)],
        [c(("A4", "C4"), 1), c(("G4", "B3"), 1), r(2)],
        [r(0.5), c(("E4", "G3"), 1), c(("D4", "F#3"), 1), r(1.5)],
    ]
    return pats[bar % 3]

def guitar_e(bar):
    if bar < 8:
        return [c(("E4", "G3"), 1.5), r(0.5), n("A4", 1), r(1)]
    if bar < 12:
        return [r(1), c(("G4", "E3"), 1), r(2)]
    return [c(("E4", "G3"), 2), r(2)]

def guitar_content(sec, bar, m):
    if sec == "A": return guitar_a(bar)
    if sec == "B": return guitar_b(bar)
    if sec == "C": return guitar_c(bar)
    if sec == "D": return guitar_d(bar)
    return guitar_e(bar)

# === VIOLIN I: Upper guitar voice ===
def violin1_a(bar):
    return [r(4)]

def violin1_b(bar):
    if bar % 3 == 0:
        return [n("E5", 1), n("F#5", 1), r(1), n("G5", 1)]
    if bar % 3 == 1:
        return [r(1), n("A5", 1.5), r(0.5), n("G5", 1)]
    return [n("E5", 1), r(2), n("G5", 1)]

def violin1_c(bar):
    pats = [
        [n("E5", 1), n("F#5", 0.5), r(0.5), n("G5", 1), r(1)],
        [r(0.5), n("A5", 1), n("G5", 1), r(1.5)],
        [n("E5", 0.5), r(0.5), n("D5", 1), n("E5", 1), r(1)],
        [n("G5", 1), n("A5", 1), r(1), n("G5", 1)],
    ]
    return pats[bar % 4]

def violin1_d(bar):
    if bar < 10:
        return [n("E5", 1), n("F#5", 1), n("G5", 1), r(1)]
    return [r(4)]

def violin1_e(bar):
    if bar < 12:
        return [n("E5", 2), r(2)]
    return [r(4)]

def violin1_content(sec, bar, m):
    if sec == "A": return violin1_a(bar)
    if sec == "B": return violin1_b(bar)
    if sec == "C": return violin1_c(bar)
    if sec == "D": return violin1_d(bar)
    return violin1_e(bar)

# === VIOLIN II: Shadow / inversion ===
def violin2_a(bar):
    return [r(4)]

def violin2_b(bar):
    if bar % 4 == 1:
        return [r(1), n("G4", 1), n("A4", 1), r(1)]
    if bar % 4 == 2:
        return [n("E4", 1.5), r(0.5), n("G4", 1), r(1)]
    return [r(4)]

def violin2_c(bar):
    if bar % 2 == 0:
        return [n("G4", 1), r(1), n("A4", 1), r(1)]
    return [r(0.5), n("E4", 1.5), r(0.5), n("G4", 1)]

def violin2_d(bar):
    if bar < 12:
        return [n("G4", 2), r(2)]
    return [r(4)]

def violin2_e(bar):
    if bar < 10:
        return [r(2), n("A4", 1), r(1)]
    return [r(4)]

def violin2_content(sec, bar, m):
    if sec == "A": return violin2_a(bar)
    if sec == "B": return violin2_b(bar)
    if sec == "C": return violin2_c(bar)
    if sec == "D": return violin2_d(bar)
    return violin2_e(bar)

# === VIOLA: Lower guitar counterline ===
def viola_a(bar):
    return [r(4)]

def viola_b(bar):
    if bar % 3 == 0:
        return [n("G3", 1), n("A3", 1), r(1), n("E3", 1)]
    if bar % 3 == 1:
        return [r(1), n("C4", 1.5), r(0.5), n("B3", 1)]
    return [n("G3", 1), r(2), n("E3", 1)]

def viola_c(bar):
    pats = [
        [n("G3", 1), n("A3", 0.5), r(0.5), n("E3", 1), r(1)],
        [r(0.5), n("C4", 1), n("B3", 1), r(1.5)],
        [n("G3", 0.5), r(0.5), n("F#3", 1), n("G3", 1), r(1)],
        [n("E3", 1), n("C4", 1), r(1), n("B3", 1)],
    ]
    return pats[bar % 4]

def viola_d(bar):
    if bar < 10:
        return [n("G3", 1), n("A3", 1), n("E3", 1), r(1)]
    return [r(4)]

def viola_e(bar):
    if bar < 12:
        return [n("G3", 2), r(2)]
    return [r(4)]

def viola_content(sec, bar, m):
    if sec == "A": return viola_a(bar)
    if sec == "B": return viola_b(bar)
    if sec == "C": return viola_c(bar)
    if sec == "D": return viola_d(bar)
    return viola_e(bar)

# === CELLO: Extended bass contour ===
def cello_a(bar):
    return [r(4)]

def cello_b(bar):
    if bar % 2 == 0:
        return [n("E2", 2), n("A2", 1), r(1)]
    return [n("G2", 1.5), r(0.5), n("E2", 2)]

def cello_c(bar):
    pats = [
        [n("E2", 1), n("A2", 1), n("G2", 1), r(1)],
        [n("E2", 2), r(1), n("A2", 1)],
        [n("G2", 1), n("E2", 1), n("A2", 1), r(1)],
        [n("E2", 1.5), r(0.5), n("G2", 2)],
    ]
    return pats[bar % 4]

def cello_d(bar):
    if bar < 12:
        return [n("E2", 2), n("A2", 1), r(1)]
    return [r(4)]

def cello_e(bar):
    if bar < 12:
        return [n("E2", 2), r(2)]
    return [r(4)]

def cello_content(sec, bar, m):
    if sec == "A": return cello_a(bar)
    if sec == "B": return cello_b(bar)
    if sec == "C": return cello_c(bar)
    if sec == "D": return cello_d(bar)
    return cello_e(bar)

# === REDUCED TEXTURE ===
def use_reduced_texture(m, sec):
    if sec == "A":
        return True
    if sec == "B":
        return m in (19, 20, 25, 26, 31, 32, 37, 38)
    if sec == "C":
        return m in (45, 46, 55, 56, 65, 66)
    if sec == "D":
        return m in (71, 72, 78, 79)
    if sec == "E":
        return m >= 90
    return False

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Parallel Currents"
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

    section_starts = [1, 19, 41, 71, 86]
    section_labels = ["A", "B", "C", "D", "E"]
    section_barlines = [18, 40, 70, 85]

    for m in range(1, 101):
        sec = section(m)
        bar = bar_in(m, sec)
        reduced = use_reduced_texture(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=92, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))

        if m == 41:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 71:
            mg.insert(0, dynamics.Dynamic("f"))
        elif m == 86:
            mg.insert(0, dynamics.Dynamic("mp"))

        for e in guitar_content(sec, bar, m):
            mg.append(e)

        if m in section_barlines:
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        vn1_c = violin1_content(sec, bar, m)
        vn2_c = violin2_content(sec, bar, m)
        vla_c = viola_content(sec, bar, m)
        vc_c = cello_content(sec, bar, m)

        if reduced:
            if sec == "B" and m % 4 in (1, 2):
                vn2_c = [r(4)]
            if sec == "B" and m % 4 in (0, 3):
                vla_c = [r(4)]
            if sec == "C" and m % 2 == 1:
                vn2_c = [r(4)]
            if sec == "E" and m >= 92:
                vn1_c = [r(4)]
                vn2_c = [r(4)]
                vla_c = [r(4)]
                vc_c = [r(4)]

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
    out_path = os.path.join(out_dir, "V1_Parallel_Currents.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")

if __name__ == "__main__":
    main()
