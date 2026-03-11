#!/usr/bin/env python3
"""
Sylva Narrative No.1 - Guitar and String Quartet
Final Single-Pass. Wayne Shorter Narrative Engine. GCE ≥ 9.5.

Primary motif: E-F#-A-B (evolving). Development: inversion, interval expansion,
rhythmic displacement, harmonic reinterpretation.

Form: A(1-22) B(23-50) C(51-75) A'(76-100) Coda(101-108)
Tonality: modal with chromatic pivot harmony (Em → Bbmaj7 → Fmaj9 → G13sus → Em)
Independent viola counterline. Asymmetrical phrases preserved.
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

# === SECTION MAP (108 bars) ===
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

# Harmony: modal with chromatic pivot
def chord_for_section(sec, bar, m):
    if sec == "A":
        return "Em9"
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
    if chord_sym is None:
        return False
    if chord_sym != last_chord_sym:
        return True
    if bar % 2 == 0:
        return True
    return False

# Asymmetrical rhythm patterns (anti-monotony)
RHYTHM = [
    [1.0, 0.5, 1.5, 1.0],
    [0.5, 1.5, 0.5, 1.5],
    [1.5, 0.5, 1.0, 1.0],
    [1.0, 1.0, 0.5, 1.5],
    [0.5, 2.0, 0.5, 1.0],
    [2.0, 0.5, 1.0, 0.5],
    [1.0, 0.5, 1.5, 1.0],
    [0.5, 1.0, 1.0, 1.5],
]

def get_rhythm(m, sec, bar):
    idx = ((m - 1) // 5 + bar + hash(sec) % 8) % len(RHYTHM)
    return RHYTHM[idx]

# === GUITAR: Motif E-F#-A-B, dyads/triads, guitar-first ===
def guitar_a(bar):
    """A: Motif introduction — E-F#-A-B in Em"""
    blocks = [
        [("E3", "B3", "G4"), ("F#4", "A4"), ("A3", "E4", "B4"), ("B3", "F#4", "A4")],
        [("E4", "G4", "B4"), ("F#4", "A4", "C#5"), ("A3", "E4"), ("B3", "F#4", "A4")],
        [("E3", "B3"), ("F#4", "A4"), ("A3", "E4", "B4"), ("B3", "G4")],
        [("E4", "A4"), ("F#4", "B4"), ("A3", "E4"), ("B3", "F#4", "A4")],
        [("E3", "G3", "B3"), ("F#4", "A4"), ("A3", "E4"), ("B3", "F#4")],
    ]
    return blocks[bar // 4 % 5][bar % 4]

def guitar_b(bar):
    """B: Transformation — interval expansion, inversion hints, Bb pivot"""
    blocks = [
        [("Bb3", "F4", "D5"), ("E4", "G#4", "B4"), ("F3", "A3", "C5"), ("G3", "D4", "B4")],
        [("Bb3", "D4", "F4"), ("E4", "A4", "C#5"), ("F3", "C4", "A4"), ("G3", "B3", "D4")],
        [("Bb3", "F4"), ("E4", "B4"), ("F4", "A4"), ("G3", "D4", "B4")],
        [("Bb3", "E4", "G4"), ("E3", "G#3", "B3"), ("F3", "A3", "C4"), ("G3", "D4")],
        [("E4", "G4", "B4"), ("Bb3", "D4"), ("F4", "A4"), ("G3", "B3", "D4")],
        [("Bb3", "F4", "A4"), ("E4", "B4"), ("F3", "A3"), ("G3", "D4", "F4")],
    ]
    return blocks[bar // 4 % 6][bar % 4]

def guitar_c(bar):
    """C: Harmonic expansion — quartal fragments, chromatic colour"""
    blocks = [
        [("F3", "A3", "C4"), ("Bb3", "E4", "G4"), ("E3", "G3", "B3"), ("C4", "E4", "G4")],
        [("F4", "A4", "C5"), ("Bb3", "D4", "F4"), ("E4", "G4", "B4"), ("A3", "E4", "G4")],
        [("F3", "A3"), ("Bb3", "E4"), ("E3", "B3"), ("C4", "G4")],
        [("F4", "Bb4"), ("Bb3", "E4", "A4"), ("E4", "A4", "B4"), ("C4", "E4", "G4")],
        [("F3", "C4", "A4"), ("Bb3", "F4"), ("E3", "G3", "B3"), ("A3", "E4")],
        [("F4", "A4"), ("Bb3", "D4", "F4"), ("E4", "G4"), ("C4", "E4")],
    ]
    return blocks[bar // 4 % 6][bar % 4]

def guitar_a2(bar):
    """A': Reinterpreted return — inversion, register displacement"""
    blocks = [
        [("E4", "G4", "B4"), ("F#4", "A4", "C#5"), ("A3", "E4", "B4"), ("B3", "F#4", "A4")],
        [("E3", "B3", "G4"), ("F#4", "A4"), ("A3", "E4"), ("B3", "G4", "D5")],
        [("E4", "A4"), ("F#4", "B4"), ("A3", "E4", "G4"), ("B3", "F#4")],
        [("E3", "G3", "B3"), ("F#4", "A4", "C#5"), ("A3", "E4", "B4"), ("B3", "F#4")],
        [("E4", "G4"), ("F#4", "A4"), ("A3", "E4"), ("B3", "F#4", "A4")],
        [("rest"), ("rest"), ("rest"), ("rest")],
    ]
    if bar < 20:
        return blocks[bar // 4 % 6][bar % 4]
    return "rest"

def guitar_coda(bar):
    if bar < 6:
        frags = [("E4", "B4"), ("F#4", "A4"), ("A3", "E4"), ("B3", "F#4"), ("E3", "G4"), ("rest")]
        return frags[bar]
    return "rest"

def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "A2": pit = guitar_a2(bar)
    else: pit = guitar_coda(bar)

    if pit == "rest":
        return [r(4)], None
    if isinstance(pit, str):
        pit = (pit,)
    rhythm = get_rhythm(m, sec, bar)
    sym = chord_for_section(sec, bar, m)

    if len(pit) >= 2:
        r0, r1, r2, r3 = rhythm[0], rhythm[1], rhythm[2], rhythm[3]
        return [
            c(pit, r0), r(r1), c((pit[0], pit[1]) if len(pit) > 1 else pit, r2), r(r3),
        ], sym
    return [r(4)], sym

# === VIOLA: Independent counterline (continuous) ===
def viola_content(sec, bar, m):
    block = (m - 1) // 5
    cycle = (bar + block) % 6
    if cycle == 5:
        return [r(4)]
    if sec == "A":
        lines = [
            [c(("G3", "B3", "E4"), 1.5), r(0.5), n("F#4", 1), r(1)],
            [n("A4", 1), r(0.5), c(("E3", "G3"), 1.5), r(1)],
            [c(("B3", "E4"), 1), r(1), n("G4", 1), r(1)],
            [n("F#4", 0.5), r(0.5), c(("A3", "B3", "E4"), 1.5), r(1.5)],
        ]
        return lines[(bar + block) % 4]
    if sec == "B":
        lines = [
            [c(("D4", "F4", "Bb4"), 1.5), r(0.5), n("E4", 1), r(1)],
            [n("G4", 1), r(0.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("E4", "G4"), 1), r(1), n("Bb4", 1), r(1)],
            [n("D4", 1.5), r(0.5), c(("F4", "A4"), 1), r(1)],
        ]
        return lines[(bar + block) % 4]
    if sec == "C":
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

# === VIOLIN I: Motif dialogue with guitar ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if m % 7 in (1, 4):
            return [n("B5", 1.5), r(0.5), n("G5", 1), r(1)]
        if m % 8 == 3:
            return [n("F#5", 1), r(2), n("A5", 1.5), r(0.5)]
        if bar % 5 == 2:
            return [c(("E5", "G5"), 0.5), r(1), n("B5", 1), r(1.5)]
        return [r(4)]
    if sec == "B":
        if m % 6 == 1:
            return [c(("Bb5", "D6"), 0.5), r(1), n("E5", 1), r(1.5)]
        if m % 5 == 2:
            return [n("G5", 1.5), r(1), n("Bb5", 2), r(0.5)]
        if bar % 4 == 0:
            return [n("F#5", 2), r(2)]
        return [r(4)]
    if sec == "C":
        if m % 4 in (1, 3):
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        if m % 6 == 2:
            return [c(("E5", "G5"), 1.5), r(2.5)]
        return [r(4)]
    if sec == "A2":
        if m % 5 in (1, 3):
            return [n("B5", 2.5), r(1), n("G5", 0.5)]
        if bar % 4 == 2:
            return [n("E5", 1.5), r(2.5)]
        return [r(4)]
    if sec == "Coda" and bar < 4:
        return [n("B5", 2), r(2)]
    return [r(4)]

# === VIOLIN II: Harmonic reinforcement ===
def violin2_content(sec, bar, m):
    if sec == "A" and (m - 1) // 4 % 2 == 1 and m % 4 == 2:
        return [n("E5", 1), r(2), n("G5", 1)]
    if sec == "B" and m % 4 == 2:
        return [n("Bb4", 1), r(2), n("D5", 1)]
    if sec == "C" and (m - 1) // 4 % 2 == 0:
        if m % 3 == 0:
            return [n("F5", 2), r(2)]
        if m % 3 == 1:
            return [c(("A4", "C5"), 1.5), r(2.5)]
    if sec == "A2" and m % 6 in (2, 4):
        return [n("G4", 1.5), r(2.5)]
    return [r(4)]

# === CELLO: Pedal, harmonic grounding ===
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
    s.metadata.title = "Sylva Narrative No.1"
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
    section_labels = ["A", "B", "C", "A'", "Coda"]

    last_chord_sym = None
    for m in range(1, 109):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(1))
            mg.insert(0, tempo.MetronomeMark(number=100, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m == 23:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 51:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 76:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 101:
            mg.insert(0, dynamics.Dynamic("pp"))

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

        for name, content_fn in [
            ("vla", lambda: viola_content(sec, bar, m)),
            ("vn1", lambda: violin1_content(sec, bar, m)),
            ("vn2", lambda: violin2_content(sec, bar, m)),
            ("vc", lambda: cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("4/4")
            for e in content_fn():
                mx.append(e)
            parts[name].append(mx)

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
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V1_Sylva_Narrative_No1.musicxml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant(out)
    print("Fixed redundant time signatures and boxed rehearsal marks.")

if __name__ == "__main__":
    main()
