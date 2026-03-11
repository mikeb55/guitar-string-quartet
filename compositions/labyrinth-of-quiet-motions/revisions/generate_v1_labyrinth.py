#!/usr/bin/env python3
"""
Labyrinth of Quiet Motions V1 – Polyphonic Labyrinth / Counterpoint Hybrid
Orbit Album – Guitar + String Quartet

Contrapuntal summit. Motivic seed G-E-C. Diminished pivots. 30%+ reduced texture.
Form: A(1-18) B(19-40) C(41-70 climax) D(71-88) E(89-100)
~100 bars, 5-6 min. ♩=78. GCE ≥ 9.6.
"""
import os
from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    harmony, expressions, dynamics, articulations
)
from music21.bar import Barline
from music21.instrument import Guitar, Violin, Viola, Violoncello

def n(pitch, dur=1.0, art=None):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    if art:
        x.articulations.append(art)
    return x

def c(pitches, dur=1.0):
    x = chord.Chord(pitches)
    x.duration = duration.Duration(dur)
    return x

def r(dur=1.0):
    x = note.Rest()
    x.duration = duration.Duration(dur)
    return x

def section(m):
    if m <= 18: return "A"
    if m <= 40: return "B"
    if m <= 70: return "C"
    if m <= 88: return "D"
    return "E"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 19
    if sec == "C": return m - 41
    if sec == "D": return m - 71
    return m - 89

def texture_mode(m):
    """Reduced texture ~30%: duo/trio. Refresh every 8-12 bars."""
    if m in range(1, 7): return "duo"
    if m in range(19, 25): return "trio"
    if m in range(45, 51): return "full"
    if m in range(71, 78): return "trio"
    if m in range(89, 101): return "thinning"
    return "full"

def guitar_content(sec, bar, m):
    mode = texture_mode(m)
    if sec == "A":
        if mode == "duo" and bar < 4:
            return [c(("G3", "B3"), 2), r(1), c(("E3", "G3"), 1)]
        lines = [
            [c(("E3", "G3"), 2), r(1), c(("A3", "C4"), 1)],
            [r(1), c(("G3", "B3"), 2), c(("E3", "G3"), 1)],
            [c(("E3", "G#3"), 1.5), r(0.5), c(("B3", "D4"), 1), r(1)],
            [c(("C#3", "E3"), 2), r(1), c(("G3", "B3"), 1)],
            [c(("G3", "B3", "D4"), 2), r(1), c(("E3", "G3"), 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "B":
        if mode == "trio" and bar < 4:
            return [c(("E3", "G3", "B3"), 2), r(1), c(("A3", "C4"), 1)]
        lines = [
            [c(("E3", "G3", "B3"), 2), r(1), c(("A3", "C4"), 1)],
            [r(1), c(("G3", "Bb3"), 2), c(("F3", "A3"), 1)],
            [c(("Eb3", "G3"), 1.5), c(("Bb3", "D4"), 1.5), r(1)],
            [c(("C#3", "E3"), 2), c(("G#3", "B3"), 2)],
            [c(("E3", "G3"), 1), c(("A3", "C4"), 1), c(("E3", "G#3"), 1), r(1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "C":
        lines = [
            [c(("E3", "G3"), 1), c(("A3", "C4"), 1), c(("E3", "G#3"), 1), r(1)],
            [c(("G3", "Bb3"), 1), c(("F3", "A3"), 1), c(("Eb3", "G3"), 2)],
            [c(("E3", "B3"), 1), c(("C#4", "E4"), 1), c(("G3", "B3"), 2)],
            [c(("A3", "C#4"), 1), c(("E3", "G3"), 1), c(("B3", "D4"), 2)],
            [c(("G3", "B3"), 1), n("E4", 1), c(("G3", "B3"), 2)],
        ]
        return lines[(bar + m) % 5]
    if sec == "D":
        if mode == "trio" and bar < 5:
            return [c(("E3", "G3"), 2), r(1), c(("A3", "C4"), 1)]
        if bar < 12:
            return [c(("E3", "G3"), 2), r(1), c(("A3", "C4"), 1)]
        return [c(("E3", "B3"), 3), r(1)]
    if sec == "E":
        if bar < 8:
            return [c(("E3", "G3"), 2), r(2)]
        if bar < 11:
            return [c(("E3", "B3"), 4)]
        return [c(("E3", "B3"), 4)]
    return [r(4)]

def violin1_content(sec, bar, m):
    mode = texture_mode(m)
    if sec == "A" and mode == "duo" and bar < 4:
        return [r(4)]
    if sec == "A":
        lines = [
            [r(1), n("G5", 1), n("E5", 1), r(1)],
            [n("E5", 1.5), n("G5", 1), r(1.5)],
            [r(1), n("C5", 2), n("E5", 1)],
            [n("G5", 2), r(1), n("E5", 1)],
            [n("E5", 1), n("G5", 1), n("C5", 2)],
        ]
        return lines[(bar + m) % 5]
    if sec == "B":
        if mode == "trio" and bar in (0, 1):
            return [r(4)]
        lines = [
            [n("G5", 1), n("Bb5", 1), n("G5", 1), r(1)],
            [n("E5", 1), n("G5", 2), n("F#5", 1)],
            [n("G5", 1.5), n("E5", 1), n("C5", 1.5)],
            [n("E5", 2), n("G5", 1), r(1)],
            [n("G5", 1), n("A5", 1), n("G5", 1), n("E5", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "C":
        lines = [
            [n("G5", 1), n("A5", 1), n("G5", 1), n("E5", 1)],
            [n("Bb5", 1), n("G5", 1), n("F5", 2)],
            [n("G5", 1), n("E5", 1), n("C#5", 2)],
            [n("A5", 1), n("G5", 1), n("E5", 2)],
            [n("E5", 1), n("G5", 1), n("Bb5", 1), n("G5", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "D":
        if bar < 15:
            return [n("G5", 2), r(1), n("E5", 1)]
        return [n("G5", 3), r(1)]
    if sec == "E":
        if bar < 10:
            return [n("E5", 2), r(2)]
        if bar < 11:
            return [n("E5", 3), r(1)]
        nh = n("B5", 4)
        nh.articulations.append(articulations.Harmonic())
        return [nh]
    return [r(4)]

def violin2_content(sec, bar, m):
    mode = texture_mode(m)
    if sec == "A" and mode == "duo" and bar < 4:
        return [r(4)]
    if sec == "A":
        lines = [
            [n("C5", 1), r(1), n("E5", 1), n("G4", 1)],
            [r(1), n("E5", 1.5), n("C5", 1.5)],
            [n("E5", 1), n("G4", 2), r(1)],
            [r(1), n("C5", 2), n("E5", 1)],
            [n("G4", 1), n("E5", 1), n("C5", 2)],
        ]
        return lines[(bar + m) % 5]
    if sec == "B":
        if mode == "trio" and bar in (0, 1):
            return [r(4)]
        lines = [
            [n("E5", 1), n("G5", 1), n("E5", 1), r(1)],
            [n("C5", 1), n("E5", 2), n("D5", 1)],
            [n("E5", 1.5), n("C5", 1), n("G4", 1.5)],
            [n("C5", 2), n("E5", 1), r(1)],
            [n("E5", 1), n("F5", 1), n("E5", 1), n("C5", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "C":
        lines = [
            [n("E5", 1), n("F5", 1), n("E5", 1), n("C5", 1)],
            [n("G5", 1), n("E5", 1), n("D5", 2)],
            [n("E5", 1), n("C5", 1), n("A4", 2)],
            [n("F5", 1), n("E5", 1), n("C5", 2)],
            [n("C5", 1), n("E5", 1), n("G5", 1), n("E5", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "D":
        if bar < 15:
            return [n("E5", 2), r(1), n("C5", 1)]
        return [n("E5", 3), r(1)]
    if sec == "E":
        if bar < 11:
            return [n("G4", 2), r(2)]
        return [r(4)]
    return [r(4)]

def viola_content(sec, bar, m):
    mode = texture_mode(m)
    if sec == "A" and mode == "duo" and bar < 4:
        return [n("E4", 2), n("G4", 1), r(1)]
    if sec == "A":
        lines = [
            [n("E4", 2), n("G4", 1), r(1)],
            [n("C4", 1), n("E4", 2), n("G4", 1)],
            [n("G4", 1), r(1), n("C4", 2)],
            [n("E4", 1.5), n("C#4", 1.5), r(1)],
            [n("G4", 1), n("E4", 1), n("C4", 2)],
        ]
        return lines[(bar + m) % 5]
    if sec == "B":
        if mode == "trio" and bar in (0, 1):
            return [n("G4", 1), n("Bb4", 1), n("G4", 1), r(1)]
        lines = [
            [n("G4", 1), n("Bb4", 1), n("G4", 1), r(1)],
            [n("E4", 1), n("G4", 2), n("F4", 1)],
            [n("G4", 1.5), n("Eb4", 1), n("C4", 1.5)],
            [n("E4", 2), n("G4", 1), r(1)],
            [n("G4", 1), n("A4", 1), n("G4", 1), n("E4", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "C":
        lines = [
            [n("G4", 1), n("A4", 1), n("G4", 1), n("E4", 1)],
            [n("Bb4", 1), n("G4", 1), n("F4", 2)],
            [n("G4", 1), n("E4", 1), n("C#4", 2)],
            [n("A4", 1), n("G4", 1), n("E4", 2)],
            [n("E4", 1), n("G4", 1), n("Bb4", 1), n("G4", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "D":
        if mode == "trio" and bar < 4:
            return [r(4)]
        if bar < 15:
            return [n("G4", 2), r(1), n("E4", 1)]
        return [n("E4", 3), r(1)]
    if sec == "E":
        if bar < 11:
            return [n("C4", 2), r(2)]
        return [r(4)]
    return [r(4)]

def cello_content(sec, bar, m):
    mode = texture_mode(m)
    if sec == "A" and mode == "duo" and bar < 4:
        return [r(4)]
    if sec == "A":
        lines = [
            [n("E2", 2), n("A2", 1), n("E2", 1)],
            [n("G2", 2), n("C3", 1), r(1)],
            [n("E2", 2), n("G2", 2)],
            [n("A2", 2), n("E2", 1), r(1)],
            [n("E2", 1), n("G2", 1), n("C3", 1), n("E2", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "B":
        lines = [
            [n("E2", 2), n("Bb2", 1), n("E2", 1)],
            [n("G2", 2), n("Eb2", 1), n("G2", 1)],
            [n("E2", 2), n("C#2", 2)],
            [n("A2", 2), n("E2", 2)],
            [n("E2", 1), n("G2", 1), n("Bb2", 1), n("E2", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "C":
        lines = [
            [n("E2", 1), n("A2", 1), n("E2", 1), n("G2", 1)],
            [n("G2", 1), n("Bb2", 1), n("G2", 2)],
            [n("E2", 1), n("C#2", 1), n("E2", 2)],
            [n("A2", 1), n("E2", 1), n("G2", 2)],
            [n("E2", 1), n("G2", 1), n("A2", 1), n("E2", 1)],
        ]
        return lines[(bar + m) % 5]
    if sec == "D":
        if bar < 15:
            return [n("E2", 2), n("A2", 1), r(1)]
        return [n("E2", 4)]
    if sec == "E":
        if bar < 11:
            return [n("E2", 2), r(2)]
        return [n("E2", 4)]
    return [r(4)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Labyrinth of Quiet Motions"
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

    section_starts = [1, 19, 41, 71, 89]
    section_labels = ["A", "B", "C", "D", "E"]
    dyn_map = {1: "pp", 19: "p", 41: "mp", 55: "mf", 71: "mp", 89: "pp"}

    for m in range(1, 101):
        sec = section(m)
        bar = bar_in(m, sec)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mm = tempo.MetronomeMark(number=78, referent=note.Note(type='quarter'))
            mm.text = "Lento, polyphonic"
            mg.insert(0, mm)

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in dyn_map:
            mg.insert(0, dynamics.Dynamic(dyn_map[m]))

        for e in guitar_content(sec, bar, m):
            mg.append(e)

        if m in (18, 40, 70, 88):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for pname, content_fn in [
            ("vla", lambda s=sec, b=bar, me=m: viola_content(s, b, me)),
            ("vn1", lambda s=sec, b=bar, me=m: violin1_content(s, b, me)),
            ("vn2", lambda s=sec, b=bar, me=m: violin2_content(s, b, me)),
            ("vc", lambda s=sec, b=bar, me=m: cello_content(s, b, me)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature("4/4")
            if m == 1:
                mx.insert(0, key.KeySignature(0))
            for e in content_fn():
                mx.append(e)
            parts[pname].append(mx)

    for p in parts.values():
        s.append(p)
    return s

def main():
    score = build_score()
    base = os.path.dirname(__file__)
    out = os.path.join(base, "..", "musicxml", "V1_Labyrinth_of_Quiet_Motions.musicxml")
    out = os.path.abspath(out)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
