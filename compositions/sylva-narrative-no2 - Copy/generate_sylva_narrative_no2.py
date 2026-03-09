#!/usr/bin/env python3
"""
Sylva Narrative No.2 - Guitar and String Quartet
Dual Engine: Wayne Shorter (primary) + Frisell Atmosphere (secondary)
Primary: structural logic, motif evolution. Secondary: floating modal harmony, texture.
4-note motif, A-B-C-A', floating modal, active viola, guitar-first.
~5 min, GCE >= 9.
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

# 4-note motif: D-E-G-A. Evolves: A=original, B=interval expansion, C=harmonic expansion, A'=reinterpreted
# Frisell: floating modal — D Lydian, G Lydian, A Dorian (spacious, varied every 4 bars)
def guitar_a(bar):
    """A: Motif intro — D Lydian floating"""
    blocks = [
        [("D3","A3","F#4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C#5")],
        [("D4","F#4","A4"), ("E4","G4","B4"), ("A3","C#4","E4"), ("G3","B3","D4")],
        [("D4","A4"), ("E4","B4"), ("G4","D5"), ("A3","E4","A4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_b(bar):
    """B: Transformation — motif interval expansion, G Lydian"""
    blocks = [
        [("G3","D4","B4"), ("A4","E5"), ("B3","F#4","D5"), ("C#4","G#4","E5")],
        [("D4","G4","B4"), ("E4","A4","C#5"), ("G3","C#4","E4"), ("A3","D4","F#4")],
        [("G4","D5"), ("A4","E5"), ("B4","F#5"), ("E4","A4","C#5")],
        [("G3","D4"), ("A3","E4","G4"), ("B3","F#4","A4"), ("D4","G4","B4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def guitar_c(bar):
    """C: Harmonic expansion — A Dorian, spacious"""
    blocks = [
        [("A3","E4","G4"), ("B4","F#5"), ("C#4","E4","A4"), ("D4","F#4","B4")],
        [("E4","A4","C#5"), ("G4","B4","D5"), ("A3","E4","G4"), ("B3","F#4","A4")],
        [("A4","E5"), ("G4","D5"), ("E4","B4"), ("A3","E4")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_a2(bar):
    """A': Reinterpreted return — D Lydian transformed"""
    blocks = [
        [("D4","F#4","A4"), ("E4","G4","B4"), ("A3","E4","C#5"), ("D3","A3","F#4")],
        [("G3","D4","B4"), ("A3","E4","G4"), ("D4","A4"), ("E4","B4")],
        [("rest"), ("rest"), ("rest"), ("rest")],
    ]
    if bar < 8:
        return blocks[bar // 4 % 3][bar % 4]
    return "rest"

def guitar_content(sec, bar):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    elif sec == "C": pit = guitar_c(bar)
    else: pit = guitar_a2(bar)
    if pit == "rest": return [r(5)]
    if isinstance(pit, str): pit = (pit,)
    if len(pit) >= 3:
        return [c(pit, 2), r(0.5), c((pit[0], pit[1]), 1.5), r(1)]
    elif len(pit) == 2:
        return [c(pit, 2), r(1), c(pit, 2)]
    return [n(pit[0], 2), r(3)]

def section(m):
    if m <= 20: return "A"   # 20 bars
    if m <= 44: return "B"   # 24 bars
    if m <= 68: return "C"   # 24 bars
    return "A2"              # 20 bars (A')

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 21
    if sec == "C": return m - 45
    return m - 69

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
        bi = bar_in(m, sec)
        block = (m - 1) // 6  # Texture change every 6 bars

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(2))  # D major / Lydian
            mg.insert(0, tempo.MetronomeMark(number=72, referent=note.Note(type='quarter')))
        for e in guitar_content(sec, bi):
            mg.append(e)
        parts["gtr"].append(mg)

        # Strings — Frisell spacious, active viola
        for name in ["vn1", "vn2", "vla", "vc"]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("5/4")

            if sec == "A":
                if name == "vla" and m % 5 not in (0, 1):
                    mx.append(c(("B3","D4","F#4"), 2)); mx.append(r(3))
                elif name == "vn1" and m % 7 in (1, 4):
                    mx.append(n("F#5", 2)); mx.append(r(3))
                elif name == "vc" and m % 4 == 1:
                    mx.append(n("D2", 2)); mx.append(r(3))
                else:
                    mx.append(r(5))
            elif sec == "B":
                if name == "vla":
                    mx.append(c(("E4","G4","B4"), 1.5) if block % 2 == 0 else c(("D4","F#4","A4"), 1.5))
                    mx.append(r(3.5))
                elif name == "vn1" and m % 6 == 1:
                    mx.append(c(("G5","B5"), 1)); mx.append(r(4))
                elif name == "vc":
                    mx.append(n("G2", 1)); mx.append(r(4))
                else:
                    mx.append(r(5))
            elif sec == "C":
                if name == "vla" and m < 65:
                    mx.append(c(("A3","E4","G4"), 2)); mx.append(r(3))
                elif name == "vn1":
                    mx.append(n("A5", 2)); mx.append(r(3))
                elif name == "vc":
                    mx.append(n("A2", 2)); mx.append(r(3))
                else:
                    mx.append(r(5))
            else:
                if name == "vla" and m < 82:
                    mx.append(c(("D4","F#4","A4"), 2)); mx.append(r(3))
                elif name == "vn1":
                    mx.append(n("D5", 3)); mx.append(r(2))
                elif name == "vc":
                    mx.append(n("D2", 2)); mx.append(r(3))
                else:
                    mx.append(r(5))
            parts[name].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def main():
    score = build()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "Sylva_Narrative_No2.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
