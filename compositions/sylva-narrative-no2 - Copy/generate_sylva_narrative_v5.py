#!/usr/bin/env python3
"""
Sylva Narrative No.2 V5 - Guitar and String Quartet
GCE 9.6-9.8 target. Wayne Shorter + Frisell + ECM.
Structure: A (motif emergence) → B (rhythmic destabilization) → C (contrapuntal expansion)
→ D (harmonic bloom climax) → A′ (transformed return) → Coda (dissolution)
Primary motif: D-E-G-A. Development through inversion, expansion, displacement.
"""
import os
from music21 import stream, note, chord, duration, tempo, key, metadata, meter
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

# === SECTION MAP (88 bars) ===
def section(m):
    if m <= 16: return "A"    # motif emergence
    if m <= 32: return "B"    # rhythmic destabilization
    if m <= 48: return "C"    # contrapuntal expansion
    if m <= 60: return "D"    # harmonic bloom climax
    if m <= 76: return "A2"   # transformed return
    return "Coda"             # dissolution (77-88)

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 17
    if sec == "C": return m - 33
    if sec == "D": return m - 49
    if sec == "A2": return m - 61
    return m - 77

# === RHYTHM PATTERNS (anti-monotony: max 2 repeats) ===
# A: stable; B: destabilized (syncopation, odd groupings); C: flowing; D: dense; A': varied; Coda: sparse
RHYTHM_A = [[2.0, 0.5, 1.5, 1.0], [1.5, 1.0, 0.5, 2.0]]
RHYTHM_B = [[1.0, 1.5, 0.5, 2.0], [0.5, 2.0, 1.0, 1.5], [2.5, 0.25, 0.25, 2.0], [1.0, 1.0, 1.0, 2.0]]
RHYTHM_C = [[2.0, 1.0, 1.5, 0.5], [1.5, 0.5, 2.0, 1.0], [2.0, 0.5, 1.5, 1.0]]
RHYTHM_D = [[1.5, 1.0, 1.5, 1.0], [2.0, 1.0, 1.0, 1.0], [1.0, 2.0, 1.0, 1.0]]
RHYTHM_A2 = [[2.0, 0.5, 1.5, 1.0], [1.0, 2.0, 0.5, 1.5], [1.5, 1.0, 0.5, 2.0]]
RHYTHM_CODA = [[3.0, 2.0], [2.0, 3.0], [4.0, 1.0], [1.0, 4.0]]

def get_rhythm(m, sec, bar):
    block = (m - 1) // 6
    if sec == "A": pats = RHYTHM_A
    elif sec == "B": pats = RHYTHM_B
    elif sec == "C": pats = RHYTHM_C
    elif sec == "D": pats = RHYTHM_D
    elif sec == "A2": pats = RHYTHM_A2
    else: pats = RHYTHM_CODA
    return pats[(block + bar) % len(pats)]

# === PRIMARY MOTIF: D-E-G-A (pitch classes) ===
# A: original; B: interval expansion; C: inversion hints; D: stacked; A': harmonic reinterpretation; Coda: fragment

def guitar_a(bar):
    """A: Motif emergence — D Lydian, original D-E-G-A"""
    blocks = [
        [("D3","A3","F#4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C#5")],
        [("D4","F#4","A4"), ("E4","G4","B4"), ("A3","C#4","E4"), ("G3","B3","D4")],
        [("D4","A4"), ("E4","B4"), ("G4","D5"), ("A3","E4","A4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_b(bar):
    """B: Rhythmic destabilization — interval expansion, G Lydian"""
    blocks = [
        [("G3","D4","B4"), ("A4","E5"), ("B3","F#4","D5"), ("C#4","G#4","E5")],
        [("D4","G4","B4"), ("E4","A4","C#5"), ("G3","C#4","E4"), ("A3","D4","F#4")],
        [("G4","D5"), ("A4","E5"), ("B4","F#5"), ("E4","A4","C#5")],
        [("G3","D4"), ("A3","E4","G4"), ("B3","F#4","A4"), ("D4","G4","B4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def guitar_c(bar):
    """C: Contrapuntal expansion — A Dorian, quartal fragments"""
    blocks = [
        [("A3","E4","G4"), ("B4","F#5"), ("C#4","E4","A4"), ("D4","F#4","B4")],
        [("E4","A4","C#5"), ("G4","B4","D5"), ("A3","E4","G4"), ("B3","F#4","A4")],
        [("A4","E5"), ("G4","D5"), ("E4","B4"), ("A3","E4")],
        [("D4","G4","A4"), ("E4","A4","B4"), ("G3","C4","E4"), ("A3","D4","F#4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def guitar_d(bar):
    """D: Harmonic bloom — stacked triads, quartal, widest register"""
    blocks = [
        [("D3","F#4","A4","D5"), ("E3","G4","B4","E5"), ("G3","B4","D5","G5"), ("A3","C#4","E4","A4")],
        [("D4","F#4","A4","C#5"), ("G3","D4","B4","D5"), ("A3","E4","G4","B4"), ("D3","A3","F#4","A4")],
        [("E4","G#4","B4"), ("D4","F#4","A4"), ("G3","B3","D4","G4"), ("A3","E4","C#5")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_a2(bar):
    """A': Transformed return — inversion, register displacement"""
    blocks = [
        [("D4","F#4","A4"), ("E4","G4","B4"), ("A3","E4","C#5"), ("D3","A3","F#4")],
        [("G3","D4","B4"), ("A3","E4","G4"), ("D4","A4"), ("E4","B4")],
        [("A4","E5"), ("G4","D5"), ("D4","A4"), ("E4","B4")],
        [("rest"), ("rest"), ("rest"), ("rest")],
    ]
    if bar < 12:
        return blocks[bar // 4 % 4][bar % 4]
    return "rest"

def guitar_coda(bar):
    """Coda: Dissolution — sparse, fragmentary"""
    if bar < 6:
        frags = [("D4","A4"), ("E4","B4"), ("G3","D4"), ("A3","E4"), ("D3","F#4"), ("rest")]
        return frags[bar]
    return "rest"

# Moving dyads for guitar (40-50% dyads target)
def moving_dyads(bar, sec):
    if sec == "A": return [("D3","A3", "G3","D4"), ("E4","B4", "D4","A4"), ("A3","E4", "G3","D4")]
    if sec == "B": return [("G3","D4", "A3","E4"), ("B3","F#4", "E4","B4"), ("D4","G4", "C#4","G#4")]
    if sec == "C": return [("A3","E4", "G4","D5"), ("E4","B4", "A3","E4"), ("D4","F#4", "B3","F#4")]
    if sec == "D": return [("D3","A3", "D4","A4"), ("G3","D4", "G4","D5")]
    if sec == "A2": return [("D4","A4", "G3","D4"), ("E4","B4", "A3","E4")]
    return None

# Guitar content with distribution: 40-50% dyads, 25-35% triads, 10-20% sustained, 10-15% single-note
def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "D": pit = guitar_d(bar)
    elif sec == "A2": pit = guitar_a2(bar)
    else: pit = guitar_coda(bar)

    if pit == "rest":
        return [r(5)]
    if isinstance(pit, str):
        pit = (pit,)

    rhythm = get_rhythm(m, sec, bar)
    if sec == "Coda" and len(rhythm) == 2:
        if pit == ("rest",):
            return [r(5)]
        return [c(pit, rhythm[0]) if len(pit) > 1 else n(pit[0], rhythm[0]), r(rhythm[1])]

    # Dyad gesture every 4th bar (moving double-stops)
    if bar % 4 == 2 and moving_dyads(bar, sec):
        pairs = moving_dyads(bar, sec)
        d1, d2, d3, d4 = pairs[bar % len(pairs)]
        return [c((d1, d2), rhythm[0]), r(rhythm[1]), c((d3, d4), rhythm[2]), r(rhythm[3])]

    if len(pit) >= 3:
        return [c(pit, rhythm[0]), r(rhythm[1]), c((pit[0], pit[1]), rhythm[2]), r(rhythm[3])]
    if len(pit) == 2:
        return [c(pit, rhythm[0]), r(rhythm[1]), c(pit, rhythm[2]), r(rhythm[3])]
    return [n(pit[0], rhythm[0]), r(sum(rhythm[1:]))]

# === VIOLA: Continuous interior counterline (contrapuntal engine) ===
def viola_content(sec, bar, m, block):
    if sec == "A":
        lines = [
            [c(("B3","D4","F#4"), 1.5), r(0.5), n("E4", 1.5), r(1.5)],
            [n("G4", 1), r(0.5), c(("A3","E4"), 2), r(1.5)],
            [c(("D4","F#4"), 2), r(1), n("C#4", 1.5), r(0.5)],
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
    if sec == "D":
        # Climax: densest counterline
        bloom = [
            [c(("B3","D4","F#4","A4"), 2), r(0.5), c(("E4","G#4"), 1.5), r(1)],
            [c(("D4","F#4","A4"), 1.5), r(0.5), n("G4", 2), r(1)],
            [n("A4", 1), c(("C#4","E4","G4"), 2), r(2)],
            [c(("G3","B3","D4"), 2.5), r(1), n("E4", 1), r(0.5)],
        ]
        return bloom[bar % 4]
    if sec == "A2":
        lines = [
            [c(("D4","F#4","A4"), 2), r(1), n("E4", 1.5), r(0.5)],
            [n("G4", 1), r(1), c(("A3","E4"), 2), r(1)],
            [c(("B3","D4","F#4"), 2.5), r(2.5)],
        ]
        return lines[bar % 3] if bar < 12 else [n("D4", 3), r(2)]
    # Coda
    sparse = [[n("D4", 2), r(3)], [r(1), n("A3", 2), r(2)], [c(("G3","B3"), 2.5), r(2.5)]]
    return sparse[bar % 3]

# === VIOLIN I: Motif transformations, dialogue with guitar ===
def violin1_content(sec, bar, m):
    if sec == "A":
        if m % 7 in (1, 4):
            return [n("F#5", 2), r(1), n("A5", 1.5), r(0.5)]
        if m % 8 == 3:
            return [n("E5", 1), r(2), n("G5", 1.5), r(0.5)]
        return [r(5)]
    if sec == "B":
        if m % 6 == 1:
            return [c(("G5","B5"), 0.5), r(1), n("A5", 1), r(2.5)]
        if m % 5 == 2:
            return [n("B5", 1.5), r(1), n("G5", 2), r(0.5)]
        if m % 4 == 0:
            return [n("E5", 2), r(3)]
        return [r(5)]
    if sec == "C":
        if m % 4 in (1, 3):
            return [n("A5", 2), r(1), n("F#5", 1.5), r(0.5)]
        if m % 6 == 2:
            return [c(("E5","G5"), 1.5), r(3.5)]
        return [r(5)]
    if sec == "D":
        # Climax: active motif
        return [c(("F#5","A5","C#6"), 1.5), r(1), n("E5", 1.5), r(1)]
    if sec == "A2":
        if m % 5 in (1, 3):
            return [n("D5", 2.5), r(1), n("F#5", 1), r(0.5)]
        return [r(5)]
    if sec == "Coda":
        if bar < 4:
            return [n("D5", 2), r(3)]
        return [r(5)]

# === VIOLIN II: Harmonic reinforcement, rhythmic contrast ===
def violin2_content(sec, bar, m, block):
    if sec == "A" and block % 2 == 1 and m % 4 == 2:
        return [n("D5", 1), r(2), n("F#5", 1), r(1)]
    if sec == "B" and m % 4 == 2:
        return [n("B4", 1), r(2), n("D5", 1), r(1)]
    if sec == "C" and block % 2 == 0:
        if m % 3 == 0:
            return [n("E5", 2), r(3)]
        if m % 3 == 1:
            return [c(("G4","B4"), 1.5), r(3.5)]
    if sec == "D":
        return [c(("G4","B4","D5"), 2), r(3)]
    if sec == "A2" and m % 6 in (2, 4):
        return [n("A4", 1.5), r(3.5)]
    return [r(5)]

# === CELLO: Pedal tones, contrary motion, rhythmic grounding ===
def cello_content(sec, bar, m):
    if sec == "A":
        if m % 6 >= 3:
            return [n("D2", 2), r(3)]
        return [r(5)]
    if sec == "B":
        return [n("G2", 1), r(4)]
    if sec == "C":
        return [n("A2", 2), r(3)]
    if sec == "D":
        return [n("D2", 1), n("A2", 1), n("D2", 1.5), r(1.5)]
    if sec == "A2":
        return [n("D2", 2), r(3)]
    if sec == "Coda":
        if bar < 8:
            return [n("D2", 3), r(2)]
        return [r(5)]

def fix_redundant_notation(path):
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
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Sylva Narrative No.2"
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

    for m in range(1, 89):
        sec = section(m)
        bar = bar_in(m, sec)
        block = (m - 1) // 6

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(2))
            mg.insert(0, tempo.MetronomeMark(number=72, referent=note.Note(type='quarter')))
        for e in guitar_content(sec, bar, m):
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

    for p in parts.values():
        s.append(p)
    return s

def main():
    score = build()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V5Sylva_Narrative_No2.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant_notation(out)
    print("Fixed redundant time signatures.")

if __name__ == "__main__":
    main()
