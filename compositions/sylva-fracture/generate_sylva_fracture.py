#!/usr/bin/env python3
"""
Sylva Fracture - Guitar and String Quartet
Primary: Wayne Shorter (motif, harmony, form)
Secondary: Zappa (1-3 gestures only - unexpected hits, rhythmic disruption)
Motif: F#-A-B-D. Form: A-B-C-D-E-A'-Coda.
~5 min, 72 bars @ 5/4, q=72.
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

# === SECTION MAP (72 bars) ===
# A: 1-10, B: 11-20, C: 21-30, D: 31-42, E: 43-52, A': 53-62, Coda: 63-72
def section(m):
    if m <= 10: return "A"
    if m <= 20: return "B"
    if m <= 30: return "C"
    if m <= 42: return "D"
    if m <= 52: return "E"
    if m <= 62: return "A2"
    return "Coda"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 11
    if sec == "C": return m - 21
    if sec == "D": return m - 31
    if sec == "E": return m - 43
    if sec == "A2": return m - 53
    return m - 63

# Chord symbols for F# Lydian
def chord_symbol_for(pitches):
    if not pitches or pitches == "rest":
        return None
    if isinstance(pitches, str):
        pitches = (pitches,)
    pit_str = "+".join(sorted(pitches))
    if "F#3" in pit_str or "F#4" in pit_str:
        if "A" in pit_str and "C#" in pit_str:
            return "F#maj7"
        if "A" in pit_str and "B" in pit_str:
            return "F#"
        return "F#"
    if "B3" in pit_str or "B4" in pit_str:
        if "D4" in pit_str and "F#4" in pit_str:
            return "B"
        return "B5"
    if "A3" in pit_str or "A4" in pit_str:
        if "C#4" in pit_str and "E4" in pit_str:
            return "A"
        return "A5"
    if "E4" in pit_str and "G#4" in pit_str:
        return "E"
    if "D4" in pit_str and "F#4" in pit_str:
        return "D"
    if "G#3" in pit_str or "G#4" in pit_str:
        return "G#m"
    return "F#"

# Rhythm patterns
RHYTHM = [
    [2.0, 0.5, 1.5, 1.0], [1.5, 1.0, 0.5, 2.0],
    [1.0, 1.5, 0.5, 2.0], [0.5, 2.0, 1.0, 1.5],
    [2.0, 1.0, 1.5, 0.5], [1.5, 0.5, 2.0, 1.0],
]

def get_rhythm(m, sec, bar):
    idx = ((m - 1) // 6 + bar + hash(sec) % 10) % len(RHYTHM)
    return RHYTHM[idx]

# Motif F#-A-B-D — Wayne Shorter development
def guitar_a(bar):
    """A: Motif emergence — F# Lydian"""
    blocks = [
        [("F#3","A3","C#4"), ("A4","E5"), ("B3","F#4","D5"), ("F#4","A4","B4")],
        [("F#4","A4","C#5"), ("B3","D4","F#4"), ("A3","C#4","E4"), ("F#3","A3","B3")],
    ]
    return blocks[bar // 4 % 2][bar % 4]

def guitar_b(bar):
    """B: Development — interval expansion"""
    blocks = [
        [("B3","F#4","D5"), ("A4","E5"), ("F#4","A4","C#5"), ("B3","D4","F#4")],
        [("F#3","A3","C#4"), ("G#3","B3","D4"), ("A3","E4","C#5"), ("B3","F#4","A4")],
    ]
    return blocks[bar // 4 % 2][bar % 4]

def guitar_c(bar):
    """C: Contrapuntal expansion — quartal fragments"""
    blocks = [
        [("F#3","B3","E4"), ("A4","D5"), ("B3","E4","A4"), ("F#4","A4","C#5")],
        [("A3","D4","G#4"), ("B3","F#4","B4"), ("F#4","A4"), ("B3","D4","F#4")],
    ]
    return blocks[bar // 4 % 2][bar % 4]

def guitar_d(bar):
    """D: Harmonic bloom — stacked triads, climax"""
    blocks = [
        [("F#3","A3","C#4","F#4"), ("B3","D4","F#4","B4"), ("A3","C#4","E4","A4"), ("F#3","B3","F#4","A4")],
        [("F#4","A4","C#5"), ("B3","F#4","D5"), ("A3","E4","C#5"), ("F#3","A3","B3","F#4")],
    ]
    return blocks[bar // 4 % 2][bar % 4]

def guitar_e(bar):
    """E: Fractured gesture — Zappa influence (angular, disruptive)"""
    # Zappa moments: bar 0, 4, 8 — unexpected angular voicings
    blocks = [
        [("F#3","B3","G#4"), ("A3","D4","F#4"), ("B3","E4","G#4"), ("F#4","A4","C#5")],
        [("G#3","C#4","E4"), ("B3","F#4","A4"), ("F#3","A3","C#4"), ("A3","E4","G#4")],
    ]
    return blocks[bar // 4 % 2][bar % 4]

def guitar_a2(bar):
    """A': Transformed return"""
    blocks = [
        [("F#4","A4","C#5"), ("B3","D4","F#4"), ("A3","E4","C#5"), ("F#3","A3","B3")],
        [("F#4","A4"), ("B3","F#4"), ("A3","E4"), ("F#3","A3","C#4")],
        [("rest"), ("rest"), ("rest"), ("rest")],
    ]
    if bar < 8:
        return blocks[bar // 4 % 3][bar % 4]
    return "rest"

def guitar_coda(bar):
    """Coda: Dissolve"""
    if bar < 6:
        frags = [("F#4","A4"), ("B3","F#4"), ("A3","E4"), ("F#3","A3"), ("B3","D4"), ("rest")]
        return frags[bar]
    return "rest"

def moving_dyads(bar, sec):
    if sec == "A": return [("F#3","A3", "B3","F#4"), ("A4","E5", "B3","D4")]
    if sec == "B": return [("B3","F#4", "A3","E4"), ("F#4","A4", "B3","D4")]
    if sec == "C": return [("F#3","B3", "A3","E4"), ("B3","F#4", "A4","D5")]
    if sec == "D": return [("F#3","A3", "F#4","A4"), ("B3","F#4", "B4","F#5")]
    if sec == "A2": return [("F#4","A4", "B3","F#4"), ("A3","E4", "F#3","A3")]
    return None

def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "D": pit = guitar_d(bar)
    elif sec == "E": pit = guitar_e(bar)
    elif sec == "A2": pit = guitar_a2(bar)
    else: pit = guitar_coda(bar)

    if pit == "rest":
        return [r(5)], None
    if isinstance(pit, str):
        pit = (pit,)
    rhythm = get_rhythm(m, sec, bar)
    sym = chord_symbol_for(pit)

    if bar % 4 == 2 and moving_dyads(bar, sec):
        pairs = moving_dyads(bar, sec)
        d1, d2, d3, d4 = pairs[bar % len(pairs)]
        return [
            c((d1, d2), rhythm[0]), r(rhythm[1]), c((d3, d4), rhythm[2]), r(rhythm[3])
        ], chord_symbol_for((d1, d2))
    if len(pit) >= 3:
        return [
            c(pit, rhythm[0]), r(rhythm[1]), c((pit[0], pit[1]), rhythm[2]), r(rhythm[3])
        ], sym
    if len(pit) == 2:
        return [c(pit, rhythm[0]), r(rhythm[1]), c(pit, rhythm[2]), r(rhythm[3])], sym
    return [n(pit[0], rhythm[0]), r(sum(rhythm[1:]))], sym

# Viola — interior counterline
def viola_content(sec, bar, m, block):
    if sec == "D":
        bloom = [
            [c(("A3","C#4","E4","F#4"), 2), r(0.5), c(("B3","D4"), 1.5), r(1)],
            [c(("F#3","A3","C#4"), 1.5), r(0.5), n("B3", 2), r(1)],
            [n("A4", 1), c(("C#4","E4","F#4"), 2), r(2)],
        ]
        return bloom[bar % 3]
    if sec == "A":
        lines = [
            [c(("A3","C#4","E4"), 1.5), r(0.5), n("F#4", 1.5), r(1.5)],
            [n("B3", 1), r(0.5), c(("F#3","A3"), 2), r(1.5)],
        ]
        return lines[bar % 2]
    if sec == "B":
        lines = [
            [c(("B3","D4","F#4"), 1.5), r(0.5), n("A4", 2), r(1)],
            [n("F#4", 1), c(("A3","C#4"), 1.5), r(1), n("B3", 1.5)],
        ]
        return lines[bar % 2]
    if sec == "C":
        lines = [
            [c(("F#3","A3","C#4"), 2), r(1), n("E4", 1.5), r(0.5)],
            [n("A4", 1), r(1), c(("B3","D4"), 2), r(1)],
        ]
        return lines[bar % 2]
    if sec == "E":
        # Zappa: slightly angular
        return [c(("G#3","B3","D4"), 2), r(1), n("F#4", 1.5), r(0.5)]
    if sec == "A2":
        return [c(("F#3","A3","C#4"), 2), r(1), n("B3", 1.5), r(0.5)]
    # Coda
    return [n("F#4", 2), r(3)] if bar < 4 else [r(5)]

# Violin I — motif, dialogue
def violin1_content(sec, bar, m):
    if sec == "D":
        return [c(("F#5","A5","C#6"), 1.5), r(1), n("E5", 1.5), r(1)]
    if sec == "A":
        if m % 5 in (1, 3):
            return [n("F#5", 2), r(1), n("A5", 1.5), r(0.5)]
        return [r(5)]
    if sec == "B":
        if m % 4 == 1:
            return [c(("A5","C#6"), 0.5), r(1), n("F#5", 1), r(2.5)]
        return [r(5)]
    if sec == "C":
        if m % 3 == 0:
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        return [r(5)]
    if sec == "E":
        # Zappa moment: unexpected accent at bar 0, 5
        if bar in (0, 5):
            return [c(("F#5","A5","B5"), 0.5), r(4.5)]
        return [n("F#5", 2), r(3)]
    if sec == "A2":
        return [n("F#5", 2.5), r(1), n("A5", 1), r(0.5)] if m % 4 == 1 else [r(5)]
    if sec == "Coda":
        return [n("F#5", 2), r(3)] if bar < 4 else [r(5)]
    return [r(5)]

# Violin II — harmonic reinforcement
def violin2_content(sec, bar, m, block):
    if sec == "A" and m % 4 == 2:
        return [n("A4", 1), r(2), n("C#5", 1), r(1)]
    if sec == "B" and m % 3 == 0:
        return [n("B4", 1), r(2), n("D5", 1), r(1)]
    if sec == "C" and block % 2 == 0:
        return [c(("F#4","A4"), 1.5), r(3.5)]
    if sec == "D":
        return [c(("A4","C#5","E5"), 2), r(3)]
    if sec == "E" and bar in (2, 7):
        return [n("B4", 1), r(4)]
    if sec == "A2" and m % 5 == 2:
        return [n("A4", 1.5), r(3.5)]
    return [r(5)]

# Cello — pedal, grounding
def cello_content(sec, bar, m):
    if sec == "D":
        return [n("F#2", 1), n("B2", 1), n("F#2", 1.5), r(1.5)]
    if sec == "A" and m % 6 >= 3:
        return [n("F#2", 2), r(3)]
    if sec == "B":
        return [n("B2", 1), r(4)]
    if sec == "C":
        return [n("F#2", 2), r(3)]
    if sec == "E":
        return [n("F#2", 2), r(3)]
    if sec == "A2":
        return [n("F#2", 2), r(3)]
    if sec == "Coda" and bar < 6:
        return [n("F#2", 3), r(2)]
    return [r(5)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Sylva Fracture"
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

    # Rehearsal letters: A, B, C, D, E, A', Coda
    section_starts = [1, 11, 21, 31, 43, 53, 63]
    section_labels = ["A", "B", "C", "D", "E", "A'", "Coda"]

    last_chord_sym = None
    for m in range(1, 73):
        sec = section(m)
        bar = bar_in(m, sec)
        block = (m - 1) // 6

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(6))
            mm = tempo.MetronomeMark(number=72, referent=note.Note(type='quarter'))
            mg.insert(0, mm)
            mg.insert(0, dynamics.Dynamic("pp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in (31, 43, 53, 63):
            mg.insert(0, dynamics.Dynamic("mf" if m == 31 else "mp" if m == 43 else "pp"))

        content, chord_sym = guitar_content(sec, bar, m)
        if chord_sym and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        for e in content:
            mg.append(e)

        if m in (10, 20, 30, 42, 52, 62):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for name, content_fn in [
            ("vla", lambda: viola_content(sec, bar, m, block)),
            ("vn1", lambda: violin1_content(sec, bar, m)),
            ("vn2", lambda: violin2_content(sec, bar, m, block)),
            ("vc", lambda: cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("5/4")
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
        r'\n\s+<attributes>\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+</attributes>',
        re.MULTILINE
    )
    div_plus_time = re.compile(
        r'(<attributes>\s*\n\s+<divisions>\d+</divisions>)\s*\n\s+<time>\s*\n\s+<beats>5</beats>\s*\n\s+<beat-type>4</beat-type>\s*\n\s+</time>\s*\n\s+(</attributes>)',
        re.MULTILINE
    )
    content = time_only.sub('', content)
    content = div_plus_time.sub(r'\1\n      \2', content)
    content = re.sub(r'<rehearsal enclosure="none"', r'<rehearsal enclosure="rectangle"', content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    score = build_score()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "Sylva_Fracture.musicxml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant(out)
    print("Fixed redundant time signatures.")

if __name__ == "__main__":
    main()
