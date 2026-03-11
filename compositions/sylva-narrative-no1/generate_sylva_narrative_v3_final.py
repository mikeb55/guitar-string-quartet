#!/usr/bin/env python3
"""
Sylva Narrative V3 – Final (GCE ≥ 9.8)
Orbit Album – Guitar + String Quartet

V2 → V3: Climax expansion, viola independence, transition smoothing,
one distinctive colour event. Refine without rewriting.
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

def phase(m):
    if m <= 22: return "I"
    if m <= 50: return "II"
    if m <= 75: return "III"
    return "IV"

def section(m):
    if m <= 22: return "A"
    if m <= 50: return "B"
    if m <= 75: return "C"
    if m <= 100: return "A2"
    return "Coda"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 23
    if sec == "C": return m - 51
    if sec == "A2": return m - 76
    return m - 101

def chord_for_section(sec, bar, m):
    if sec == "A": return "Em9"
    if sec == "B":
        opts = ["Bbmaj7#11", "Em9", "Fmaj9", "G13sus"]
        return opts[bar % 4]
    if sec == "C":
        opts = ["Fmaj9", "Bbmaj7#11", "Em9", "C7alt"]
        return opts[bar % 4]
    if sec == "A2":
        return "Em9" if bar % 3 != 2 else "G13sus"
    return "Em9"

def should_insert_chord(m, sec, bar, chord_sym, last_chord_sym):
    if chord_sym is None: return False
    if chord_sym != last_chord_sym: return True
    if bar % 2 == 0: return True
    return False

RHYTHM = [
    [1.0, 0.5, 1.5, 1.0], [0.5, 1.5, 0.5, 1.5], [1.5, 0.5, 1.0, 1.0],
    [1.0, 1.0, 0.5, 1.5], [0.5, 2.0, 0.5, 1.0], [2.0, 0.5, 1.0, 0.5],
]

def get_rhythm(m, sec, bar):
    idx = ((m - 1) // 5 + bar + hash(sec) % 6) % len(RHYTHM)
    return RHYTHM[idx]

# === GUITAR V3: Colour responder — dyads, harmonics, no comping ===
def guitar_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 2, 5, 8, 11, 14, 17):
            return [r(4)], None
        blocks = [("E3", "B3"), ("F#4", "A4"), ("A3", "E4"), ("B3", "F#4")]
        pit = blocks[bar % 4]
        rhythm = get_rhythm(m, sec, bar)
        return [c(pit, rhythm[0]), r(rhythm[1]), c((pit[0], pit[1]), rhythm[2]), r(rhythm[3])], chord_for_section(sec, bar, m)
    if sec == "B":
        if bar in (1, 4, 7, 11, 15, 19, 23):
            return [r(4)], None
        blocks = [("Bb3", "F4"), ("E4", "G#4"), ("F3", "A3"), ("G3", "D4")]
        pit = blocks[bar % 4]
        return [c(pit, 2), r(2)], chord_for_section(sec, bar, m)
    if sec == "C":
        if bar in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20):
            return [r(4)], None
        blocks = [("F3", "A3"), ("Bb3", "E4"), ("E3", "G3"), ("C4", "E4")]
        pit = blocks[bar % 4]
        return [c(pit, 2), r(2)], chord_for_section(sec, bar, m)
    if sec == "A2":
        if bar in (0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19):
            return [r(4)], None
        blocks = [("E4", "G4"), ("F#4", "A4"), ("A3", "E4"), ("B3", "F#4")]
        pit = blocks[bar % 4]
        return [c(pit, 2.5), r(1.5)], chord_for_section(sec, bar, m)
    if sec == "Coda":
        if bar >= 5:
            return [r(4)], None
        return [c(("E4", "B4") if bar % 2 == 0 else ("F#4", "A4"), 2), r(2)], "Em9"
    return [r(4)], None

# === VIOLIN I V3: Climax — sustain high register (bars 60-72), extended f ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if bar in (0, 1, 3, 6, 9, 12, 15):
            return [n("B5", 1.5), r(0.5), n("G5", 1), r(1)]
        if bar in (2, 5, 8, 11):
            return [n("F#5", 1), r(2), n("A5", 1.5), r(0.5)]
        if bar in (4, 7, 10, 13):
            return [c(("E5", "G5"), 0.5), r(1), n("B5", 1), r(1.5)]
        return [r(4)]
    if sec == "B":
        if bar in (0, 3, 6, 10, 14, 18):
            return [c(("Bb5", "D6"), 0.5), r(1), n("E5", 1), r(1.5)]
        if bar in (2, 7, 12, 17):
            return [n("G5", 1.5), r(1), n("Bb5", 2), r(0.5)]
        if bar in (4, 9, 15, 21):
            return [n("F#5", 2), r(2)]
        return [r(4)]
    if sec == "C":
        if bar in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18):
            return [n("C6", 2), r(1), n("B5", 1)]
        if bar in (0, 2, 4, 7, 10):
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        if bar in (3, 8, 14):
            return [c(("E5", "G5"), 1.5), r(2.5)]
        if bar in (1, 5, 6):
            return [n("B5", 2), r(2)]
        return [r(4)]
    if sec == "A2":
        if bar in (0, 2, 5, 8, 11, 14):
            return [n("B5", 2.5), r(1), n("G5", 0.5)]
        if bar in (4, 9, 13):
            return [n("E5", 1.5), r(2.5)]
        return [r(4)]
    if sec == "Coda" and bar < 5:
        return [n("B5", 2), r(2)]
    return [r(4)]

# === VIOLIN II V3: Climax — increased rhythmic energy (bars 60-72) ===
def violin2_content(sec, bar, m):
    if sec == "A":
        if bar in (2, 6, 10, 14):
            return [r(1), n("E5", 1), r(1), n("G5", 1)]
        if bar in (4, 8, 12):
            return [n("F#5", 1), r(2), n("A5", 1)]
        return [r(4)]
    if sec == "B":
        if bar in (1, 5, 9, 13, 17):
            return [r(0.5), n("Bb4", 1), n("D5", 1), r(1.5)]
        if bar in (3, 8, 14):
            return [n("G4", 1), r(2), n("B4", 1)]
        return [r(4)]
    if sec == "C":
        if bar in (9, 10, 11, 12, 13, 14, 15, 16):
            return [n("F5", 0.75), n("G5", 0.75), n("A5", 1), r(1.5)]
        if bar in (1, 5, 9, 13):
            return [n("F5", 2), r(2)]
        if bar in (3, 7, 11):
            return [c(("A4", "C5"), 1.5), r(2.5)]
        return [r(4)]
    if sec == "A2":
        if bar in (2, 6, 10, 14):
            return [n("G4", 1.5), r(2.5)]
        return [r(4)]
    return [r(4)]

# === VIOLA V3: Independence — contrary motion, displacement, tension resolving down ===
def viola_content(sec, bar, m):
    block = (m - 1) // 5
    if m == 22:
        return [n("E4", 4)]
    if m == 50:
        return [n("F4", 4)]
    if m == 75:
        return [n("E4", 4)]
    if sec == "A":
        lines = [
            [c(("G3", "B3", "E4"), 1.5), r(0.5), n("F#4", 1), r(1)],
            [n("A4", 1), r(0.5), c(("E3", "G3"), 1.5), r(1)],
            [c(("B3", "E4"), 1), r(1), n("G4", 1), r(1)],
            [n("F#4", 0.5), r(0.5), c(("A3", "B3", "E4"), 1.5), r(1.5)],
            [r(0.5), n("C4", 1), n("B3", 1), r(1), n("G4", 0.5)],
        ]
        return lines[(bar + block) % 5]
    if sec == "B":
        lines = [
            [c(("D4", "F4", "Bb4"), 1.5), r(0.5), n("E4", 1), r(1)],
            [n("G4", 1), r(0.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("E4", "G4"), 1), r(1), n("Bb4", 1), r(1)],
            [n("D4", 1.5), r(0.5), c(("F4", "A4"), 1), r(1)],
            [r(1), n("Eb4", 0.75), n("D4", 0.75), r(1), n("Bb3", 0.5)],
        ]
        return lines[(bar + block) % 5]
    if sec == "C":
        if bar in (9, 10, 11, 12, 13, 14):
            return [n("C4", 0.5), n("Bb3", 0.5), n("A3", 1), r(2)]
        lines = [
            [c(("A3", "C4", "F4"), 1.5), r(0.5), n("Bb3", 1), r(1)],
            [n("E4", 1), r(0.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("F3", "A3"), 1), r(1), n("C4", 1), r(1)],
            [n("Bb3", 1), c(("D4", "F4"), 1.5), r(1.5)],
        ]
        return lines[(bar + block) % 4]
    if sec == "A2":
        lines = [
            [c(("E3", "G3", "B3"), 1.5), r(0.5), n("F#4", 1), r(1)],
            [n("A4", 1), r(0.5), c(("B3", "E4"), 1.5), r(1)],
            [c(("G3", "B3", "E4"), 2), r(2)],
        ]
        return lines[(bar + block) % 3] if bar < 20 else [n("E4", 2), r(2)]
    if sec == "Coda":
        return [n("E4", 2), r(2)] if bar < 6 else [r(4)]
    return [r(4)]

# === CELLO: Unchanged — gravitational bass ===
def cello_content(sec, bar, m):
    block = (m - 1) // 5
    if sec == "A":
        patterns = [
            [n("E2", 1), n("B2", 1), n("E2", 1), r(1)],
            [n("E2", 1), n("F#2", 1), n("G2", 1), n("B2", 1)],
            [n("B2", 1), n("E2", 1), n("B2", 1), r(1)],
            [n("E2", 1.5), n("B2", 0.5), n("E2", 1), r(1)],
            [n("E2", 0.5), n("B2", 1), n("E2", 1), r(1.5)],
        ]
        return patterns[(bar + block) % 5]
    if sec == "B":
        patterns = [
            [n("Bb2", 1), n("F2", 1), n("Bb2", 1), r(1)],
            [n("Bb2", 1), n("C3", 1), n("D3", 1), n("F2", 1)],
            [n("F2", 1), n("Bb2", 1), n("F2", 1), r(1)],
            [n("Bb2", 1.5), n("F2", 0.5), n("Bb2", 1), r(1)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "C":
        patterns = [
            [n("F2", 1), n("C3", 1), n("F2", 1), r(1)],
            [n("F2", 1), n("G2", 1), n("A2", 1), n("C3", 1)],
            [n("C3", 1), n("F2", 1), n("C3", 1), r(1)],
        ]
        return patterns[(bar + block) % 3]
    if sec == "A2":
        patterns = [
            [n("E2", 2), r(2)],
            [n("E2", 1), n("B2", 1), r(2)],
            [n("B2", 1), n("E2", 1), r(2)],
        ]
        return patterns[(bar + block) % 3]
    if sec == "Coda" and bar < 6:
        return [n("E2", 2), r(2)]
    return [r(4)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Sylva Narrative"
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

    section_starts = [1, 23, 51, 76, 101]
    section_labels = ["I", "II", "III", "IV", "Coda"]
    dyn_map = {
        1: "pp", 12: "mp", 20: "mp", 23: "mp", 45: "mf", 51: "mf",
        58: "f", 60: "f", 65: "f", 70: "f", 73: "f", 76: "mf",
        90: "p", 101: "pp"
    }
    colour_moment = 63

    last_chord_sym = None
    for m in range(1, 109):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(1))
            mm = tempo.MetronomeMark(number=100, referent=note.Note(type='quarter'))
            mm.text = "Moderately, narrative flow"
            mg.insert(0, mm)

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in dyn_map:
            mg.insert(0, dynamics.Dynamic(dyn_map[m]))

        content, chord_sym = guitar_content(sec, bar, m)
        if should_insert_chord(m, sec, bar, chord_sym, last_chord_sym):
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        for e in content:
            mg.append(e)

        if m in (22, 50, 75, 100):
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
                mx.insert(0, key.KeySignature(1))
            if pname == "vn1" and m == colour_moment:
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
    ws_root = os.path.abspath(os.path.join(base, "..", "..", ".."))
    out_ecm = os.path.join(ws_root, "ECM-Orbit-Album-2027", "Compositions", "Sylva_Narrative", "V3_Sylva_Narrative_Final.musicxml")
    os.makedirs(os.path.dirname(out_ecm), exist_ok=True)

    out_local = os.path.join(base, "musicxml", "V3_Sylva_Narrative_Final.musicxml")
    os.makedirs(os.path.dirname(out_local), exist_ok=True)

    for out in [out_ecm, out_local]:
        score.write('musicxml', fp=out)
        fix_redundant(out)
        print(f"Exported: {out}")

if __name__ == "__main__":
    main()
