#!/usr/bin/env python3
"""
Replace introduction (bars 1-4) of Sylva Narrative V6 with strings-only narrative opening.
Option 1: Guitar removed for first 4 bars, chamber narrative texture, guitar enters bar 5.
"""
from pathlib import Path
from music21 import converter, stream, note, chord, duration, dynamics

DIV = 10080  # divisions per quarter
Q = 10080
H = 20160
DQ = 15120
E = 5040
MEASURE = 50400  # 5/4


def n(pitch_name, dur_divisions, octave=4):
    n_ = note.Note(pitch_name + str(octave))
    n_.duration = duration.Duration()
    n_.duration.quarterLength = dur_divisions / DIV
    return n_


def r(dur_divisions):
    rest_ = note.Rest()
    rest_.duration = duration.Duration()
    rest_.duration.quarterLength = dur_divisions / DIV
    return rest_


def c(pitches_with_oct, dur_divisions):
    ch = chord.Chord(pitches_with_oct)
    ch.duration = duration.Duration()
    ch.duration.quarterLength = dur_divisions / DIV
    return ch


def main():
    base = Path(__file__).resolve().parent.parent.parent
    src = base / "compositions/sylva-narrative-no2/musicxml/V6Sylva_Narrative_No2.musicxml"
    dst = base / "compositions/sylva-narrative/musicxml/V7_Sylva_Narrative_New_Intro.musicxml"
    dst.parent.mkdir(parents=True, exist_ok=True)

    score = converter.parse(str(src))

    # Part order: Guitar, Violin I, Violin II, Viola, Cello
    parts = list(score.parts)

    # --- Guitar: measures 1-4 = full rests (preserve m1 attributes/directions) ---
    gtr = parts[0]
    for m_num in [1, 2, 3, 4]:
        m = gtr.measure(m_num)
        to_remove = [e for e in m.elements if isinstance(e, (note.Note, note.Rest, chord.Chord))]
        for e in to_remove:
            m.remove(e)
        rest_ = note.Rest()
        rest_.duration = duration.Duration()
        rest_.duration.quarterLength = 5.0  # whole measure 5/4
        m.append(rest_)

    # --- Violin I: new intro ---
    # Bar 1: very light sustained tone (pp)
    # Bar 2: short melodic fragment - F#5-A5 (theme head)
    # Bar 3: (harmonic bloom - part of)
    # Bar 4: completes melodic fragment, resolves
    vln1 = parts[1]
    for m_num in [1, 2, 3, 4]:
        m = vln1.measure(m_num)
        to_remove = [e for e in m.elements if isinstance(e, (note.Note, note.Rest, chord.Chord, dynamics.Dynamic))]
        for e in to_remove:
            m.remove(e)
    vln1.measure(1).append(dynamics.Dynamic("pp"))
    vln1.measure(1).append(n("F#", H, 5))  # F#5 half
    vln1.measure(1).append(r(Q))
    vln1.measure(1).append(n("A", DQ, 5))
    vln1.measure(1).append(r(E))

    vln1.measure(2).append(n("F#", DQ, 5))  # melodic fragment start
    vln1.measure(2).append(r(Q))
    vln1.measure(2).append(n("E", DQ, 5))
    vln1.measure(2).append(r(E))

    vln1.measure(3).append(dynamics.Dynamic("mp"))
    vln1.measure(3).append(n("A", H, 5))
    vln1.measure(3).append(r(Q))
    vln1.measure(3).append(n("G", DQ, 5))
    vln1.measure(3).append(r(E))

    vln1.measure(4).append(n("F#", H, 5))  # completes fragment
    vln1.measure(4).append(r(Q))
    vln1.measure(4).append(n("A", DQ, 5))
    vln1.measure(4).append(r(E))

    # --- Violin II: answers quietly ---
    vln2 = parts[2]
    for m_num in [1, 2, 3, 4]:
        m = vln2.measure(m_num)
        to_remove = [e for e in m.elements if isinstance(e, (note.Note, note.Rest, chord.Chord, dynamics.Dynamic))]
        for e in to_remove:
            m.remove(e)
    vln2.measure(1).append(dynamics.Dynamic("pp"))
    vln2.measure(1).append(n("D", H, 5))
    vln2.measure(1).append(r(Q))
    vln2.measure(1).append(n("F#", DQ, 5))
    vln2.measure(1).append(r(E))

    vln2.measure(2).append(n("D", DQ, 5))  # answer
    vln2.measure(2).append(r(Q))
    vln2.measure(2).append(n("C#", DQ, 5))
    vln2.measure(2).append(r(E))

    vln2.measure(3).append(n("E", H, 5))
    vln2.measure(3).append(r(Q))
    vln2.measure(3).append(n("D", DQ, 5))
    vln2.measure(3).append(r(E))

    vln2.measure(4).append(n("D", H, 5))
    vln2.measure(4).append(r(Q))
    vln2.measure(4).append(n("F#", DQ, 5))
    vln2.measure(4).append(r(E))

    # --- Viola: sustained harmonic colour (pp), slow inner motion ---
    vla = parts[3]
    for m_num in [1, 2, 3, 4]:
        m = vla.measure(m_num)
        to_remove = [e for e in m.elements if isinstance(e, (note.Note, note.Rest, chord.Chord, dynamics.Dynamic))]
        for e in to_remove:
            m.remove(e)
    vla.measure(1).append(dynamics.Dynamic("pp"))
    vla.measure(1).append(c(["B3", "D4", "F#4"], H))
    vla.measure(1).append(r(Q))
    vla.measure(1).append(c(["B3", "D4"], DQ))
    vla.measure(1).append(r(E))

    vla.measure(2).append(c(["A3", "C#4"], Q))
    vla.measure(2).append(c(["G3", "B3"], H))
    vla.measure(2).append(c(["E4"], DQ))
    vla.measure(2).append(r(E))

    vla.measure(3).append(c(["D4", "F#4"], H))
    vla.measure(3).append(r(Q))
    vla.measure(3).append(c(["C#4", "E4"], DQ))
    vla.measure(3).append(r(E))

    vla.measure(4).append(c(["B3", "D4", "F#4"], H))
    vla.measure(4).append(r(Q))
    vla.measure(4).append(c(["B3", "D4"], DQ))
    vla.measure(4).append(r(E))

    # --- Cello: slow stepwise bass motion ---
    vc = parts[4]
    for m_num in [1, 2, 3, 4]:
        m = vc.measure(m_num)
        to_remove = [e for e in m.elements if isinstance(e, (note.Note, note.Rest, chord.Chord, dynamics.Dynamic))]
        for e in to_remove:
            m.remove(e)
    vc.measure(1).append(dynamics.Dynamic("pp"))
    vc.measure(1).append(n("D", H, 2))
    vc.measure(1).append(r(Q))
    vc.measure(1).append(n("E", DQ, 2))
    vc.measure(1).append(r(E))

    vc.measure(2).append(n("E", H, 2))
    vc.measure(2).append(r(Q))
    vc.measure(2).append(n("F#", DQ, 2))
    vc.measure(2).append(r(E))

    vc.measure(3).append(n("F#", H, 2))
    vc.measure(3).append(r(Q))
    vc.measure(3).append(n("G", DQ, 2))
    vc.measure(3).append(r(E))

    vc.measure(4).append(n("D", H, 2))
    vc.measure(4).append(r(Q))
    vc.measure(4).append(n("D", DQ, 2))
    vc.measure(4).append(r(E))

    # Update movement title
    score.metadata.movementName = "V7_Sylva_Narrative_New_Intro"

    score.write("musicxml", fp=str(dst))
    print(f"Written: {dst}")


if __name__ == "__main__":
    main()
