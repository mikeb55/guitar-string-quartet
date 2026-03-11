#!/usr/bin/env python3
"""
Myrtle's Prayer V2 – Guitar and String Quartet
Counterpoint / Tonality Hybrid + Wayne Shorter Narrative (light). GCE 9.7–10.

V2 UPGRADES:
- Genuine 4-part string counterpoint in B section
- Guitar: 3+ dyadic passages, 2+ triadic, 1 guitar–violin dialogue, 1 colour-shift section
- Stronger climax (bars 37–42): widest register, violin I ascent, richest sonority
- Smoother voice-leading (stepwise Viola, Violin II)
- Transformed return with suspended calm and release
- Anti-monotony: texture variation every 6–8 bars

Form: A(1-16) B(17-32) C(33-52) D(53-68) A'(69-84) Coda(85-96)
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

# === SECTION MAP (96 bars) ===
def section(m):
    if m <= 16: return "A"
    if m <= 32: return "B"
    if m <= 52: return "C"
    if m <= 68: return "D"
    if m <= 84: return "A2"
    return "Coda"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 17
    if sec == "C": return m - 33
    if sec == "D": return m - 53
    if sec == "A2": return m - 69
    return m - 85

def chord_for_section(sec, bar, m):
    if sec == "A":
        return "Dm9"
    if sec == "B":
        return "Gm9" if bar % 3 != 2 else "Dm9"
    if sec == "C":
        if bar < 6:
            return "Fmaj9"
        if bar < 12:
            return "Bbmaj7#11"
        if bar < 16:
            return "Fmaj9"
        return "Bbmaj7#11"
    if sec == "D":
        return "C13sus" if bar % 2 == 0 else "Dm9"
    if sec == "A2":
        return "Dm9"
    return "Dm9"

def should_insert_chord(m, sec, bar, chord_sym, last_chord_sym):
    if chord_sym is None:
        return False
    if chord_sym != last_chord_sym:
        return True
    if bar % 2 == 0:
        return True
    return False

# === GUITAR V2: More compositionally necessary ===
# 3+ dyadic passages, 2+ triadic, 1 guitar–violin dialogue, 1 colour-shift section
def guitar_a(bar):
    """A: Dyads + triads — moving, not static"""
    blocks = [
        [("D3", "F3", "A3"), ("A3", "C4"), ("D4", "F4"), ("D3", "A3")],
        [("D3", "F3"), ("A3", "E4"), ("D4", "F4"), ("F3", "A3")],
        [("D3", "F3", "A3"), ("A3", "C4"), ("D4", "F4"), ("D3", "F3")],
        [("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "A3")],
    ]
    return blocks[bar % 4][bar % 4]

def guitar_b(bar):
    """B: Dyads, triads, dialogue-ready — active supporting"""
    blocks = [
        [("G3", "B3"), ("D4", "F4"), ("G3", "B3", "D4"), ("A3", "E4")],
        [("D3", "F3"), ("G3", "D4"), ("G3", "B3", "D4"), ("D4", "A4")],
        [("G3", "B3"), ("C4", "E4"), ("D4", "F4"), ("G3", "D4")],
        [("D3", "F3"), ("G3", "B3"), ("A3", "E4"), ("D4", "F4")],
    ]
    return blocks[bar % 4][bar % 4]

def guitar_c(bar):
    """C: Climax — stacked dyads, colour chords, supporting"""
    blocks = [
        [("F3", "A3", "C4"), ("Bb3", "D4", "F4"), ("F4", "A4", "C5"), ("Bb3", "E4", "A4")],
        [("Bb3", "D4"), ("F4", "A4"), ("Bb3", "F4", "A4"), ("F3", "A3", "C4")],
        [("F3", "Bb3"), ("A3", "D4"), ("C4", "F4"), ("Bb3", "E4", "A4")],
        [("Bb3", "D4", "F4"), ("A4", "C5"), ("Bb3", "F4", "A4"), ("F3", "A3")],
        [("F3", "A3", "C4"), ("Bb3", "E4"), ("F4", "A4"), ("Bb3", "D4")],
    ]
    return blocks[(bar // 4) % 5][bar % 4]

def guitar_d(bar):
    """D: Colour-shift section — guitar subtly changes emotional colour"""
    blocks = [
        ("D3", "F3", "A3"),
        ("A3", "C4"),
        ("D4", "F4"),
        ("D3", "F3", "A3"),
        ("C4", "E4"),
        ("D3", "A3"),
    ]
    return blocks[bar % 6]

def guitar_a2(bar):
    """A': Transformed return — dyads, triads, sparse but present"""
    blocks = [
        [("D4", "F4"), ("A3", "C4"), ("D3", "F3"), ("A3", "E4")],
        [("D3", "F3", "A3"), ("D4", "F4"), ("A3", "E4"), ("D4", "F4")],
        [("D3", "A3"), ("F3", "A3"), ("D4", "F4"), ("A3", "C4")],
    ]
    return blocks[bar % 3][bar % 4]

def guitar_coda(bar):
    """Coda: Release — sparse dyads, fading"""
    if bar < 12:
        frags = [
            ("D4", "F4"), ("A3", "C4"), ("D3", "F3"), ("A3", "E4"),
            ("D3", "F3"), ("D4", "F4"), ("A3", "E4"), ("D3", "A3"),
            ("F3", "A3"), ("D4", "F4"), ("A3", "C4"), ("D3", "F3"),
        ]
        return frags[bar]
    return None

def guitar_content(sec, bar, m):
    if sec == "A":
        pit = guitar_a(bar)
    elif sec == "B":
        pit = guitar_b(bar)
    elif sec == "C":
        pit = guitar_c(bar)
    elif sec == "D":
        pit = guitar_d(bar)
    elif sec == "A2":
        pit = guitar_a2(bar)
    else:
        pit = guitar_coda(bar)

    if pit is None:
        return [r(4)], None

    sym = chord_for_section(sec, bar, m)
    if len(pit) >= 3:
        return [c(pit, 2.5), r(1.5)], sym
    if len(pit) == 2:
        return [c(pit, 2), r(2)], sym
    return [c(pit, 2.5), r(1.5)], sym

# === VIOLIN I V2: Expressive arcs, registral lift toward climax ===
def violin1_content(sec, bar, m):
    if sec == "A":
        arcs = [
            [n("A5", 2), r(1), n("F5", 1)],
            [n("F5", 1.5), r(1), n("A5", 1.5)],
            [n("A5", 2), r(1), n("G5", 1)],
            [n("F5", 1), r(1), n("A5", 2)],
        ]
        return arcs[bar % 4] if bar < 12 else [n("A5", 2), r(1), n("F5", 1)]
    if sec == "B":
        # 4-part counterpoint: expressive melodic arc
        arcs = [
            [n("G5", 1.5), n("A5", 1), r(0.5), n("D5", 1)],
            [n("D5", 1), n("E5", 1), n("G5", 1.5), r(0.5)],
            [n("F5", 1), r(1), n("A5", 2)],
            [n("G5", 2), r(1), n("D5", 1)],
        ]
        return arcs[bar % 4]
    if sec == "C":
        # Climax: bars 37-42 = peak, registral lift to C6/D6
        if bar < 6:
            return [n("F5", 1.5), r(1), n("A5", 1.5)]
        if bar < 10:
            return [n("Bb5", 2), r(1), n("F5", 1)]
        if bar < 14:
            return [n("A5", 1), n("Bb5", 1), n("C6", 1.5), r(0.5)]
        if bar < 18:
            return [n("C6", 1.5), r(0.5), n("Bb5", 1.5), r(0.5)]
        return [n("Bb5", 2), r(2)]
    if sec == "D":
        return [n("A5", 3), r(1)] if m % 4 in (1, 3) else [r(4)]
    if sec == "A2":
        arcs = [
            [n("A5", 2), r(1), n("F5", 1)],
            [n("F5", 1.5), r(1), n("A5", 1.5)],
            [n("A5", 2), r(2)],
        ]
        return arcs[bar % 3]
    if sec == "Coda":
        if bar < 8:
            return [n("A5", 2), r(2)]
        if bar < 12:
            return [n("F5", 1.5), r(2.5)]
        return [r(4)]
    return [r(4)]

# === VIOLIN II V2: Active secondary line, harmonic bridge, stepwise motion ===
def violin2_content(sec, bar, m):
    if sec == "A":
        if (m - 1) // 4 % 2 == 1 and m % 3 == 0:
            return [n("C5", 1), n("D5", 1), r(1), n("E5", 1)]
        return [r(4)]
    if sec == "B":
        # 4-part counterpoint: active secondary, rhythmic response
        lines = [
            [n("D5", 1), n("E5", 1), r(1), n("G5", 1)],
            [n("B4", 1), n("C5", 1), n("D5", 1.5), r(0.5)],
            [n("E5", 1), r(1), n("G5", 1.5), r(0.5)],
            [n("D5", 1), n("E5", 1), n("F5", 1), r(1)],
        ]
        return lines[bar % 4]
    if sec == "C":
        lines = [
            [n("F5", 1), n("G5", 1), r(2)],
            [n("Bb4", 1), n("C5", 1), n("D5", 1), r(1)],
            [n("C5", 1.5), r(2.5)],
            [n("D5", 1), n("E5", 1), r(2)],
        ]
        return lines[bar % 4]
    if sec == "D":
        if m % 5 == 2:
            return [n("E5", 1), n("F5", 1.5), r(1.5)]
        return [r(4)]
    if sec == "A2":
        if m % 4 == 2:
            return [n("C5", 1), n("D5", 1), r(2)]
        return [r(4)]
    if sec == "Coda" and bar < 6:
        return [n("C5", 2), r(2)]
    return [r(4)]

# === VIOLA V2: Continuous interior motion, stepwise, motivic fragments ===
def viola_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        lines = [
            [n("A3", 0.5), n("B3", 0.5), n("C4", 1), r(1), n("F4", 1)],
            [n("D4", 1), n("E4", 1), r(1), c(("F3", "A3"), 1)],
            [n("A3", 0.5), n("B3", 0.5), n("C4", 1), r(1), n("D4", 1)],
            [n("F4", 1), n("E4", 1), r(1), c(("A3", "C4"), 1)],
        ]
        return lines[(bar + block) % 4]
    if sec == "B":
        # 4-part counterpoint: continuous interior, stepwise
        lines = [
            [n("B3", 0.5), n("C4", 0.5), n("D4", 1), r(1), n("A4", 1)],
            [n("G4", 1), n("F4", 1), r(1), c(("D4", "F4"), 1)],
            [n("G3", 0.5), n("A3", 0.5), n("B3", 1), r(1), n("D4", 1)],
            [n("F4", 1), n("E4", 1), r(1), c(("A3", "C4"), 1)],
        ]
        return lines[(bar + block) % 4]
    if sec == "C":
        lines = [
            [n("A3", 0.5), n("Bb3", 0.5), n("C4", 1), r(1), n("Bb3", 1)],
            [n("C4", 1), n("Bb3", 0.5), n("A3", 0.5), r(1), c(("Bb3", "D4"), 1)],
            [n("F3", 0.5), n("G3", 0.5), n("A3", 1), r(1), n("C4", 1)],
            [n("Bb3", 1), n("A3", 1), r(1), c(("D4", "F4"), 1)],
            [n("A3", 0.5), n("B3", 0.5), n("C4", 1), r(1), n("E4", 1)],
        ]
        return lines[(bar + block) % 5]
    if sec == "D":
        lines = [
            [n("D4", 1), n("E4", 1), n("F4", 0.5), r(1.5)],
            [n("A3", 0.5), n("B3", 0.5), n("C4", 1), r(2)],
            [n("F4", 0.5), n("E4", 0.5), n("D4", 1.5), r(1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "A2":
        lines = [
            [n("A3", 0.5), n("B3", 0.5), n("C4", 1), r(1), n("F4", 1)],
            [n("D4", 1), n("E4", 1), r(1), c(("F3", "A3"), 1)],
            [n("A3", 0.5), n("B3", 0.5), n("C4", 2), r(1)],
        ]
        return lines[(bar + block) % 3]
    if sec == "Coda":
        return [n("D4", 1), n("E4", 1), r(2)] if bar < 8 else [r(4)]
    return [r(4)]

# === CELLO V2: Harmonic gravity, slow bass, pedal, contrary motion ===
def cello_content(sec, bar, m):
    block = (m - 1) // 4
    if sec == "A":
        patterns = [
            [n("D2", 2), r(2)],
            [n("D2", 1), n("A2", 1), r(2)],
            [n("A2", 1), n("D2", 1), r(2)],
            [n("D2", 2.5), r(1.5)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "B":
        patterns = [
            [n("G2", 2), r(2)],
            [n("G2", 1), n("D3", 1), r(2)],
            [n("D3", 1), n("G2", 1), r(2)],
            [n("G2", 2.5), r(1.5)],
        ]
        return patterns[(bar + block) % 4]
    if sec == "C":
        # Climax: cello anchors arrival
        patterns = [
            [n("F2", 1), n("C3", 1), n("Bb2", 1), r(1)],
            [n("F2", 1), n("Bb2", 1), n("C3", 1), r(1)],
            [n("Bb2", 1), n("F2", 1), n("Bb2", 1), r(1)],
            [n("F2", 2), r(2)],
            [n("Bb2", 1), n("C3", 1), r(2)],
        ]
        return patterns[(bar + block) % 5]
    if sec == "D":
        patterns = [
            [n("D2", 3), r(1)],
            [n("D2", 1), n("A2", 2), r(1)],
            [n("A2", 1), n("D2", 2), r(1)],
        ]
        return patterns[(bar + block) % 3]
    if sec == "A2":
        patterns = [
            [n("D2", 2), r(2)],
            [n("D2", 1), n("A2", 1), r(2)],
            [n("A2", 1), n("D2", 1), r(2)],
        ]
        return patterns[(bar + block) % 3]
    if sec == "Coda" and bar < 8:
        return [n("D2", 2), r(2)]
    return [r(4)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Myrtle's Prayer"
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

    section_starts = [1, 17, 33, 53, 69, 85]
    section_labels = ["A", "B", "C", "D", "A'", "Coda"]

    last_chord_sym = None
    for m in range(1, 97):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))
            mg.insert(0, tempo.MetronomeMark(number=84, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("pp"))

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m == 17:
            mg.insert(0, dynamics.Dynamic("p"))
        elif m == 33:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 37:
            mg.insert(0, dynamics.Dynamic("mf"))
        elif m == 43:
            mg.insert(0, dynamics.Dynamic("mp"))
        elif m == 53:
            mg.insert(0, dynamics.Dynamic("pp"))
        elif m == 69:
            mg.insert(0, dynamics.Dynamic("p"))
        elif m == 85:
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

        if m in (16, 32, 52, 68, 84):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for name, content_fn in [
            ("vla", lambda s=sec, b=bar, mm=m: viola_content(s, b, mm)),
            ("vn1", lambda s=sec, b=bar, mm=m: violin1_content(s, b, mm)),
            ("vn2", lambda s=sec, b=bar, mm=m: violin2_content(s, b, mm)),
            ("vc", lambda s=sec, b=bar, mm=m: cello_content(s, b, mm)),
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
    out = os.path.join(os.path.dirname(__file__), "musicxml", "V2_Myrtles_Prayer.musicxml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")
    fix_redundant(out)
    print("Fixed redundant time signatures and boxed rehearsal marks.")

if __name__ == "__main__":
    main()
