#!/usr/bin/env python3
"""
Northern Letters V1
Metheny–Bacharach Lyrical Architecture Engine
Target: GCE ≥ 9.8

Floating lyrical chamber music. Melodic landscape unfolding slowly.
Form: A (guitar theme) B (strings inherit) C (harmonic surprise) D (climax) E (quiet return)
Duration: 4–5 min at ♩ = 88
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

# === SECTION BOUNDARIES ===
# A: 1-24, B: 25-48, C: 49-72, D: 73-96, E: 97-110
def section(m):
    if m <= 24: return "A"
    if m <= 48: return "B"
    if m <= 72: return "C"
    if m <= 96: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 25
    if sec == "C": return m - 49
    if sec == "D": return m - 73
    return m - 97

# === GUITAR: Melodic catalyst, sustained lyrical, gentle dyads ===
# A: Guitar + cello duet, introduces theme (stepwise, target 3rd/6th/maj7)
def guitar_a(bar):
    # Lyrical 8-bar phrases, stepwise with occasional leap
    phrase = bar % 8
    if phrase == 0:
        return [n("E4", 2), n("G4", 1), n("A4", 1)]
    if phrase == 1:
        return [n("B4", 1.5), r(0.5), n("C5", 1), r(1)]
    if phrase == 2:
        return [n("A4", 2), n("G4", 1), r(1)]
    if phrase == 3:
        return [r(0.5), n("E4", 2), n("F#4", 1), r(0.5)]
    if phrase == 4:
        return [n("G4", 1), n("A4", 1.5), r(0.5), n("B4", 1)]
    if phrase == 5:
        return [n("C5", 2), r(1), n("A4", 0.5), r(0.5)]
    if phrase == 6:
        return [n("G4", 1.5), r(0.5), n("E4", 2)]
    if phrase == 7:
        return [r(1), c(("G3", "B3"), 2), r(1)]
    return [r(4)]

def guitar_b(bar):
    # Light answering phrases while strings lead
    if bar % 4 == 0:
        return [r(1), c(("E3", "G3"), 1.5), r(0.5), n("A4", 1)]
    if bar % 4 == 1:
        return [n("G4", 2), r(2)]
    if bar % 4 == 2:
        return [r(2), c(("G3", "B3"), 1), r(1)]
    if bar % 4 == 3:
        return [n("E4", 1.5), r(0.5), n("G4", 1), r(1)]
    return [r(4)]

def guitar_c(bar):
    # Harmonic surprise section – answering phrases, harmonic colour
    pats = [
        [c(("E3", "G3"), 2), r(1), n("A4", 0.5), r(0.5)],
        [r(1), n("G4", 2), r(1)],
        [c(("Bb2", "Eb3"), 1.5), r(0.5), c(("G3", "Bb3"), 1), r(1)],
        [n("Eb4", 1), r(1), c(("Eb3", "G3"), 1.5), r(0.5)],
        [r(1), c(("C3", "E3"), 2), r(1)],
        [n("F4", 1.5), r(0.5), n("Eb4", 1), r(1)],
    ]
    return pats[bar % 6]

def guitar_d(bar):
    # Climax – harmonic support, sustained
    if bar < 16:
        return [c(("Eb3", "G3"), 2), r(1), n("Ab4", 0.5), r(0.5)]
    if bar < 20:
        return [c(("C3", "E3"), 2), r(2)]
    return [r(2), c(("F2", "A3"), 1.5), r(0.5)]

def guitar_e(bar):
    # Quiet return – melody drifting away
    if bar < 6:
        return [c(("E3", "G3"), 2), r(2)]
    if bar < 10:
        return [r(2), n("E4", 1.5), r(0.5)]
    return [c(("C3", "E3"), 2), r(2)]

def guitar_content(sec, bar, m):
    if sec == "A": return guitar_a(bar)
    if sec == "B": return guitar_b(bar)
    if sec == "C": return guitar_c(bar)
    if sec == "D": return guitar_d(bar)
    return guitar_e(bar)

# === VIOLIN I: Long melodic arcs, target tones, stepwise ===
def violin1_a(bar):
    return [r(4)]

def violin1_b(bar):
    # Strings inherit melody – 8-bar lyrical phrase
    phrase = bar % 8
    if phrase == 0:
        return [n("E5", 2), n("F#5", 1), n("G5", 1)]
    if phrase == 1:
        return [n("A5", 1.5), r(0.5), n("B5", 1), r(0.5)]
    if phrase == 2:
        return [n("G5", 2), n("E5", 1), r(1)]
    if phrase == 3:
        return [r(0.5), n("C5", 2), n("B5", 1), r(0.5)]
    if phrase == 4:
        return [n("A5", 1), n("G5", 1.5), r(0.5), n("E5", 1)]
    if phrase == 5:
        return [n("G5", 2), r(1), n("A5", 0.5), r(0.5)]
    if phrase == 6:
        return [n("E5", 1.5), r(0.5), n("C5", 2)]
    if phrase == 7:
        return [r(1), n("E5", 2), r(1)]
    return [r(4)]

def violin1_c(bar):
    # Harmonic surprise – sustained, transformed melody
    pats = [
        [n("E5", 2), n("F5", 1), r(1)],
        [n("G5", 1.5), r(0.5), n("Eb5", 1), r(1)],
        [n("Bb5", 1), r(1), n("Ab5", 1.5), r(0.5)],
        [n("Eb5", 2), r(1), n("G5", 0.5), r(0.5)],
        [n("C5", 1.5), r(0.5), n("Eb5", 1), r(1)],
        [n("F5", 2), r(2)],
    ]
    return pats[bar % 6]

def violin1_d(bar):
    # Climax – longest phrase, highest register
    if bar < 8:
        return [n("G5", 1), n("A5", 1), n("Bb5", 1), n("C6", 1)]
    if bar < 16:
        return [n("A5", 2), n("G5", 1), r(1)]
    if bar < 20:
        return [n("E5", 1.5), r(0.5), n("C5", 2)]
    return [n("G5", 2), r(2)]

def violin1_e(bar):
    # Quiet return – sustained, drifting
    if bar < 8:
        return [n("E5", 2), r(2)]
    if bar < 12:
        return [r(2), n("C5", 1.5), r(0.5)]
    return [r(4)]

def violin1_content(sec, bar, m):
    if sec == "A": return violin1_a(bar)
    if sec == "B": return violin1_b(bar)
    if sec == "C": return violin1_c(bar)
    if sec == "D": return violin1_d(bar)
    return violin1_e(bar)

# === VIOLIN II: Sustained harmonic colour, slow voice-leading ===
def violin2_a(bar):
    return [r(4)]

def violin2_b(bar):
    if bar % 2 == 0:
        return [n("G4", 2), n("A4", 1), r(1)]
    return [r(1), n("B4", 2), r(1)]

def violin2_c(bar):
    pats = [
        [n("E4", 2), n("F4", 1), r(1)],
        [r(1), n("Ab4", 2), r(1)],
        [n("Bb4", 1.5), r(0.5), n("Eb4", 1), r(1)],
        [n("G4", 2), r(2)],
        [n("C4", 1.5), r(0.5), n("Eb4", 2)],
        [n("F4", 2), r(2)],
    ]
    return pats[bar % 6]

def violin2_d(bar):
    if bar < 20:
        return [n("E4", 2), n("G4", 1), r(1)]
    return [r(4)]

def violin2_e(bar):
    if bar < 10:
        return [n("C4", 2), r(2)]
    return [r(4)]

def violin2_content(sec, bar, m):
    if sec == "A": return violin2_a(bar)
    if sec == "B": return violin2_b(bar)
    if sec == "C": return violin2_c(bar)
    if sec == "D": return violin2_d(bar)
    return violin2_e(bar)

# === VIOLA: Inner harmonic glue, occasional counter-melody ===
def viola_a(bar):
    return [r(4)]

def viola_b(bar):
    if bar % 2 == 0:
        return [n("C4", 2), n("E4", 1), r(1)]
    return [r(1), n("G4", 2), r(1)]

def viola_c(bar):
    pats = [
        [n("A3", 2), n("Bb3", 1), r(1)],
        [r(1), n("Eb4", 2), r(1)],
        [n("F4", 1.5), r(0.5), n("Bb3", 1), r(1)],
        [n("Eb4", 2), r(2)],
        [n("G3", 1.5), r(0.5), n("Bb3", 2)],
        [n("C4", 2), r(2)],
    ]
    return pats[bar % 6]

def viola_d(bar):
    if bar < 20:
        return [n("C4", 2), n("E4", 1), r(1)]
    return [r(4)]

def viola_e(bar):
    if bar < 10:
        return [n("G3", 2), r(2)]
    return [r(4)]

def viola_content(sec, bar, m):
    if sec == "A": return viola_a(bar)
    if sec == "B": return viola_b(bar)
    if sec == "C": return viola_c(bar)
    if sec == "D": return viola_d(bar)
    return viola_e(bar)

# === CELLO: Bass contour, sustained, duet with guitar in A ===
def cello_a(bar):
    # Cmaj7 → Am7 → Dm7 → G7 cycle
    cycle = bar % 4
    if cycle == 0:
        return [n("C2", 2), n("E2", 1), r(1)]
    if cycle == 1:
        return [n("A2", 2), n("C3", 1), r(1)]
    if cycle == 2:
        return [n("D2", 2), n("F2", 1), r(1)]
    return [n("G2", 2), n("B2", 1), r(1)]

def cello_b(bar):
    cycle = bar % 4
    if cycle == 0:
        return [n("F2", 2), n("A2", 1), r(1)]
    if cycle == 1:
        return [n("D2", 2), n("F#2", 1), r(1)]
    if cycle == 2:
        return [n("G2", 2), n("B2", 1), r(1)]
    return [n("C2", 2), n("E2", 1), r(1)]

def cello_c(bar):
    # Bacharach: Cmaj7 → Fm6 → Bb13 → Ebmaj9
    cycle = bar % 4
    if cycle == 0:
        return [n("C2", 2), n("E2", 1), r(1)]
    if cycle == 1:
        return [n("F2", 2), n("Ab2", 1), r(1)]
    if cycle == 2:
        return [n("Bb1", 2), n("D2", 1), r(1)]
    return [n("Eb2", 2), n("G2", 1), r(1)]

def cello_d(bar):
    # Climax bass
    cycle = bar % 4
    if cycle == 0:
        return [n("Eb2", 2), n("G2", 1), r(1)]
    if cycle == 1:
        return [n("Ab1", 2), n("C2", 1), r(1)]
    if cycle == 2:
        return [n("C2", 2), n("E2", 1), r(1)]
    return [n("F2", 2), n("Ab2", 1), r(1)]

def cello_e(bar):
    # Stepwise resolution
    if bar < 6:
        return [n("C2", 2), n("E2", 1), r(1)]
    if bar < 10:
        return [n("F2", 1.5), r(0.5), n("E2", 1), r(1)]
    return [n("C2", 2), r(2)]

def cello_content(sec, bar, m):
    if sec == "A": return cello_a(bar)
    if sec == "B": return cello_b(bar)
    if sec == "C": return cello_c(bar)
    if sec == "D": return cello_d(bar)
    return cello_e(bar)

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Northern Letters"
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

    section_starts = [1, 25, 49, 73, 97]
    section_labels = ["A", "B", "C", "D", "E"]
    section_barlines = [24, 48, 72, 96]

    for m in range(1, 111):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=88, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))

        if m == 25:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 49:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 73:
            mg.insert(0, dynamics.Dynamic("f"))
        elif m == 97:
            mg.insert(0, dynamics.Dynamic("p"))

        for e in guitar_content(sec, bar, m):
            mg.append(e)

        if m in section_barlines:
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for name, content_fn in [
            ("vn1", violin1_content),
            ("vn2", violin2_content),
            ("vla", viola_content),
            ("vc", cello_content),
        ]:
            content = content_fn(sec, bar, m)
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
    out_path = os.path.join(out_dir, "V1_Northern_Letters.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")
    engrave_clean_time_sigs(out_path)
    print("Engraving: time signatures only at meter changes.")

if __name__ == "__main__":
    main()
