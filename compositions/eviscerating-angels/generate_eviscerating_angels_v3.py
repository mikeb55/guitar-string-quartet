#!/usr/bin/env python3
"""
Eviscerating Angels V3 - Guitar and String Quartet
GCE 9.5+ target. Score readability standard applied.
Structure: A (motif emergence) → B (rhythmic destabilization) → C (contrapuntal expansion)
→ D (harmonic bloom climax) → E (fractured release) → F (coda)
Chord symbols, boxed rehearsal letters, double barlines, dynamics.
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
# A: 1-12, B: 13-24, C: 25-36, D: 37-48, E: 49-60, F: 61-72
def section(m):
    if m <= 12: return "A"
    if m <= 24: return "B"
    if m <= 36: return "C"
    if m <= 48: return "D"
    if m <= 60: return "E"
    return "F"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 13
    if sec == "C": return m - 25
    if sec == "D": return m - 37
    if sec == "E": return m - 49
    return m - 61

# Chord symbol mapping — must match actual pitches
def chord_symbol_for(pitches):
    if not pitches or pitches == "rest":
        return None
    if isinstance(pitches, str):
        pitches = (pitches,)
    pit_str = "+".join(sorted(pitches))
    # A minor family
    if "A3" in pit_str and "E4" in pit_str and "G4" in pit_str:
        return "Am" if "C5" not in pit_str else "Am7"
    if "A3" in pit_str and "E4" in pit_str and "C5" in pit_str:
        return "Am7"
    if "A3" in pit_str and "E4" in pit_str:
        return "Am"
    if "A3" in pit_str and "C#4" in pit_str and "E4" in pit_str:
        return "A"
    # E family
    if "E4" in pit_str and "G#4" in pit_str and "B4" in pit_str:
        return "E"
    if "E4" in pit_str and "B4" in pit_str:
        return "E5"
    if "E3" in pit_str and "B3" in pit_str and "G4" in pit_str:
        return "Em"
    # G family
    if "G3" in pit_str and "D4" in pit_str and "B4" in pit_str:
        return "G/B"
    if "G3" in pit_str and "D4" in pit_str:
        return "G"
    if "G4" in pit_str and "D5" in pit_str:
        return "G5"
    # D family
    if "D4" in pit_str and "F#4" in pit_str and "A4" in pit_str:
        return "D"
    if "D4" in pit_str and "F#4" in pit_str:
        return "D5"
    # C family
    if "C4" in pit_str and "E4" in pit_str and "G4" in pit_str:
        return "Cm"
    # B family
    if "B3" in pit_str and "D4" in pit_str and "F#4" in pit_str:
        return "Bm"
    # F# family
    if "F#4" in pit_str and "C#5" in pit_str:
        return "F#5"
    # C# family
    if "C#4" in pit_str and "G#4" in pit_str and "E5" in pit_str:
        return "C#m"
    if "D4" in pit_str and "A4" in pit_str:
        return "D5"
    if "B4" in pit_str and "F#5" in pit_str:
        return "B5"
    if "E4" in pit_str and "A4" in pit_str and "C#5" in pit_str:
        return "A"
    if "G4" in pit_str and "D5" in pit_str and "B5" in pit_str:
        return "G"
    if "A3" in pit_str and "E4" in pit_str and "B4" in pit_str:
        return "Am"
    return "Am"  # default

# Rhythm patterns — less square, more varied
RHYTHM_PATTERNS = [
    [1.5, 1.0, 0.5, 2.0],
    [1.0, 1.5, 0.5, 2.0],
    [2.0, 0.5, 1.5, 1.0],
    [0.5, 2.0, 1.0, 1.5],
    [1.0, 1.0, 1.0, 2.0],
    [2.5, 0.25, 0.25, 2.0],
    [1.5, 0.5, 2.0, 1.0],
    [2.0, 1.0, 0.5, 1.5],
]

def get_rhythm(m, sec):
    block = (m - 1) // 6
    idx = (block + hash(sec) % 100) % len(RHYTHM_PATTERNS)
    return RHYTHM_PATTERNS[idx]

# Guitar content by section
def guitar_a(bar):
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C5")],
        [("E4","G#4","B4"), ("D4","F#4","A4"), ("C4","E4","G4"), ("B3","D4","F#4")],
        [("A3","E4"), ("G4","D5"), ("E4","B4","G5"), ("A3","C#4","E4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_b(bar):
    blocks = [
        [("E3","B3","G4"), ("A3","E4","C5"), ("D4","F#4","A4"), ("E4","G#4","B4")],
        [("C4","E4","G4"), ("B3","D4","F#4"), ("A3","E4","G4"), ("G4","D5","B5")],
        [("E4","B4"), ("F#4","C#5"), ("G4","D5"), ("A3","E4","B4")],
        [("C#4","G#4"), ("D4","A4"), ("E4","B4","G5"), ("A3","E4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def guitar_c(bar):
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G4","D5"), ("A3","E4","C5")],
        [("E4","B4","G5"), ("A3","E4"), ("D4","F#4","A4"), ("G3","B3","D4")],
        [("A4","E5"), ("G4","D5"), ("E4","B4"), ("A3","E4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_d(bar):
    """D: Climax — stacked triads, quartal"""
    blocks = [
        [("A3","E4","G4","B4"), ("E3","B3","G4","B4"), ("D4","F#4","A4","D5"), ("E4","G#4","B4","E5")],
        [("G3","D4","B4","D5"), ("A3","E4","C#5","E5"), ("B3","F#4","D5"), ("C4","E4","G4","B4")],
        [("A3","E4","G4"), ("E4","B4","G5"), ("D4","G4","A4"), ("E4","A4","B4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_e(bar):
    """E: Fractured release"""
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("rest"), ("rest")],
        [("G3","D4"), ("A3","E4"), ("E4","B4"), ("A3","E4")],
    ]
    if bar < 8:
        return blocks[bar // 4 % 2][bar % 4]
    return "rest"

def guitar_f(bar):
    """F: Transformed return / coda"""
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C5")],
        [("D4","F#4","A4"), ("E4","G4","B4"), ("A3","E4"), ("G3","D4")],
        [("rest"), ("rest"), ("rest"), ("rest")],
    ]
    if bar < 10:
        return blocks[bar // 4 % 3][bar % 4]
    return "rest"

def moving_dyads(bar, sec):
    if sec == "A":
        return [("A3","E4", "G3","D4"), ("E4","B4", "D4","A4"), ("A3","E4", "G3","D4")]
    if sec == "B":
        return [("E3","B3", "G3","D4"), ("A3","E4", "C4","G4"), ("D4","F#4", "E4","B4")]
    if sec == "C":
        return [("A3","E4", "G4","D5"), ("E4","B4", "A3","E4")]
    if sec == "D":
        return [("A3","E4", "A4","E5"), ("G3","D4", "G4","D5")]
    return None

def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "D": pit = guitar_d(bar)
    elif sec == "E": pit = guitar_e(bar)
    else: pit = guitar_f(bar)

    if pit == "rest":
        return [r(5)], None
    if isinstance(pit, str):
        pit = (pit,)
    rhythm = get_rhythm(m, sec)
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

# Viola — continuous interior counterline
def viola_content(sec, bar, m, block):
    if sec == "D":
        bloom = [
            [c(("B3","D4","F#4","A4"), 2), r(0.5), c(("E4","G#4"), 1.5), r(1)],
            [c(("D4","F#4","A4"), 1.5), r(0.5), n("G4", 2), r(1)],
            [n("A4", 1), c(("C#4","E4","G4"), 2), r(2)],
            [c(("G3","B3","D4"), 2.5), r(1), n("E4", 1), r(0.5)],
        ]
        return bloom[bar % 4]
    if sec == "A":
        lines = [
            [c(("B3","D4","F#4"), 1.5), r(0.5), n("E4", 1.5), r(1.5)],
            [n("G4", 1), r(0.5), c(("A3","E4"), 2), r(1.5)],
            [c(("D4","F#4"), 2), r(1), n("C4", 1.5), r(0.5)],
            [n("E4", 0.5), r(0.5), c(("G3","B3","D4"), 2.5), r(1.5)],
        ]
        return lines[bar % 4]
    if sec == "B":
        lines = [
            [c(("E4","G#4","B4"), 1.5), r(0.5), n("D4", 2), r(1)],
            [n("A4", 1), c(("C#4","E4"), 1.5), r(1), n("B3", 1.5)],
            [c(("D4","F#4","A4"), 2), r(0.5), n("G4", 1.5), r(1)],
            [n("E4", 1), r(0.5), c(("G3","B3"), 2), r(1.5)],
        ]
        return lines[bar % 4]
    if sec == "C":
        lines = [
            [c(("A3","E4","G4"), 2), r(1), n("E4", 1.5), r(0.5)],
            [n("G4", 1), r(1), c(("A3","C#4"), 2), r(1)],
            [r(1), c(("E4","B4"), 2.5), r(1.5)],
            [c(("D4","F#4"), 1.5), r(0.5), n("B3", 2), r(1)],
        ]
        return lines[bar % 4]
    if sec == "E":
        sparse = [
            [n("A3", 3), r(2)], [r(1), n("E4", 2.5), r(1.5)],
            [c(("G3","B3"), 2), r(3)], [n("E4", 1.5), r(3.5)],
        ]
        return sparse[bar % 4]
    # F
    lines = [
        [c(("D4","F#4","A4"), 2), r(1), n("E4", 1.5), r(0.5)],
        [n("G4", 1), r(1), c(("A3","E4"), 2), r(1)],
        [c(("B3","D4","F#4"), 2.5), r(2.5)],
    ]
    return lines[bar % 3] if bar < 10 else [n("A3", 3), r(2)]

# Violin I — motif, dialogue with guitar
def violin1_content(sec, bar, m):
    if sec == "D":
        return [c(("E5","G5","B5"), 1.5), r(1), n("A5", 1.5), r(1)]
    if sec == "A":
        if m % 7 in (1, 4):
            return [n("E5", 2), r(1), n("G5", 1.5), r(0.5)]
        if m % 8 == 3:
            return [n("A5", 1), r(2), n("E5", 1.5), r(0.5)]
        return [r(5)]
    if sec == "B":
        if m % 6 == 1:
            return [c(("E5","G5"), 0.5), r(1), n("B5", 1), r(2.5)]
        if m % 5 == 2:
            return [n("G5", 1.5), r(1), n("E5", 2), r(0.5)]
        if m % 4 == 0:
            return [n("A5", 2), r(3)]
        return [r(5)]
    if sec == "C":
        if m % 4 in (1, 3):
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        if m % 6 == 2:
            return [c(("E5","G5"), 1.5), r(3.5)]
        return [r(5)]
    if sec == "E":
        return [n("G5", 2.5), r(1), n("E5", 1), r(0.5)] if m % 3 == 1 else [r(5)]
    if sec == "F":
        return [n("D5", 2.5), r(1), n("F#5", 1), r(0.5)] if m % 4 == 1 else [r(5)]
    return [r(5)]

# Violin II — materially more active
def violin2_content(sec, bar, m, block):
    if sec == "A":
        if block >= 1 and m % 4 == 2:
            return [n("D5", 1), r(2), n("F#5", 1), r(1)]
        if m % 6 == 4:
            return [c(("B4","D5"), 1.5), r(3.5)]
        return [r(5)]
    if sec == "B":
        if m % 3 in (1, 2):
            return [n("B4", 1), r(1), n("D5", 1.5), r(1.5)]
        if m % 4 == 0:
            return [c(("G4","B4"), 2), r(3)]
        return [r(5)]
    if sec == "C":
        if block % 2 == 0:
            return [n("E5", 2), r(1), n("G5", 1.5), r(0.5)] if m % 3 == 0 else [r(5)]
        return [c(("G4","B4","D5"), 1.5), r(3.5)] if m % 4 == 1 else [r(5)]
    if sec == "D":
        return [c(("G4","B4","D5"), 2), r(1), n("A4", 1.5), r(0.5)]
    if sec == "E":
        if m % 4 in (2, 3):
            return [n("E5", 1.5), r(3.5)]
        return [r(5)]
    if sec == "F":
        if m % 5 in (1, 3):
            return [n("A4", 2), r(3)]
        return [r(5)]
    return [r(5)]

def cello_content(sec, bar, m):
    if sec == "D":
        return [n("E2", 1), n("A2", 1), n("E2", 1.5), r(1.5)]
    if sec == "A":
        if m % 6 >= 3:
            return [n("E2", 2), r(3)]
        return [r(5)]
    if sec == "B":
        return [n("E2", 1), r(4)]
    if sec == "C":
        return [n("A2", 2), r(3)]
    if sec == "E":
        return [n("E2", 2), r(3)]
    if sec == "F":
        return [n("A2", 2), r(3)]
    return [r(5)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Eviscerating Angels"
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

    last_chord_sym = None
    for m in range(1, 73):
        sec = section(m)
        bar = bar_in(m, sec)
        block = (m - 1) // 6

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))
            mm = tempo.MetronomeMark(number=76, referent=note.Note(type='quarter'))
            mm.text = "Slowly, tense and floating"
            mg.insert(0, mm)
            mg.insert(0, dynamics.Dynamic("pp"))

        # Rehearsal letter at section start
        if m in (1, 13, 25, 37, 49, 61):
            rm = expressions.RehearsalMark(["A","B","C","D","E","F"][(m-1)//12])
            mg.insert(0, rm)
        # Dynamics at section starts
        if m == 37:
            mg.insert(0, dynamics.Dynamic("mf"))
        if m == 49:
            mg.insert(0, dynamics.Dynamic("mp"))
        if m == 61:
            mg.insert(0, dynamics.Dynamic("pp"))

        content, chord_sym = guitar_content(sec, bar, m)
        if chord_sym and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        elif sec in ("E", "F") and bar > 4:
            last_chord_sym = None
        for e in content:
            mg.append(e)
        parts["gtr"].append(mg)

        # Viola
        mvla = stream.Measure(number=m)
        mvla.timeSignature = meter.TimeSignature("5/4")
        for e in viola_content(sec, bar, m, block):
            mvla.append(e)
        parts["vla"].append(mvla)

        # Violin I
        mvn1 = stream.Measure(number=m)
        mvn1.timeSignature = meter.TimeSignature("5/4")
        for e in violin1_content(sec, bar, m):
            mvn1.append(e)
        parts["vn1"].append(mvn1)

        # Violin II
        mvn2 = stream.Measure(number=m)
        mvn2.timeSignature = meter.TimeSignature("5/4")
        for e in violin2_content(sec, bar, m, block):
            mvn2.append(e)
        parts["vn2"].append(mvn2)

        # Cello
        mvc = stream.Measure(number=m)
        mvc.timeSignature = meter.TimeSignature("5/4")
        for e in cello_content(sec, bar, m):
            mvc.append(e)
        parts["vc"].append(mvc)

        # Double barline at end of section (before A→B, B→C, etc.)
        if m in (12, 24, 36, 48, 60):
            mg.rightBarline = Barline('double')

    for p in parts.values():
        s.append(p)
    return s

def fix_redundant_time_sigs(path):
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
    # Box rehearsal letters (enclosure="rectangle")
    content = re.sub(r'<rehearsal enclosure="none"', r'<rehearsal enclosure="rectangle"', content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    score = build_score()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V3Eviscerating_Angels.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant_time_sigs(out)
    print("Fixed redundant time signatures.")

if __name__ == "__main__":
    main()
