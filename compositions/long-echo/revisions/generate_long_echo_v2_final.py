#!/usr/bin/env python3
"""
Long Echo V2 Final
Refinement of V1 — GCE 9.8+

Refinements:
- Section C: modal shift, inner-voice semitone motion, subtle cello bass movement
- Pre-ending: 3 measures thinning (Vn2 → Viola → Guitar), then Vn1 + Cello suspended, then final
- Motivic recall: D-E-A cell near end (violin I, guitar dyad, cello stepwise)
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

# === MOTIVIC SEED: D-E (M2), E-A (P4), A-C (m3) ===
MOTIVE = [("D4", "E4"), ("E4", "A4"), ("A3", "C4"), ("D3", "A3")]

def section(m):
    if m <= 12: return "A"
    if m <= 26: return "B"
    if m <= 45: return "C"
    if m <= 55: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 13
    if sec == "C": return m - 27
    if sec == "D": return m - 46
    return m - 56

# === GUITAR ===
def guitar_a(bar):
    if bar in (0, 1, 4, 5):
        return [c(("D3", "A3"), 2), r(2)]
    if bar in (2, 3):
        return [c(("E3", "B3"), 2), r(2)]
    if bar in (6, 7):
        return [c(("D3", "F#3", "A3"), 3), r(1)]
    if bar in (8, 9):
        return [r(1), c(("E3", "A3"), 2), r(1)]
    return [c(("D3", "A3"), 2), r(2)]

def guitar_b(bar):
    frags = [
        [c(("D3", "A3", "F#4"), 3), r(1)],
        [c(("E3", "B3"), 2), r(2)],
        [c(("G3", "D4"), 2), r(2)],
        [c(("D3", "A3"), 2), c(("E3", "A3"), 1), r(1)],
        [c(("A2", "E3", "G3"), 3), r(1)],
        [c(("D3", "A3"), 4)],
        [r(2), c(("E3", "B3"), 2)],
        [c(("G3", "A3", "D4"), 2), r(2)],
    ]
    return frags[bar % 8]

def guitar_c(bar):
    """C: Modal shift, inner-voice semitone motion"""
    frags = [
        [c(("D3", "A3", "F#4"), 1), c(("Eb3", "Bb3"), 1), r(2)],
        [c(("E3", "G#3", "B3"), 2), r(2)],
        [c(("D3", "A3"), 2), c(("C3", "G3"), 2)],
        [c(("A2", "E3"), 2), c(("Bb2", "F3"), 1), r(1)],
        [c(("Eb3", "Bb3"), 2), c(("D3", "A3"), 1), r(1)],
        [c(("D3", "F#3", "A3"), 2), c(("Eb3", "Bb3"), 1), r(1)],
        [r(1), c(("E3", "A3"), 2), r(1)],
        [c(("G3", "B3", "D4"), 1), c(("F#3", "C#4"), 1), r(2)],
        [c(("D3", "A3"), 2), c(("Eb3", "Bb3"), 1), r(1)],
        [c(("A2", "E3"), 2), n("F3", 1), r(1)],
    ]
    return frags[bar % 10]

def guitar_d(bar):
    if bar < 5:
        return [c(("D3", "A3"), 2), r(2)]
    if bar < 8:
        return [r(2), c(("E3", "A3"), 2)]
    return [c(("D3", "A3"), 3), r(1)]

def guitar_e(bar):
    """E: Motivic recall + pre-ending dissolution"""
    if bar < 4:
        return [c(("D3", "A3"), 2), r(2)]
    if bar < 7:
        return [r(2), c(("E3", "B3"), 2)]
    if bar < 10:
        return [c(("D3", "A3"), 2), r(2)]
    if bar == 10:
        return [r(4)]
    if bar == 11:
        return [r(4)]
    if bar == 12:
        return [c(("D3", "A3"), 4)]
    return [c(("D3", "A3"), 4)]

def guitar_content(sec, bar, m):
    if sec == "A": return guitar_a(bar)
    if sec == "B": return guitar_b(bar)
    if sec == "C": return guitar_c(bar)
    if sec == "D": return guitar_d(bar)
    return guitar_e(bar)

# === VIOLIN I ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if bar in (2, 5, 8):
            return [n("E6", 4)]
        if bar in (4, 7):
            return [n("A5", 3), r(1)]
        return [r(4)]
    if sec == "B":
        if bar % 3 == 0:
            return [n("F#5", 2), r(2)]
        if bar % 4 == 1:
            return [n("E5", 3), r(1)]
        return [r(4)]
    if sec == "C":
        if bar % 2 == 0:
            return [n("A5", 2), n("G5", 1), r(1)]
        if bar % 3 == 1:
            return [n("B5", 3), r(1)]
        if bar in (6, 7):
            return [n("Bb5", 2), n("A5", 1), r(1)]
        return [r(4)]
    if sec == "D":
        if bar < 5:
            return [n("E5", 2), r(2)]
        return [r(4)]
    if sec == "E":
        if bar < 3:
            return [n("E6", 4)]
        if bar < 6:
            return [r(4)]
        if bar < 10:
            return [n("E6", 4)]
        if bar == 10:
            return [n("D6", 1), n("E6", 1), n("A5", 1), r(1)]
        if bar == 11:
            return [n("E6", 4)]
        return [n("E6", 4)]

# === VIOLIN II: Drops first in pre-ending ===
def violin2_content(sec, bar, m):
    if sec == "A":
        return [r(4)]
    if sec == "B":
        if bar in (2, 5, 8):
            return [r(1), n("D5", 2), r(1)]
        return [r(4)]
    if sec == "C":
        if bar % 3 == 0:
            return [n("A4", 2), r(2)]
        if bar % 4 == 2:
            return [r(2), n("E5", 2)]
        if bar in (6, 7):
            return [r(1), n("Bb4", 2), r(1)]
        return [r(4)]
    if sec == "D":
        if bar < 6:
            return [n("D5", 2), r(2)]
        return [r(4)]
    if sec == "E":
        if bar < 4:
            return [r(2), n("A5", 2)]
        if bar < 11:
            return [r(2), n("A5", 2)]
        return [r(4)]

# === VIOLA: Drops second in pre-ending ===
def viola_content(sec, bar, m):
    if sec == "A":
        if bar in (3, 6, 9):
            return [n("A3", 2), n("B3", 1), r(1)]
        return [r(4)]
    if sec == "B":
        if bar % 2 == 0:
            return [n("D4", 2), r(2)]
        if bar % 3 == 1:
            return [n("E4", 2), n("F#4", 1), r(1)]
        return [r(4)]
    if sec == "C":
        if bar % 2 == 0:
            return [n("A3", 1), n("Bb3", 1), n("B3", 1), r(1)]
        if bar in (5, 7):
            return [n("Eb4", 2), n("D4", 1), r(1)]
        return [r(4)]
    if sec == "D":
        if bar < 7:
            return [n("D4", 3), r(1)]
        return [r(4)]
    if sec == "E":
        if bar < 10:
            return [n("A3", 2), n("B3", 1), r(1)]
        return [r(4)]

# === CELLO: Subtle bass movement in C; motivic recall in E ===
def cello_content(sec, bar, m):
    if sec == "A":
        return [n("D2", 4)]
    if sec == "B":
        if bar % 4 == 0:
            return [n("D2", 2), n("A2", 2)]
        return [n("D2", 4)]
    if sec == "C":
        if bar % 4 == 0:
            return [n("D2", 1), n("Eb2", 1), n("D2", 1), r(1)]
        if bar % 5 == 2:
            return [n("A2", 2), n("E2", 2)]
        if bar in (6, 7):
            return [n("Bb1", 2), n("D2", 2)]
        return [n("D2", 4)]
    if sec == "D":
        return [n("D2", 4)]
    if sec == "E":
        if bar < 10:
            return [n("D2", 4)]
        if bar == 10:
            return [n("D2", 1), n("E2", 1), n("A2", 1), r(1)]
        return [n("D2", 4)]

# === PRE-ENDING: bars 63-65 = Vn2 out, Vla out, Gtr out; 66 = Vn1+Vc; 67 = final ===
def is_pre_ending_dissolution(m):
    return 63 <= m <= 67

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Long Echo"
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

    section_starts = [1, 13, 27, 46, 56]
    section_labels = ["A", "B", "C", "D", "E"]
    section_barlines = [12, 26, 45, 55, 66]

    for m in range(1, 68):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=52, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("pp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))

        if m == 27:
            mg.insert(0, dynamics.Dynamic("p"))
        elif m == 35:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 38:
            mg.insert(0, dynamics.Dynamic("p"))
        elif m == 46:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 56:
            mg.insert(0, dynamics.Dynamic("pp"))
        elif m == 63:
            mg.insert(0, dynamics.Dynamic("pp"))

        for e in guitar_content(sec, bar, m):
            mg.append(e)

        if m in section_barlines:
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        vn1_c = violin1_content(sec, bar, m)
        vn2_c = violin2_content(sec, bar, m)
        vla_c = viola_content(sec, bar, m)
        vc_c = cello_content(sec, bar, m)

        if is_pre_ending_dissolution(m):
            if m == 63:
                vn2_c = [r(4)]
            elif m == 64:
                vn2_c = [r(4)]
                vla_c = [r(4)]
            elif m == 65:
                vn2_c = [r(4)]
                vla_c = [r(4)]
            elif m == 66:
                vn2_c = [r(4)]
                vla_c = [r(4)]

        reduced = (
            (sec == "A" and m in (1, 2, 3, 6, 7, 10, 11)) or
            (sec == "B" and m in (14, 15, 20, 21, 24, 25)) or
            (sec == "C" and m in (28, 29, 34, 35, 40, 41)) or
            (sec == "D" and m >= 50) or
            (sec == "E")
        )
        if reduced and not is_pre_ending_dissolution(m):
            if m % 3 == 0:
                vn2_c = [r(4)]
            if m % 3 == 1 and sec != "A":
                vla_c = [r(4)]
            if m % 3 == 2 and sec != "A":
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
    out_path = os.path.join(out_dir, "V2_Long_Echo_Final.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")

if __name__ == "__main__":
    main()
