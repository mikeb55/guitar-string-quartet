#!/usr/bin/env python3
"""
Drift Study No.2 - Guitar and String Quartet
Engine: Scofield–Holland Hybrid
~5 min, 125 bars @ 4/4, q=105.

Scofield: syncopated rhythms, dyads/triads, angular melodic fragments
Holland: harmonic grounding, cello-driven bass, contrapuntal ensemble

Form: A (1-20) B (21-40) C (41-60) D (61-80) A' (81-100)
Harmony: Dm9, G13sus, Bbmaj7#11, Fmaj9
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

# === SECTION MAP (125 bars, ~5 min) ===
# A: 1-25, B: 26-50, C: 51-75, D: 76-100, A': 101-125
def section(m):
    if m <= 25: return "A"
    if m <= 50: return "B"
    if m <= 75: return "C"
    if m <= 100: return "D"
    return "A2"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 26
    if sec == "C": return m - 51
    if sec == "D": return m - 76
    return m - 101

# Chord symbols per section
def chord_for_section(sec, bar):
    if sec == "A":
        return "Dm9"
    if sec == "B":
        return "G13sus" if bar % 4 < 2 else "Dm9"
    if sec == "C":
        return "Bbmaj7#11" if bar % 4 < 2 else "Fmaj9"
    if sec == "D":
        opts = ["Fmaj9", "Bbmaj7#11", "Fmaj9", "Dm9"]
        return opts[bar % 4]
    if sec == "A2":
        return "Dm9"
    return "Dm9"

# Syncopated rhythm patterns (Scofield) — 4/4, each sums to 4
RHYTHM = [
    [1.0, 0.5, 1.0, 1.5],  # chord, rest, chord, rest
    [0.5, 1.5, 0.5, 1.5],
    [1.5, 0.5, 1.0, 1.0],
    [0.5, 1.0, 0.5, 2.0],
    [1.0, 0.5, 1.5, 1.0],
    [0.5, 1.0, 1.0, 1.5],
]

def get_rhythm(m, sec, bar):
    idx = ((m - 1) // 6 + bar + hash(sec) % 10) % len(RHYTHM)
    return RHYTHM[idx]

# Dm9: D-F-A-C-E
# G13sus: G-C-D-F-A-E
# Bbmaj7#11: Bb-D-F-A-E
# Fmaj9: F-A-C-E-G

def guitar_a(bar):
    """A: Groove motif — Dm9 dyads and triads"""
    blocks = [
        [("D3", "F3"), ("A3", "C4"), ("D4", "F4"), ("A3", "E4")],
        [("D3", "F3", "A3"), ("C4", "E4"), ("D4", "F4"), ("A3", "C4")],
        [("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "F3")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_b(bar):
    """B: Harmonic expansion — G13sus / Dm9"""
    blocks = [
        [("G3", "C4"), ("D4", "F4"), ("A3", "E4"), ("D3", "F3")],
        [("G3", "D4", "F4"), ("C4", "E4"), ("D4", "A4"), ("G3", "C4")],
        [("D3", "F3"), ("A3", "C4"), ("G3", "D4"), ("C4", "F4")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_c(bar):
    """C: Contrapuntal — Bbmaj7#11 / Fmaj9"""
    blocks = [
        [("Bb3", "D4"), ("F4", "A4"), ("Bb3", "E4"), ("F3", "A3")],
        [("F3", "A3", "C4"), ("E4", "G4"), ("Bb3", "D4"), ("F4", "A4")],
        [("Bb3", "F4"), ("D4", "A4"), ("F3", "C4"), ("Bb3", "E4")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_d(bar):
    """D: Harmonic bloom — fuller voicings"""
    blocks = [
        [("F3", "A3", "C4"), ("E4", "G4"), ("Bb3", "D4", "F4"), ("F4", "A4", "C5")],
        [("Bb3", "D4", "E4"), ("F3", "A3", "C4"), ("D3", "F3", "A3"), ("Bb3", "F4")],
        [("F3", "A3"), ("C4", "E4"), ("Bb3", "D4"), ("F4", "A4")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_a2(bar):
    """A': Transformed return — Dm9"""
    blocks = [
        [("D4", "F4"), ("A3", "C4"), ("D3", "F3"), ("A3", "E4")],
        [("D3", "F3", "A3"), ("C4", "E4"), ("D4", "F4"), ("rest")],
        [("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "F3")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "D": pit = guitar_d(bar)
    else: pit = guitar_a2(bar)

    if pit == "rest":
        return [r(4)], None
    if isinstance(pit, str):
        pit = (pit,)
    rhythm = get_rhythm(m, sec, bar)
    sym = chord_for_section(sec, bar)

    # Ensure guitar is never monophonic — dyads or triads
    if len(pit) >= 2:
        r0, r1, r2, r3 = rhythm[0], rhythm[1], rhythm[2], rhythm[3]
        return [
            c(pit, r0), r(r1), c((pit[0], pit[1]) if len(pit) > 1 else pit, r2), r(r3),
        ], sym
    return [r(4)], sym

# Viola — interior counterpoint
def viola_content(sec, bar, m):
    if sec == "A":
        lines = [
            [c(("A3", "C4", "E4"), 1.5), r(0.5), n("F4", 1), r(1)],
            [n("D4", 1), r(0.5), c(("F3", "A3"), 1.5), r(1)],
            [c(("A3", "C4"), 1), r(1), n("D4", 1), r(1)],
        ]
        return lines[bar % 3]
    if sec == "B":
        lines = [
            [c(("C4", "E4", "G4"), 1.5), r(0.5), n("A4", 1), r(1)],
            [n("G4", 1), r(0.5), c(("D4", "F4"), 1.5), r(1)],
            [c(("A3", "C4"), 1), r(1), n("G4", 1), r(1)],
        ]
        return lines[bar % 3]
    if sec == "C":
        lines = [
            [c(("F3", "A3", "C4"), 1.5), r(0.5), n("Bb3", 1), r(1)],
            [n("D4", 1), r(0.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("F3", "A3"), 1), r(1), n("C4", 1), r(1)],
        ]
        return lines[bar % 3]
    if sec == "D":
        bloom = [
            [c(("A3", "C4", "E4", "F4"), 1.5), r(0.5), c(("Bb3", "D4"), 1), r(1)],
            [c(("F3", "A3", "C4"), 1), r(0.5), n("E4", 1), r(1.5)],
            [n("Bb3", 1), c(("D4", "F4", "A4"), 1.5), r(1.5)],
        ]
        return bloom[bar % 3]
    if sec == "A2":
        return [c(("D3", "F3", "A3"), 1.5), r(0.5), n("C4", 1), r(1)]
    return [r(4)]

# Violin I — melodic counterlines
def violin1_content(sec, bar, m):
    if sec == "A":
        if m % 5 in (1, 3):
            return [n("A5", 1.5), r(0.5), n("F5", 1), r(1)]
        return [r(4)]
    if sec == "B":
        if m % 4 == 1:
            return [c(("G5", "A5"), 0.5), r(1), n("D5", 1), r(1.5)]
        return [r(4)]
    if sec == "C":
        if m % 3 == 0:
            return [n("Bb5", 1.5), r(0.5), n("F5", 1), r(1)]
        return [r(4)]
    if sec == "D":
        return [c(("F5", "A5", "C6"), 1), r(1), n("E5", 1), r(1)]
    if sec == "A2":
        return [n("A5", 2), r(1), n("F5", 0.5), r(0.5)] if m % 4 == 1 else [r(4)]
    return [r(4)]

# Violin II — harmonic reinforcement
def violin2_content(sec, bar, m):
    if sec == "A" and m % 4 == 2:
        return [n("C5", 1), r(2), n("E5", 0.5), r(0.5)]
    if sec == "B" and m % 3 == 0:
        return [n("D5", 1), r(2), n("F5", 0.5), r(0.5)]
    if sec == "C" and bar % 2 == 0:
        return [c(("F4", "A4"), 1), r(3)]
    if sec == "D":
        return [c(("A4", "C5", "E5"), 1.5), r(2.5)]
    if sec == "A2" and m % 5 == 2:
        return [n("C5", 1), r(3)]
    return [r(4)]



# Cello — bass-like harmonic anchor (Holland: drives motion)
def cello_content(sec, bar, m):
    if sec == "A":
        return [n("D2", 1), n("A2", 1), n("D2", 1), r(1)]
    if sec == "B":
        return [n("G2", 1), n("D3", 1), n("G2", 1), r(1)]
    if sec == "C":
        return [n("Bb2", 1), n("F2", 1), n("Bb2", 1), r(1)]
    if sec == "D":
        return [n("F2", 1), n("C3", 1), n("Bb2", 1), r(1)]
    if sec == "A2":
        return [n("D2", 2), r(2)]
    return [r(4)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Drift Study No.2"
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

    section_starts = [1, 26, 51, 76, 101]
    section_labels = ["A", "B", "C", "D", "A'"]

    last_chord_sym = None
    for m in range(1, 126):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))  # 1 flat
            mm = tempo.MetronomeMark(number=105, referent=note.Note(type='quarter'))
            mg.insert(0, mm)
            mg.insert(0, dynamics.Dynamic("mp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in (26, 51, 76, 101):
            dyn = "mf" if m == 76 else "mp" if m in (26, 51) else "pp" if m == 101 else "mp"
            mg.insert(0, dynamics.Dynamic(dyn))

        content, chord_sym = guitar_content(sec, bar, m)
        if chord_sym and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        for e in content:
            mg.append(e)

        if m in (25, 50, 75, 100):
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
    out = os.path.join(os.path.dirname(__file__), "musicxml", "Drift_Study_No2_Scofield_Holland.musicxml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant(out)
    print("Fixed redundant time signatures and boxed rehearsal marks.")

if __name__ == "__main__":
    main()
