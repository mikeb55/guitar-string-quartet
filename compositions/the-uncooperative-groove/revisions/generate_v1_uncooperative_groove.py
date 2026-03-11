#!/usr/bin/env python3
"""
The Uncooperative Groove V1 – Scofield-Zappa Rhythmic Hybrid
Orbit Album – Guitar + String Quartet

Rhythm-driven chamber piece. Groove forms, breaks, reforms.
Meters: 7/8 (3+2+2), 5/8 (2+3), 4/4.
Sections: A(1-8) Groove Emergence, B(9-16) Disruption, C(17-28) False Stability,
D(29-44) Metric Arguments, E(45-56) Peak Energy, F(57-60) Dry Ending.
~60 bars, 4-5 min.
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

def section(m):
    if m <= 8: return "A"
    if m <= 16: return "B"
    if m <= 28: return "C"
    if m <= 44: return "D"
    if m <= 56: return "E"
    return "F"

def bar_in(m, sec):
    if sec == "A": return m - 1
    if sec == "B": return m - 9
    if sec == "C": return m - 17
    if sec == "D": return m - 29
    if sec == "E": return m - 45
    return m - 57

def time_sig(m):
    sec = section(m)
    if sec == "A": return "7/8"
    if sec == "B": return "5/8"
    if sec == "C": return "4/4"
    if sec == "D":
        bar = bar_in(m, sec)
        return "7/8" if bar % 2 == 0 else "5/8"
    if sec == "E":
        bar = bar_in(m, sec)
        cycle = [0, 1, 2, 3]
        return ["7/8", "5/8", "7/8", "4/4"][bar % 4]
    return "4/4"

def bar_dur(m):
    ts = time_sig(m)
    if ts == "7/8": return 3.5
    if ts == "5/8": return 2.5
    return 4.0

def chord_for(sec, bar):
    opts_a = ["E7sus4", "A7", "D7", "E7sus4"]
    opts_c = ["G7", "C7", "F7", "G7"]
    opts_d = ["E7", "A7alt", "D7", "E7"]
    if sec == "A": return opts_a[bar % 4]
    if sec == "B": return None
    if sec == "C": return opts_c[bar % 4]
    if sec == "D": return opts_d[bar % 4]
    if sec == "E": return "E7" if bar % 2 == 0 else "A7alt"
    return None

def guitar_content(sec, bar, m):
    bd = bar_dur(m)
    if sec == "A":
        if bar in (0, 2, 5): return [r(bd)]
        return [c(("E3", "B3"), 1.5), r(0.5), c(("A3", "E4"), 1), r(0.5)]
    if sec == "B":
        if bar in (1, 3, 5, 7): return [r(bd)]
        return [c(("Bb3", "F4"), 0.5), r(0.5), c(("C#4", "G#4"), 0.5), r(1)]
    if sec == "C":
        if bar in (0, 4, 8): return [r(bd)]
        return [c(("G3", "B3"), 1), r(0.5), c(("C4", "E4"), 1), r(0.5), c(("F3", "A3"), 1)]
    if sec == "D":
        if bar % 2 == 1: return [c(("E3", "B3"), 1), r(bar_dur(m) - 1)]
        return [c(("A3", "E4"), 1.5), r(0.5), c(("D3", "A3"), 1), r(bar_dur(m) - 2.5)]
    if sec == "E":
        if bar in (0, 2, 5, 7): return [r(bd)]
        return [c(("E3", "Bb3"), 0.5), c(("C#4", "G4"), 0.5), r(0.5), c(("E3", "B3"), 1)]
    if sec == "F":
        if bar == 0: return [c(("E3", "B3"), 2), r(2)]
        return [r(bd)]
    return [r(bd)]

def violin1_content(sec, bar, m):
    bd = bar_dur(m)
    if sec == "A":
        if bar in (1, 4, 7): return [r(1), n("G5", 1), n("E5", 1), r(bd - 3)]
        return [r(bd)]
    if sec == "B":
        if bar in (0, 2, 4, 6): return [n("Bb5", 0.5), r(1), n("F#5", 0.5), r(bd - 2)]
        return [r(bd)]
    if sec == "C":
        if bar in (2, 6, 10): return [r(1), n("G5", 1), r(bd - 2)]
        return [r(bd)]
    if sec == "D":
        if bar in (2, 6, 10):
            if bd > 2.5: return [n("E5", 1), r(0.5), n("G5", 1), r(bd - 2.5)]
            return [n("E5", 1), n("G5", 1), r(bd - 2)]
        return [r(bd)]
    if sec == "E":
        if bar in (1, 4, 8): return [n("G5", 1), n("Bb5", 0.5), r(bd - 1.5)]
        return [r(bd)]
    if sec == "F":
        if bar == 2: return [n("B5", 2)]
        return [r(bd)]
    return [r(bd)]

def violin2_content(sec, bar, m):
    bd = bar_dur(m)
    if sec == "A":
        if bar in (2, 6): return [r(1.5), n("C5", 1), r(bd - 2.5)]
        return [r(bd)]
    if sec == "B":
        if bar in (1, 5): return [r(0.5), n("G4", 1), n("Db4", 0.5), r(bd - 2)]
        return [r(bd)]
    if sec == "C":
        if bar in (3, 7, 11): return [r(1), n("E5", 1), r(bd - 2)]
        return [r(bd)]
    if sec == "D":
        if bar in (4, 8): return [n("G4", 3), r(bd - 3)] if bar_dur(m) >= 3 else [n("G4", 1), r(bd - 1)]
        return [r(bd)]
    if sec == "E":
        if bar in (3, 6): return [r(1), n("G4", 1), r(bd - 2)]
        return [r(bd)]
    return [r(bd)]

def viola_content(sec, bar, m):
    bd = bar_dur(m)
    if sec == "A":
        if bar in (3, 6): return [n("C#4", 1), n("E4", 1), r(bd - 2)]
        return [r(bd)]
    if sec == "B":
        if bar in (2, 6): return [n("Bb3", 0.5), n("D4", 0.5), r(bd - 1)]
        return [r(bd)]
    if sec == "C":
        if bar in (1, 5, 9): return [r(1), n("C4", 1), n("E4", 1), r(bd - 3)]
        return [r(bd)]
    if sec == "D":
        if bar in (3, 7, 11):
            if bd >= 3: return [n("E4", 1), n("G4", 2), r(bd - 3)]
            return [n("E4", 1), n("G4", 1), r(bd - 2)]
        return [r(bd)]
    if sec == "E":
        if bar in (2, 5, 9): return [n("C#4", 2), r(bd - 2)]
        return [r(bd)]
    return [r(bd)]

def cello_content(sec, bar, m):
    bd = bar_dur(m)
    if sec == "A":
        pat = [n("E2", 1.5), n("A2", 1), n("E2", 1)]
        return pat if bd >= 3.5 else [n("E2", 1.5), n("A2", 1), r(bd - 2.5)]
    if sec == "B":
        if bar in (0, 2, 4, 6): return [n("Bb2", 0.5), r(1), n("E2", 0.5), r(bd - 2)]
        return [r(bd)]
    if sec == "C":
        if bar in (1, 3, 5, 7): return [n("G2", 2), n("C3", 2)]
        return [n("G2", 2), r(2)]
    if sec == "D":
        if bar % 2 == 0: return [n("E2", 1.5), n("A2", 1), r(bd - 2.5)]
        return [n("A2", 1), n("E2", 1), r(bd - 2)]
    if sec == "E":
        if bd >= 3: return [n("E2", 1), n("Bb2", 1), n("E2", 1), r(bd - 3)]
        return [n("E2", 1), n("Bb2", 1), r(bd - 2)]
    if sec == "F":
        if bar == 1: return [n("E2", 1)]
        return [r(bd)]
    return [r(bd)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "The Uncooperative Groove"
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

    section_starts = [1, 9, 17, 29, 45, 57]
    section_labels = ["A", "B", "C", "D", "E", "F"]
    dyn_map = {1: "mp", 9: "mf", 17: "mp", 29: "mf", 45: "f", 57: "p"}

    last_chord = None
    for m in range(1, 61):
        sec = section(m)
        bar = bar_in(m, sec)
        ts = time_sig(m)

        mg = stream.Measure(number=m)
        mg.timeSignature = meter.TimeSignature(ts)
        if m == 1:
            mg.insert(0, key.KeySignature(0))
            mm = tempo.MetronomeMark(number=104, referent=note.Note(type='quarter'))
            mm.text = "Groove Emergence (7/8 = 3+2+2)"
            mg.insert(0, mm)

        if m in section_starts:
            idx = section_starts.index(m)
            mg.insert(0, expressions.RehearsalMark(section_labels[idx]))
        if m in dyn_map:
            mg.insert(0, dynamics.Dynamic(dyn_map[m]))

        chord_sym = chord_for(sec, bar)
        if chord_sym and chord_sym != last_chord:
            try:
                mg.insert(0, harmony.ChordSymbol(chord_sym))
            except Exception:
                pass
            last_chord = chord_sym

        for e in guitar_content(sec, bar, m):
            mg.append(e)

        if m in (8, 16, 28, 44, 56):
            mg.rightBarline = Barline('double')

        parts["gtr"].append(mg)

        for pname, content_fn in [
            ("vla", lambda: viola_content(sec, bar, m)),
            ("vn1", lambda: violin1_content(sec, bar, m)),
            ("vn2", lambda: violin2_content(sec, bar, m)),
            ("vc", lambda: cello_content(sec, bar, m)),
        ]:
            mx = stream.Measure(number=m)
            mx.timeSignature = meter.TimeSignature(ts)
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
    out = os.path.join(base, "..", "musicxml", "V1_The_Uncooperative_Groove.musicxml")
    out = os.path.abspath(out)
    score.write('musicxml', fp=out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
