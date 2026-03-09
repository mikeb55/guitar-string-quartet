#!/usr/bin/env python3
"""
Sylva Sketch 2 - Guitar and String Quartet
Engine: Andrew Hill — angular motif, chromatic pivot harmony, asymmetrical form.
Guitar-first, active viola counterline, irregular phrases, anti-monotony.
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

# Chromatic pivot harmony — Andrew Hill style (varied every 4 bars)
# Angular voicings: minor 2nds, tritones, quartal
def guitar_a(bar):
    blocks = [
        [("C#4","D4","F#4"), ("E4","Bb4"), ("G3","C#4","E4"), ("F4","Ab4","C5")],
        [("Bb3","D4","F4"), ("E4","G#4","B4"), ("C#4","F4","A4"), ("D4","F#4","Bb4")],
        [("Ab3","B3","E4"), ("F#4","A4","C#5"), ("G4","Bb4","D5"), ("E4","G4","C5")],
    ]
    return blocks[bar // 4 % 3][bar % 4]

def guitar_b(bar):
    blocks = [
        [("C4","Eb4","G4"), ("B3","D#4","F#4"), ("Db4","F4","Ab4"), ("E4","G#4","C5")],
        [("F#3","A3","C#4"), ("G4","B4","Eb5"), ("A3","C#4","F4"), ("Bb3","D4","F#4")],
        [("Eb4","G4","Bb4"), ("C#4","E4","A4"), ("D4","F4","Ab4"), ("F4","A4","C#5")],
        [("G#3","B3","E4"), ("A4","C5","F5"), ("Bb4","D5","G5"), ("E4","Ab4","B4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def guitar_c(bar):
    blocks = [
        [("C#4","D4","F#4"), ("E4","Bb4"), ("rest"), ("rest")],
    ]
    if bar < 8:
        return blocks[0][bar % 4]
    return "rest"

def guitar_content(sec, bar):
    if sec == "A": pit = guitar_a(bar)
    elif sec == "B": pit = guitar_b(bar)
    else: pit = guitar_c(bar)
    if pit == "rest": return [r(5)]
    if isinstance(pit, str): pit = (pit,)
    if len(pit) >= 3:
        return [c(pit, 2), r(0.5), c((pit[0], pit[1]), 1.5), r(1)]
    elif len(pit) == 2:
        return [c(pit, 2), r(1), c(pit, 2)]
    return [n(pit[0], 2), r(3)]

def section(m):
    if m <= 19: return "A"   # 19 bars
    if m <= 41: return "B"   # 22 bars
    return "C"               # 27 bars (incl. coda)

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 20
    return m - 42

def build():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Sylva Sketch 2"
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

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mg.insert(0, tempo.MetronomeMark(number=88, referent=note.Note(type='quarter')))
        for e in guitar_content(sec, bi):
            mg.append(e)
        parts["gtr"].append(mg)

        # Strings — active viola counterline, irregular entries
        for name in ["vn1", "vn2", "vla", "vc"]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("5/4")

            # Texture change every 6 bars (anti-monotony)
            block = (m - 1) // 6

            if sec == "A":
                if name == "vla" and m % 5 != 0:  # Active viola
                    mx.append(c(("B3","D4","F#4"), 1.5) if block % 2 == 0 else c(("C#4","E4","A4"), 1.5))
                    mx.append(r(3.5))
                elif name == "vn1" and m % 7 in (1, 3):
                    mx.append(n("E5", 1)); mx.append(r(4))
                elif name == "vc" and m % 4 == 1:
                    mx.append(n("E2", 2)); mx.append(r(3))
                else:
                    mx.append(r(5))
            elif sec == "B":
                if name == "vla":
                    mx.append(c(("E4","G#4","B4"), 1) if block % 3 == 0 else c(("F#4","A4","C#5"), 1))
                    mx.append(r(4))
                elif name == "vn1" and m % 6 == 1:
                    mx.append(c(("E5","G5"), 0.5)); mx.append(r(4.5))
                elif name == "vc":
                    mx.append(n("E2", 1)); mx.append(r(4))
                else:
                    mx.append(r(5))
            else:
                if name == "vla" and m < 75:
                    mx.append(c(("B3","E4"), 2)); mx.append(r(3))
                elif name == "vn1":
                    mx.append(n("G5", 3)); mx.append(r(2))
                elif name == "vc":
                    mx.append(n("E2", 2)); mx.append(r(3))
                else:
                    mx.append(r(5))
            parts[name].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def main():
    score = build()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "Sylva_Sketch_2.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
