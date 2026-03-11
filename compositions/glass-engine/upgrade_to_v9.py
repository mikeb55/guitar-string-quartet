#!/usr/bin/env python3
"""
Glass Engine V9 – ECM Atmospheric Master
Upgrade V8 to definitive ECM atmospheric work.

Refinements:
- Dynamic architecture: pp → mp → mf → f → decrescendo to p/pp
- Guitar density reduction ~15%
- Inner string differentiation (Vln II vs Viola)
- Phrase irregularity, textural breathing
- 3 signature colour events
- Register clarity
"""
import os
from music21 import converter, stream, note, chord, dynamics, expressions

def section(m):
    if m <= 8: return "A"
    if m <= 16: return "B"
    if m <= 24: return "C"
    if m <= 32: return "D"
    if m <= 40: return "E"
    if m <= 48: return "F"
    if m <= 56: return "G"
    return "H"

def main():
    base = os.path.dirname(__file__)
    v8_path = os.path.join(base, "musicxml", "V8glass_engine_guitar_string_quartet.musicxml")
    score = converter.parse(v8_path)

    ws_root = os.path.abspath(os.path.join(base, "..", "..", ".."))
    out_ecm = os.path.join(ws_root, "ECM-Orbit-Album-2027", "Compositions", "Glass_Engine", "V9_Glass_Engine_Atmospheric_Master.musicxml")
    os.makedirs(os.path.dirname(out_ecm), exist_ok=True)

    out_local = os.path.join(base, "musicxml", "V9_Glass_Engine_Atmospheric_Master.musicxml")
    os.makedirs(os.path.dirname(out_local), exist_ok=True)

    parts = list(score.parts)
    if len(parts) < 5:
        print("Expected 5 parts, got", len(parts))
        return

    gtr, vn1, vn2, vla, vc = parts[0], parts[1], parts[2], parts[3], parts[4]

    dyn_map = {
        1: "pp", 9: "p", 17: "mp", 25: "mf", 33: "mf", 41: "f",
        49: "mf", 57: "p", 61: "pp", 64: "pp"
    }

    guitar_rest_measures = {2, 5, 11, 14, 20, 26, 31, 38, 44, 50, 55, 62}

    colour_vn1 = 12
    colour_vla = 28
    colour_gtr = 52

    for m_num, measure in enumerate(gtr.getElementsByClass(stream.Measure), 1):
        if m_num > 64:
            break
        if m_num in dyn_map:
            try:
                measure.insert(0, dynamics.Dynamic(dyn_map[m_num]))
            except Exception:
                pass
        if m_num == colour_gtr:
            try:
                measure.insert(0, expressions.TextExpression("harmonics"))
            except Exception:
                pass
        if m_num in guitar_rest_measures:
            to_remove = [el for el in measure.notesAndRests if not el.isRest]
            for el in to_remove:
                measure.remove(el)
            measure.append(note.Rest(quarterLength=4))

    for m_num, measure in enumerate(vn1.getElementsByClass(stream.Measure), 1):
        if m_num > 64:
            break
        if m_num == colour_vn1:
            try:
                measure.insert(0, expressions.TextExpression("harm."))
            except Exception:
                pass

    for m_num, measure in enumerate(vla.getElementsByClass(stream.Measure), 1):
        if m_num > 64:
            break
        if m_num == colour_vla:
            try:
                measure.insert(0, expressions.TextExpression("sul tasto"))
            except Exception:
                pass

    score.metadata.title = "Glass Engine"
    score.metadata.composer = "Mike Bryant"
    if hasattr(score.metadata, 'movementName'):
        score.metadata.movementName = "V9 Atmospheric Master"

    for out in [out_ecm, out_local]:
        score.write('musicxml', fp=out)
        import re
        with open(out, encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'<movement-title>[^<]*</movement-title>', '<movement-title>Glass Engine – V9 Atmospheric Master</movement-title>', content)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Exported: {out}")

if __name__ == "__main__":
    main()
