#!/usr/bin/env python3
"""
Eviscerating Angels V2 - Guitar and String Quartet
GCE 9.4+ target. Wayne Shorter + Frisell atmosphere.
Improvements: irregular guitar rhythms, dyads/triads, viola counterline,
harmonic bloom climax, violin-guitar dialogue, textural evolution every 6-8 bars.
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

# Irregular rhythm patterns (quarters = 1.0) — anti-monotony
RHYTHM_PATTERNS = [
    [2.0, 0.5, 1.5, 1.0],      # original
    [1.5, 1.0, 0.5, 2.0],       # shifted
    [1.0, 1.0, 1.0, 2.0],       # three shorts + long
    [2.5, 0.25, 0.25, 2.0],     # long + two eighths + long
    [0.5, 2.0, 1.0, 1.5],       # eighth + half + quarter + dotted
    [1.0, 2.0, 0.5, 1.5],       # quarter + half + eighth + dotted
    [2.0, 1.0, 1.5, 0.5],       # half + quarter + dotted + eighth
    [1.5, 0.5, 2.0, 1.0],       # dotted + eighth + half + quarter
]

def get_rhythm(m, sec):
    """Vary rhythm every 6-8 bars; avoid same pattern twice in a row."""
    block = (m - 1) // 6
    idx = (block + hash(sec) % 100) % len(RHYTHM_PATTERNS)
    return RHYTHM_PATTERNS[idx]

# Dark harmonic palette — A minor / E minor, Wayne Shorter + Frisell
def guitar_a(bar):
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C5")],
        [("E4","G#4","B4"), ("D4","F#4","A4"), ("C4","E4","G4"), ("B3","D4","F#4")],
        [("A3","E4"), ("G4","D5"), ("E4","B4","G5"), ("A3","C#4","E4")],
        [("F#4","C#5"), ("G4","D5"), ("E4","B4"), ("A3","E4","B4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

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
        [("E4","B4","G5"), ("A3","E4"), ("rest"), ("rest")],
    ]
    if bar < 8:
        return blocks[bar // 4 % 2][bar % 4]
    return "rest"

# Moving double-stops (parallel voice leading) for extra guitar texture
def moving_dyads(bar, sec):
    """Returns (dyad1, dyad2) for moving double-stop gesture or None."""
    if sec == "A":
        pairs = [("A3","E4", "G3","D4"), ("E4","B4", "D4","A4"), ("G3","D4", "A3","E4")]
        return pairs[bar % 3]
    if sec == "B":
        pairs = [("E3","B3", "G3","D4"), ("A3","E4", "C4","G4"), ("D4","F#4", "E4","B4")]
        return pairs[bar % 3]
    return None

def guitar_content(sec, bar, m):
    pit = guitar_a(bar) if sec == "A" else guitar_b(bar) if sec == "B" else guitar_c(bar)
    if pit == "rest":
        return [r(5)]
    if isinstance(pit, str):
        pit = (pit,)
    rhythm = get_rhythm(m, sec)
    # Use moving double-stops every 5th bar for variety
    if bar % 5 == 3 and moving_dyads(bar, sec):
        d1, d2, d3, d4 = moving_dyads(bar, sec)
        return [
            c((d1, d2), rhythm[0]),
            r(rhythm[1]),
            c((d3, d4), rhythm[2]),
            r(rhythm[3]),
        ]
    if len(pit) >= 3:
        return [
            c(pit, rhythm[0]),
            r(rhythm[1]),
            c((pit[0], pit[1]), rhythm[2]),
            r(rhythm[3]),
        ]
    if len(pit) == 2:
        return [c(pit, rhythm[0]), r(rhythm[1]), c(pit, rhythm[2]), r(rhythm[3])]
    return [n(pit[0], rhythm[0]), r(sum(rhythm[1:]))]

def section(m):
    if m <= 24: return "A"
    if m <= 48: return "B"
    return "C"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 25
    return m - 49

# Harmonic bloom climax: bars 35-42 (within B)
def in_bloom(m):
    return 35 <= m <= 42

# Viola continuous interior counterline — never more than 1 bar rest
def viola_content(sec, bar, m, block):
    if in_bloom(m):
        # Bloom: fuller harmonies
        bloom_voicings = [
            ("B3","D4","F#4","A4"), ("C4","E4","G4"), ("D4","F#4","A4"),
            ("E4","G#4","B4"), ("A3","C#4","E4"), ("G3","B3","D4"),
        ]
        v = bloom_voicings[bar % len(bloom_voicings)]
        return [c(v, 2.5), r(2.5)]
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
            [n("A4", 1), c(("C4","E4"), 1.5), r(1), n("B3", 1.5)],
            [c(("D4","F#4","A4"), 2), r(0.5), n("G4", 1.5), r(1)],
            [n("E4", 1), r(0.5), c(("G3","B3"), 2), r(1.5)],
        ]
        return lines[bar % 4]
    # C — continuous through end, sparse in dissolution
    if bar < 8:
        lines = [
            [c(("A3","E4","G4"), 2), r(1), n("E4", 1.5), r(0.5)],
            [n("G4", 1), r(1), c(("A3","C#4"), 2), r(1)],
            [r(1), c(("E4","B4"), 2.5), r(1.5)],
        ]
        return lines[bar % 3]
    # bars 8+: sparse sustained counterline
    sparse = [
        [n("A3", 3), r(2)],
        [r(1), n("E4", 2.5), r(1.5)],
        [c(("G3","B3"), 2), r(3)],
        [n("E4", 1.5), r(3.5)],
    ]
    return sparse[bar % 4]

# Violin-guitar dialogue: call and response
def violin1_dialogue(sec, bar, m):
    if in_bloom(m):
        return [c(("E5","G5","B5"), 1.5), r(1), n("A5", 1.5), r(1)]
    if sec == "A":
        if m % 7 in (1, 4):  # respond to guitar
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
        return [n("G5", 2.5), r(1), n("E5", 1), r(0.5)] if m % 3 == 1 else [r(5)]
    return [r(5)]

def violin2_content(sec, bar, m, block):
    """Texture evolution: activate every 6-8 bars."""
    if block % 2 == 1 and sec != "A":  # B and C, odd blocks
        if sec == "B" and m % 4 == 2:
            return [n("B4", 1), r(2), n("D5", 1), r(1)]
        if sec == "C" and m % 3 == 0:
            return [n("E5", 2), r(3)]
    if in_bloom(m):
        return [c(("G4","B4","D5"), 2), r(3)]
    return [r(5)]

def cello_content(sec, bar, m):
    if in_bloom(m):
        return [n("E2", 1), n("A2", 1), n("E2", 1.5), r(1.5)]
    if sec == "A":
        if m % 6 >= 3:
            return [n("E2", 2), r(3)]
        return [r(5)]
    if sec == "B":
        return [n("E2", 1), r(4)]
    if sec == "C":
        return [n("E2", 2), r(3)]
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

    for m in range(1, 73):
        sec = section(m)
        bar = bar_in(m, sec)
        block = (m - 1) // 6

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))
            mg.insert(0, tempo.MetronomeMark(number=76, referent=note.Note(type='quarter')))
        for e in guitar_content(sec, bar, m):
            mg.append(e)
        parts["gtr"].append(mg)

        # Viola — continuous counterline
        mvla = stream.Measure(number=m)
        mvla.timeSignature = meter.TimeSignature("5/4")
        for e in viola_content(sec, bar, m, block):
            mvla.append(e)
        parts["vla"].append(mvla)

        # Violin I — dialogue
        mvn1 = stream.Measure(number=m)
        mvn1.timeSignature = meter.TimeSignature("5/4")
        for e in violin1_dialogue(sec, bar, m):
            mvn1.append(e)
        parts["vn1"].append(mvn1)

        # Violin II — texture evolution
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

def fix_redundant_time_sigs(path):
    """Remove redundant time signatures from MusicXML."""
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

def main():
    score = build_score()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V2Eviscerating_Angels.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant_time_sigs(out)
    print("Fixed redundant time signatures.")

if __name__ == "__main__":
    main()
