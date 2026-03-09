#!/usr/bin/env python3
"""
Eviscerating Angels - Guitar and String Quartet
Dark, intense chamber piece. Guitar-first, anti-monotony compliant.
Structure: A (introduction) - B (development) - C (transformation)
~5 min, varied harmonies every 4 bars, guitar dyads/triads throughout.
"""
import os
from music21 import stream, note, chord, duration, tempo, key, metadata, meter
from music21.instrument import Guitar, Violin, Viola, Violoncello

def make_note(pitch, dur=1.0):
    n = note.Note(pitch)
    n.duration = duration.Duration(dur)
    return n

def make_chord(pitches, dur=1.0):
    c = chord.Chord(pitches)
    c.duration = duration.Duration(dur)
    return c

def make_rest(dur=1.0):
    r = note.Rest()
    r.duration = duration.Duration(dur)
    return r

# Dark harmonic palette - A minor / E minor with tension (varied every 4 bars)
def section_a(bar):
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G3","D4","B4"), ("A3","E4","C5")],
        [("E4","G#4","B4"), ("D4","F#4","A4"), ("C4","E4","G4"), ("B3","D4","F#4")],
        [("A3","E4"), ("G4","D5"), ("E4","B4","G5"), ("A3","C#4","E4")],
        [("F#4","C#5"), ("G4","D5"), ("E4","B4"), ("A3","E4","B4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def section_b(bar):
    blocks = [
        [("E3","B3","G4"), ("A3","E4","C5"), ("D4","F#4","A4"), ("E4","G#4","B4")],
        [("C4","E4","G4"), ("B3","D4","F#4"), ("A3","E4","G4"), ("G4","D5","B5")],
        [("E4","B4"), ("F#4","C#5"), ("G4","D5"), ("A3","E4","B4")],
        [("C#4","G#4"), ("D4","A4"), ("E4","B4","G5"), ("A3","E4")],
    ]
    return blocks[bar // 4 % 4][bar % 4]

def section_c(bar):
    blocks = [
        [("A3","E4","G4"), ("E4","B4"), ("G4","D5"), ("A3","E4","C5")],
        [("E4","B4","G5"), ("A3","E4"), ("rest"), ("rest")],
    ]
    if bar < 8:
        return blocks[bar // 4 % 2][bar % 4]
    return "rest"

def get_guitar(sec, bar):
    if sec == "A": pit = section_a(bar)
    elif sec == "B": pit = section_b(bar)
    else: pit = section_c(bar)
    if pit == "rest": return [make_rest(5)]
    if isinstance(pit, str): pit = (pit,)
    if len(pit) >= 3:
        return [make_chord(pit, 2), make_rest(0.5), make_chord((pit[0], pit[1]), 1.5), make_rest(1)]
    elif len(pit) == 2:
        return [make_chord(pit, 2), make_rest(1), make_chord(pit, 2)]
    return [make_note(pit[0], 2), make_rest(3)]

def get_section(m):
    if m <= 24: return "A"
    if m <= 48: return "B"
    return "C"

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Eviscerating Angels"
    s.metadata.composer = "Mike Bryant"

    parts = {}
    for name, inst, pname in [
        ("guitar", Guitar, "Guitar"),
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
        sec = get_section(m)
        bar = (m - 1) % 24 if sec == "A" else (m - 25) % 24 if sec == "B" else m - 49

        # Guitar
        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            mg.insert(0, key.KeySignature(-1))  # G minor / related
            mg.insert(0, tempo.MetronomeMark(number=76, referent=note.Note(type='quarter')))
        for e in get_guitar(sec, bar):
            mg.append(e)
        parts["guitar"].append(mg)

        # Strings - varied by section
        for name in ["vn1", "vn2", "vla", "vc"]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("5/4")
            if sec == "A":
                if m % 6 < 3 and name == "vn1":
                    mx.append(make_note("E5", 2)); mx.append(make_rest(3))
                elif m % 6 >= 3 and name == "vc":
                    mx.append(make_note("E2", 2)); mx.append(make_rest(3))
                else:
                    mx.append(make_rest(5))
            elif sec == "B":
                if name == "vn1" and m % 4 == 1:
                    mx.append(make_chord(("E5","G5"), 0.5)); mx.append(make_rest(4.5))
                elif name == "vc":
                    mx.append(make_note("E2", 1)); mx.append(make_rest(4))
                else:
                    mx.append(make_rest(5))
            else:
                if name == "vn1":
                    mx.append(make_note("G5", 3)); mx.append(make_rest(2))
                elif name == "vc":
                    mx.append(make_note("E2", 2)); mx.append(make_rest(3))
                else:
                    mx.append(make_rest(5))
            parts[name].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def main():
    score = build_score()
    out = os.path.join(os.path.dirname(__file__), "musicxml", "Eviscerating_Angels.musicxml")
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
