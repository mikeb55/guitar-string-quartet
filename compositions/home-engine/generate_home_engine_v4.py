#!/usr/bin/env python3
"""
Home Engine V4 - Guitar and String Quartet
Target: 10/10 ECM chamber-jazz. Scofield–Holland + Zappa (controlled contrast).

V4 improvements over V3:
- 7-section form with E (harmonic bloom / emotional apex)
- Stronger climax: widest register, richest sonority, guitar/string dialogue
- Harmonic propulsion: chromatic approach, bass-led pivots
- Guitar: moving dyads, quartal fragments, triad-pair, varied rhythm, answers strings
- Strings: Vn1 motif transformation + registral lift; Vn2 secondary melodic; Viola continuous; Cello spine
- Rhythmic vitality: no square phrasing, displaced accents, variation every 4-6 bars
- Multi-voice chamber interaction in A, C, E

Form: A(1-16) B(17-32) C(33-48) D(49-62 Zappa) E(63-80 climax) A'(81-94) Coda(95-108)
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
    if m <= 16: return "A"
    if m <= 32: return "B"
    if m <= 48: return "C"
    if m <= 62: return "D"
    if m <= 80: return "E"
    if m <= 94: return "A2"
    return "Coda"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 17
    if sec == "C": return m - 33
    if sec == "D": return m - 49
    if sec == "E": return m - 63
    if sec == "A2": return m - 81
    return m - 95

# Harmonic propulsion — forward gravity, chromatic approach
def chord_for_section(sec, bar, m):
    if sec == "A":
        return "Dm9"
    if sec == "B":
        return "G13sus" if bar % 2 == 0 else "Dm9"
    if sec == "C":
        return "Bbmaj7#11" if bar % 3 != 2 else "Fmaj9"
    if sec == "D":
        opts = ["A7alt", "Bbmaj7#11", "Fmaj9", "Dm9"]
        return opts[bar % 4]
    if sec == "E":
        return "Fmaj9" if bar % 4 < 2 else "Bbmaj7#11"
    if sec == "A2":
        return "Dm9"
    return "Dm9"

# Rhythmic vitality — varied, no square; each 4-tuple sums to 4
RHYTHM = [
    [0.5, 1.0, 0.5, 2.0],
    [1.0, 0.5, 1.5, 1.0],
    [0.5, 1.5, 0.5, 1.5],
    [1.5, 0.5, 1.0, 1.0],
    [0.25, 1.5, 0.5, 1.75],
    [1.0, 0.5, 1.0, 1.5],
    [0.5, 1.0, 1.0, 1.5],
    [1.25, 0.5, 1.0, 1.25],
]

def get_rhythm(m, sec, bar):
    idx = ((m - 1) // 4 + bar + hash(sec) % 8) % len(RHYTHM)
    return RHYTHM[idx]

# Guitar — moving dyads, quartal, triad-pair, chord stabs; no monophonic
def guitar_a(bar):
    blocks = [
        [("D3", "F3"), ("A3", "C4"), ("D4", "F4"), ("A3", "E4")],
        [("D3", "F3", "A3"), ("C4", "E4"), ("D4", "F4"), ("A3", "C4")],
        [("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "F3")],
        [("D3", "F3", "A3", "C4"), ("A3", "E4"), ("D4", "F4"), ("A3", "C4")],
        [("D3", "G3"), ("A3", "D4"), ("F3", "A3"), ("C4", "E4")],
    ]
    return blocks[(bar // 4 + bar) % 5][bar % 4]

def guitar_b(bar):
    blocks = [
        [("G3", "C4"), ("D4", "F4"), ("A3", "E4"), ("D3", "F3")],
        [("G3", "D4", "F4"), ("C4", "E4"), ("D4", "A4"), ("G3", "C4")],
        [("D3", "F3"), ("A3", "C4"), ("G3", "D4"), ("C4", "F4")],
        [("G3", "C4", "D4"), ("F4", "A4"), ("G3", "D4"), ("C4", "E4")],
    ]
    return blocks[(bar // 4) % 4][bar % 4]

def guitar_c(bar):
    blocks = [
        [("Bb3", "D4"), ("F4", "A4"), ("Bb3", "E4"), ("F3", "A3")],
        [("F3", "A3", "C4"), ("E4", "G4"), ("Bb3", "D4"), ("F4", "A4")],
        [("Bb3", "F4"), ("D4", "A4"), ("F3", "C4"), ("Bb3", "E4")],
        [("Bb3", "D4", "E4"), ("F3", "A3", "C4"), ("Bb3", "F4"), ("D4", "A4")],
    ]
    return blocks[(bar // 4) % 4][bar % 4]

def guitar_d(bar):
    blocks = [
        [("A3", "C#4", "G4"), ("Bb3", "E4", "F4"), ("A3", "Eb4", "G4"), ("D3", "F3", "A3")],
        [("Bb3", "D4", "E4"), ("F3", "A3", "C4"), ("A3", "C#4", "G4"), ("Bb3", "F4")],
        [("D3", "F3"), ("A3", "C#4"), ("Bb3", "E4"), ("F3", "A3", "C4")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_e(bar):
    """E: Harmonic bloom — stacked triads, quartal, widest register"""
    blocks = [
        [("F3", "A3", "C4", "E4"), ("Bb3", "D4", "F4", "A4"), ("F3", "A3", "C4"), ("Bb3", "E4", "A4")],
        [("Bb3", "D4", "E4"), ("F4", "A4", "C5"), ("Bb3", "F4", "A4"), ("F3", "A3", "C4")],
        [("F3", "A3", "C4"), ("E4", "G4", "Bb4"), ("F4", "A4"), ("Bb3", "D4")],
        [("Bb3", "D4", "F4"), ("A4", "C5", "E5"), ("Bb3", "E4"), ("F4", "A4")],
    ]
    return blocks[(bar // 4) % 4][bar % 4]

def guitar_a2(bar):
    blocks = [
        [("D4", "F4"), ("A3", "C4"), ("D3", "F3"), ("A3", "E4")],
        [("D3", "F3", "A3"), ("C4", "E4"), ("D4", "F4"), ("A3", "C4")],
        [("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "F3")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_coda(bar):
    if bar < 12:
        frags = [
            ("D4", "F4"), ("A3", "C4"), ("D3", "F3"), ("rest"),
            ("D3", "F3"), ("A3", "E4"), ("rest"), ("rest"),
            ("D4", "F4"), ("rest"), ("D3", "F3"), ("rest"),
        ]
        return frags[bar]
    return "rest"

def guitar_content(sec, bar, m):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    elif sec == "D": pit = guitar_d(bar)
    elif sec == "E": pit = guitar_e(bar)
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

# Viola — continuous interior counterline; harmonic friction
def viola_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        lines = [
            [c(("A3", "C4", "E4"), 1.5), r(0.5), n("F4", 1), r(1)],
            [n("D4", 1), r(0.5), c(("F3", "A3"), 1.5), r(1)],
            [c(("A3", "C4"), 1), r(1), n("D4", 1), r(1)],
            [n("F4", 0.5), r(0.5), c(("A3", "C4", "E4"), 1.5), r(1.5)],
        ]
        return lines[(bar + block) % 4]
    if sec == "B":
        lines = [
            [c(("C4", "E4", "G4"), 1.5), r(0.5), n("A4", 1), r(1)],
            [n("G4", 1), r(0.5), c(("D4", "F4"), 1.5), r(1)],
            [c(("A3", "C4"), 1), r(1), n("G4", 1), r(1)],
            [n("D4", 1.5), r(0.5), c(("F4", "A4"), 1), r(1)],
        ]
        return lines[(bar + block) % 4]
    if sec == "C":
        lines = [
            [c(("F3", "A3", "C4"), 1.5), r(0.5), n("Bb3", 1), r(1)],
            [n("D4", 1), r(0.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("F3", "A3"), 1), r(1), n("C4", 1), r(1)],
            [n("Bb3", 1), c(("D4", "F4"), 1.5), r(1.5)],
        ]
        return lines[(bar + block) % 4]
    if sec == "D":
        return [
            c(("A3", "C#4", "E4", "G4"), 0.25), r(0.75),
            c(("A3", "C#4", "E4", "G4"), 0.25), r(1.5),
            c(("A3", "C#4", "E4", "G4"), 0.25), r(0.5),
        ]
    if sec == "E":
        return [c(("A3", "C4", "E4", "F4"), 1.5), r(0.5), c(("Bb3", "D4"), 1), r(1)]
    if sec == "A2":
        return [c(("D3", "F3", "A3"), 1.5), r(0.5), n("C4", 1), r(1)]
    if sec == "Coda":
        return [n("D4", 2), r(2)] if bar < 10 else [r(4)]
    return [r(4)]

# Violin I — motif transformation, registral lift in climax
def violin1_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        if m % 4 in (1, 3) or m % 5 == 2:
            return [n("A5", 1.5), r(0.5), n("F5", 1), r(1)]
        if m % 6 == 0:
            return [c(("A5", "C6"), 0.5), r(1), n("F5", 1), r(1.5)]
        return [r(4)]
    if sec == "B":
        if m % 4 == 1 or m % 5 == 2:
            return [c(("G5", "A5"), 0.5), r(1), n("D5", 1), r(1.5)]
        return [r(4)]
    if sec == "C":
        if m % 3 == 0 or m % 5 == 1:
            return [n("Bb5", 1.5), r(0.5), n("F5", 1), r(1)]
        return [r(4)]
    if sec == "D":
        return [c(("A5", "C#6", "G6"), 0.25), r(0.75), n("E5", 0.25), r(2.75)]
    if sec == "E":
        return [c(("F5", "A5", "C6"), 1), r(1), n("Bb5", 1), r(1)]
    if sec == "A2":
        if m % 4 == 1 or m % 5 == 2:
            return [n("A5", 2), r(1), n("F5", 0.5), r(0.5)]
        return [r(4)]
    if sec == "Coda":
        return [n("A5", 2), r(2)] if bar < 8 else [r(4)]
    return [r(4)]

# Violin II — secondary melodic voice, rhythmic replies
def violin2_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        if m % 4 == 2 or m % 5 == 0:
            return [n("C5", 1), r(2), n("E5", 0.5), r(0.5)]
        if m % 6 == 3:
            return [c(("C5", "E5"), 0.5), r(2), n("A4", 0.5), r(1)]
        return [r(4)]
    if sec == "B":
        if m % 3 == 0 or m % 5 == 2:
            return [n("D5", 1), r(2), n("F5", 0.5), r(0.5)]
        return [r(4)]
    if sec == "C":
        if bar % 2 == 0 or m % 5 == 3:
            return [c(("F4", "A4"), 1), r(3)]
        return [r(4)]
    if sec == "D":
        return [r(0.5), c(("A4", "C#5", "E5"), 0.25), r(3.25)]
    if sec == "E":
        return [c(("A4", "C5", "E5"), 1.5), r(2.5)]
    if sec == "A2":
        if m % 5 == 2 or m % 6 == 3:
            return [n("C5", 1), r(3)]
        return [r(4)]
    return [r(4)]

# Cello — harmonic spine, drive transitions, rhythmic life
def cello_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        patterns = [
            [n("D2", 1), n("A2", 1), n("D2", 1), r(1)],
            [n("D2", 1), n("F2", 1), n("A2", 1), r(1)],
            [n("A2", 1), n("D2", 1), n("A2", 1), r(1)],
            [n("D2", 1.5), n("A2", 0.5), n("D2", 1), r(1)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "B":
        patterns = [
            [n("G2", 1), n("D3", 1), n("G2", 1), r(1)],
            [n("G2", 1), n("A2", 1), n("D3", 1), r(1)],
            [n("D3", 1), n("G2", 1), n("D3", 1), r(1)],
            [n("G2", 1.5), n("D3", 0.5), n("G2", 1), r(1)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "C":
        patterns = [
            [n("Bb2", 1), n("F2", 1), n("Bb2", 1), r(1)],
            [n("Bb2", 1), n("C3", 1), n("F2", 1), r(1)],
            [n("F2", 1), n("Bb2", 1), n("F2", 1), r(1)],
            [n("Bb2", 1.5), n("F2", 0.5), n("Bb2", 1), r(1)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "D":
        return [n("A2", 0.5), r(0.5), n("Bb2", 0.5), r(0.5), n("A2", 1), r(1)]
    if sec == "E":
        return [n("F2", 1), n("C3", 1), n("Bb2", 1), r(1)]
    if sec == "A2":
        patterns = [
            [n("D2", 2), r(2)],
            [n("D2", 1), n("A2", 1), r(2)],
            [n("A2", 1), n("D2", 1), r(2)],
        ]
        return patterns[(bar + block) % 3]
    if sec == "Coda" and bar < 12:
        return [n("D2", 2), r(2)]
    return [r(4)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Home Engine"
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

    section_starts = [1, 17, 33, 49, 63, 81, 95]
    section_labels = ["A", "B", "C", "D", "E", "A'", "Coda"]

    last_chord_sym = None
    for m in range(1, 109):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))
            mm = tempo.MetronomeMark(number=104, referent=note.Note(type='quarter'))
            mg.insert(0, mm)
            mg.insert(0, dynamics.Dynamic("mp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m == 49:
            mg.insert(0, dynamics.Dynamic("ff"))
        elif m == 63:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m in (17, 33):
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 81:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 95:
            mg.insert(0, dynamics.Dynamic("pp"))

        content, chord_sym = guitar_content(sec, bar, m)
        if chord_sym and chord_sym != last_chord_sym:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord_sym = chord_sym
        for e in content:
            mg.append(e)

        if m in (16, 32, 48, 62, 80, 94):
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
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V4_Home_Engine_Scofield.musicxml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant(out)
    print("Fixed redundant time signatures and boxed rehearsal marks.")

if __name__ == "__main__":
    main()
