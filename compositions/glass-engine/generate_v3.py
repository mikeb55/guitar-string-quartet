#!/usr/bin/env python3
"""
Glass Engine V3 - Rewrite with:
- Anti-repetition (repetition-fatigue-rule)
- Rich guitar writing (dyads, triads, quartal, chordal)
- Evolving sections, ensemble hits, silence
- ~5 min, A-B-C-D-A'-Coda structure
"""
import os
from music21 import stream, note, chord, duration, tempo, key, metadata, meter
from music21.instrument import Guitar, Violin, Viola, Violoncello

def make_note(pitch, dur_quarter=1.0):
    n = note.Note(pitch)
    n.duration = duration.Duration(dur_quarter)
    return n

def make_chord(pitches, dur_quarter=1.0):
    c = chord.Chord(pitches)
    c.duration = duration.Duration(dur_quarter)
    return c

def make_rest(dur_quarter=1.0):
    r = note.Rest()
    r.duration = duration.Duration(dur_quarter)
    return r

def add_measure(part, meas_num, notes_and_rests, div=4):
    """Add notes to part for one 5/4 measure. Total duration = 5 quarters."""
    m = stream.Measure(number=meas_num)
    m.timeSignature = (5, 4)
    if meas_num == 1:
        m.insert(0, key.KeySignature(0))
        m.insert(0, tempo.MetronomeMark(number=72, referent=note.Note(type='quarter')))
    for elem in notes_and_rests:
        m.append(elem)
    part.append(m)

# Harmonic progression - varied every 4 bars (no loop > 4 bars)
# Format: list of (pitches, duration) - pitches can be "C4" or ("C4","E4") for chord
def section_a_harmonies(bar_in_section):
    """A: Atmospheric opening - varied every 4 bars."""
    block = bar_in_section // 4
    bar = bar_in_section % 4
    blocks = [
        [("A3","E4","G4"), ("C5","G5"), ("A4","E5"), ("E4","B4")],  # 0-3
        [("E4","B4"), ("D4","G4","C5"), ("F#4","C#5"), ("G4","D5")],  # 4-7
        [("E4","G4","B4"), ("B4","F#5"), ("C4","E4","G4"), ("A3","E4","B4")],  # 8-11
        [("G4","D5"), ("A3","E4"), ("E4","B4"), ("C5","G5")],  # 12-15
    ]
    return blocks[block % len(blocks)][bar % 4]

def section_b_harmonies(bar_in_section):
    """B: Rhythmic engine - pizzicato feel."""
    block = bar_in_section // 4
    bar = bar_in_section % 4
    blocks = [
        [("C5","G5"), ("B4","D5"), ("G4","D5"), ("D4","G4","C5")],
        [("B4","F#5"), ("A4","E5"), ("F#4","C#5"), ("E4","B4")],
        [("G4","D5"), ("C4","E4","G4"), ("B4","F#5"), ("A4","E5")],
        [("C5","G5"), ("G4","D5"), ("E4","B4"), ("A3","E4")],
    ]
    return blocks[block % len(blocks)][bar % 4]

def section_c_harmonies(bar_in_section):
    """C: Guitar chordal counterpoint - triads, quartal."""
    block = bar_in_section // 4
    bar = bar_in_section % 4
    blocks = [
        [("G3","D4","B4"), ("A3","E4","B4"), ("E4","B4","G5"), ("D4","G4","C5")],
        [("F#4","C#5"), ("C4","E4","G4"), ("B3","F#4","D5"), ("A3","E4","B4")],
        [("G4","D5"), ("E4","G4","B4"), ("C5","G5"), ("A4","E5")],
        [("D4","G4","C5"), ("B4","F#5"), ("E4","B4"), ("G4","D5")],
    ]
    return blocks[block % len(blocks)][bar % 4]

def section_d_harmonies(bar_in_section):
    """D: Ensemble hits and harmonic bloom."""
    block = bar_in_section // 4
    bar = bar_in_section % 4
    blocks = [
        [("E4","B4","G5"), ("A3","E4"), ("C5","G5"), ("G4","D5")],
        [("B4","F#5"), ("D4","G4","C5"), ("F#4","C#5"), ("E4","B4")],
        [("A4","E5"), ("C4","E4","G4"), ("G4","D5"), ("B4","F#5")],
        [("C5","G5"), ("E4","B4"), ("A3","E4"), ("G4","D5")],
    ]
    return blocks[block % len(blocks)][bar % 4]

def section_a2_harmonies(bar_in_section):
    """A': Transformed return."""
    block = bar_in_section // 4
    bar = bar_in_section % 4
    blocks = [
        [("C5","G5"), ("A3","E4","B4"), ("E4","B4"), ("G4","D5")],
        [("D4","G4","C5"), ("F#4","C#5"), ("E4","G4","B4"), ("B4","F#5")],
        [("A4","E5"), ("A3","E4"), ("G4","D5"), ("C5","G5")],
        [("E4","B4"), ("A3","E4"), ("G4","D5"), ("C5","G5")],
    ]
    return blocks[block % len(blocks)][bar % 4]

def section_coda_harmonies(bar_in_section):
    """Coda: Dissolve."""
    if bar_in_section < 4:
        return [("C5","G5"), ("A4","E5"), ("G4","D5"), ("E4","B4")][bar_in_section % 4]
    elif bar_in_section < 8:
        return [("A3","E4"), ("E4","B4"), ("rest"), ("rest")][bar_in_section % 4]
    else:
        return "rest"

def get_guitar_content(meas_num, section, bar_in):
    """Guitar: 40-60% dyads, 20-30% triads, 10-20% single. Vary texture."""
    if section == "A": pit = section_a_harmonies(bar_in)
    elif section == "B": pit = section_b_harmonies(bar_in)
    elif section == "C": pit = section_c_harmonies(bar_in)
    elif section == "D": pit = section_d_harmonies(bar_in)
    elif section == "A2": pit = section_a2_harmonies(bar_in)
    else: pit = section_coda_harmonies(bar_in)
    
    if pit == "rest" or (isinstance(pit, tuple) and len(pit) == 1 and pit[0] == "rest"):
        return [make_rest(5)]
    
    if isinstance(pit, str):
        pit = (pit,)
    
    # Triad or dyad with space - Frisell style
    if len(pit) >= 3:
        return [make_chord(pit, 2), make_rest(0.5), make_chord((pit[0], pit[1]), 1.5), make_rest(1)]
    elif len(pit) == 2:
        return [make_chord(pit, 2), make_rest(1), make_chord(pit, 2)]
    else:
        return [make_note(pit[0], 2), make_rest(3)]

def build_score():
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "Glass Engine V3"
    s.metadata.composer = "Mike Bryant"
    
    guitar = stream.Part()
    guitar.id = "P1"
    guitar.partName = "Guitar"
    guitar.insert(0, Guitar())
    
    vn1 = stream.Part()
    vn1.id = "P2"
    vn1.partName = "Violin I"
    vn1.insert(0, Violin())
    
    vn2 = stream.Part()
    vn2.id = "P3"
    vn2.partName = "Violin II"
    vn2.insert(0, Violin())
    
    vla = stream.Part()
    vla.id = "P4"
    vla.partName = "Viola"
    vla.insert(0, Viola())
    
    vc = stream.Part()
    vc.id = "P5"
    vc.partName = "Cello"
    vc.insert(0, Violoncello())
    
    def section(m):
        if m <= 16: return "A"
        if m <= 32: return "B"
        if m <= 48: return "C"
        if m <= 64: return "D"
        if m <= 80: return "A2"
        return "Coda"
    
    def bar_in(m, sec):
        if sec == "A": return m - 1
        if sec == "B": return m - 17
        if sec == "C": return m - 33
        if sec == "D": return m - 49
        if sec == "A2": return m - 65
        return m - 81
    
    for m in range(1, 97):
        sec = section(m)
        bi = bar_in(m, sec)
        
        # Guitar
        g_content = get_guitar_content(m, sec, bi)
        m_g = stream.Measure(number=m)
        m_g.timeSignature = meter.TimeSignature("5/4")
        if m == 1:
            m_g.insert(0, key.KeySignature(0))
            m_g.insert(0, tempo.MetronomeMark(number=72, referent=note.Note(type='quarter')))
        for elem in g_content:
            m_g.append(elem)
        guitar.append(m_g)
        
        # Strings - simplified: sparse, responsive
        m_v1 = stream.Measure(number=m)
        m_v1.timeSignature = meter.TimeSignature("5/4")
        m_v2 = stream.Measure(number=m)
        m_v2.timeSignature = meter.TimeSignature("5/4")
        m_va = stream.Measure(number=m)
        m_va.timeSignature = meter.TimeSignature("5/4")
        m_vc = stream.Measure(number=m)
        m_vc.timeSignature = meter.TimeSignature("5/4")
        
        # Vary string activity by section
        if sec == "A" and m % 4 != 0:
            m_v1.append(make_rest(5))
            m_v2.append(make_note("E5", 1)); m_v2.append(make_rest(4))
            m_va.append(make_rest(5))
            m_vc.append(make_note("E2", 2)); m_vc.append(make_rest(3))
        elif sec == "B":
            m_v1.append(make_note("E5", 2)); m_v1.append(make_rest(3))
            m_v2.append(make_rest(5))
            m_va.append(make_note("B3", 1)); m_va.append(make_rest(4))
            m_vc.append(make_note("E2", 1)); m_vc.append(make_note("B2", 1)); m_vc.append(make_rest(3))
        elif sec == "C":
            m_v1.append(make_note("C6", 1)); m_v1.append(make_rest(4))
            m_v2.append(make_rest(2)); m_v2.append(make_note("G5", 1)); m_v2.append(make_rest(2))
            m_va.append(make_chord(("B3","D4"), 2)); m_va.append(make_rest(3))
            m_vc.append(make_note("G2", 2)); m_vc.append(make_rest(3))
        elif sec == "D":
            if m % 4 == 1:
                m_v1.append(make_chord(("E5","G5"), 0.5)); m_v1.append(make_rest(4.5))
                m_v2.append(make_chord(("C5","E5"), 0.5)); m_v2.append(make_rest(4.5))
                m_va.append(make_chord(("B3","E4"), 0.5)); m_va.append(make_rest(4.5))
                m_vc.append(make_chord(("E2","G2"), 0.5)); m_vc.append(make_rest(4.5))
            else:
                m_v1.append(make_rest(5))
                m_v2.append(make_rest(5))
                m_va.append(make_rest(5))
                m_vc.append(make_rest(5))
        elif sec == "A2":
            m_v1.append(make_note("G5", 3)); m_v1.append(make_rest(2))
            m_v2.append(make_rest(5))
            m_va.append(make_note("B3", 2)); m_va.append(make_rest(3))
            m_vc.append(make_note("E2", 2)); m_vc.append(make_rest(3))
        else:  # Coda
            m_v1.append(make_note("G5", 4)); m_v1.append(make_rest(1))
            m_v2.append(make_rest(5))
            m_va.append(make_rest(5))
            m_vc.append(make_note("E2", 2)); m_vc.append(make_rest(3))
        
        vn1.append(m_v1)
        vn2.append(m_v2)
        vla.append(m_va)
        vc.append(m_vc)
    
    s.append(guitar)
    s.append(vn1)
    s.append(vn2)
    s.append(vla)
    s.append(vc)
    
    return s

def main():
    score = build_score()
    out_dir = os.path.join(os.path.dirname(__file__), "musicxml")
    out_path = os.path.join(out_dir, "V3glass_engine_guitar_string_quartet.musicxml")
    score.write('musicxml', fp=out_path)
    print(f"Exported: {out_path}")

if __name__ == "__main__":
    main()
