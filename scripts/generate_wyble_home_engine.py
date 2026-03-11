#!/usr/bin/env python3
"""
Generate Wyble arrangement for Home Engine only.
Two-line contrapuntal guitar; strings as sustained support.
"""
import os
from pathlib import Path

from music21 import (
    stream, note, chord, duration, tempo, key, metadata, meter,
    harmony, expressions, dynamics
)
from music21.chord import Chord
from music21.instrument import Guitar, Violin, Viola, Violoncello

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "compositions" / "home-engine" / "wyble-arrangement" / "musicxml"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def n(pitch, dur=1.0, voice=1):
    x = note.Note(pitch)
    x.duration = duration.Duration(dur)
    x.activeSite = None
    if voice:
        x.activeSite = None  # voice set when appending
    return x


def r(dur=1.0):
    x = note.Rest()
    x.duration = duration.Duration(dur)
    return x


def wyble_guitar_a(bar):
    """Two-line Wyble: upper (3rd/7th) and lower (root/5th). Contrary motion.
    Returns list of (duration, content) where content is chord, note, or rest."""
    patterns = [
        [("Dm9", 0.5, "F4", "D3"), ("Dm9", 0.5, "C4", "A3"), ("Dm9", 1.0, None, None), ("Dm9", 0.5, "E4", "D3"), ("Dm9", 1.5, None, None)],
        [("Dm9", 0.5, "A4", "A3"), ("Dm9", 1.0, "F4", "D3"), ("Dm9", 0.5, None, "A3"), ("Dm9", 2.0, None, None)],
        [("Dm9", 1.0, "C4", "D3"), ("Dm9", 0.5, "E4", None), ("Dm9", 1.0, None, "A3"), ("Dm9", 1.5, None, None)],
        [("Dm9", 0.5, "F4", "D3"), ("Dm9", 1.5, "C4", "A3"), ("Dm9", 2.0, None, None)],
    ]
    return patterns[bar % 4]


def build():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Home Engine (Wyble Arrangement)"
    s.metadata.composer = "Mike Bryant"

    gtr = stream.Part()
    gtr.insert(0, Guitar())
    gtr.partName = "Guitar"

    vln1 = stream.Part()
    vln1.insert(0, Violin())
    vln1.partName = "Violin I"

    vln2 = stream.Part()
    vln2.insert(0, Violin())
    vln2.partName = "Violin II"

    vla = stream.Part()
    vla.insert(0, Viola())
    vla.partName = "Viola"

    vc = stream.Part()
    vc.insert(0, Violoncello())
    vc.partName = "Cello"

    for m_num in range(1, 17):
        mg = stream.Measure(number=m_num)
        mg.timeSignature = meter.TimeSignature("4/4")
        if m_num == 1:
            mg.insert(0, key.KeySignature(-1))
            mg.insert(0, tempo.MetronomeMark(number=104, referent=note.Note(type='quarter')))
            mg.insert(0, dynamics.Dynamic("mp"))
            mg.insert(0, expressions.RehearsalMark("A"))
        if m_num == 9:
            mg.insert(0, expressions.RehearsalMark("B"))

        mg.insert(0, harmony.ChordSymbol("Dm9"))
        for sym, dur, up, lo in wyble_guitar_a(m_num - 1):
            if up and lo:
                c = chord.Chord([up, lo])
                c.duration = duration.Duration(dur)
                mg.append(c)
            elif up:
                mg.append(n(up, dur))
            elif lo:
                mg.append(n(lo, dur))
            else:
                mg.append(r(dur))

        gtr.append(mg)

        # Strings: sparse
        mv = stream.Measure(number=m_num)
        mv.timeSignature = meter.TimeSignature("4/4")
        if m_num % 4 == 1:
            mv.append(n("D4", 4))
        else:
            mv.append(r(4))
        vln1.append(mv)

        mv2 = stream.Measure(number=m_num)
        mv2.timeSignature = meter.TimeSignature("4/4")
        mv2.append(r(4))
        vln2.append(mv2)

        mva = stream.Measure(number=m_num)
        mva.timeSignature = meter.TimeSignature("4/4")
        mva.append(r(4))
        vla.append(mva)

        mvc = stream.Measure(number=m_num)
        mvc.timeSignature = meter.TimeSignature("4/4")
        mvc.append(n("D2", 2))
        mvc.append(r(2))
        vc.append(mvc)

    s.append(gtr)
    s.append(vln1)
    s.append(vln2)
    s.append(vla)
    s.append(vc)

    out = OUT_DIR / "Wyble_V9_Home_Engine_Scofield.musicxml"
    s.write("musicxml", fp=out)
    print(f"Generated: {out}")
    return out


if __name__ == "__main__":
    build()
