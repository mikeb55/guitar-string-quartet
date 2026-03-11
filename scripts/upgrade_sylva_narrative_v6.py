#!/usr/bin/env python3
"""
Upgrade Sylva Narrative No.2 V5 to V6 with score readability standard.
Sections: A(1-15), B(16-30), C(31-45), D(46-60), E(61-75), F(76-88)
"""
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent.parent
    src = base / "compositions/sylva-narrative-no2/musicxml/V5Sylva_Narrative_No2.musicxml"
    dst = base / "compositions/sylva-narrative-no2/musicxml/V6Sylva_Narrative_No2.musicxml"

    content = src.read_text(encoding="utf-8")

    # 1. Add rehearsal A + harmony Dmaj7 at measure 1 (after metronome, before first note)
    old_m1 = """      <direction>
        <direction-type>
          <metronome parentheses="no">
            <beat-unit>quarter</beat-unit>
            <per-minute>72</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="72" />
      </direction>
      <note>
        <pitch>
          <step>D</step>
          <octave>3</octave>
        </pitch>"""
    new_m1 = """      <direction>
        <direction-type>
          <metronome parentheses="no">
            <beat-unit>quarter</beat-unit>
            <per-minute>72</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="72" />
      </direction>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">A</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><p/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>D</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
      <note>
        <pitch>
          <step>D</step>
          <octave>3</octave>
        </pitch>"""
    content = content.replace(old_m1, new_m1, 1)

    # 2. Add barline + rehearsal B + harmony + dynamics at measure 16 (guitar part - first part)
    insert_b = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">B</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><mp/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>G</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m16 = '''    <!--========================= Measure 16 =========================-->
    <measure number="16">
      <note>'''
    new_m16 = '''    <!--========================= Measure 16 =========================-->
    <measure number="16">
''' + insert_b + '''      <note>'''
    content = content.replace(old_m16, new_m16, 1)

    # 3. Add barline + rehearsal C at measure 31
    insert_c = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">C</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><mf/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>A</root-step></root>
        <kind>minor-seventh</kind>
      </harmony>
'''
    old_m31 = '''    <!--========================= Measure 31 =========================-->
    <measure number="31">
      <note>'''
    new_m31 = '''    <!--========================= Measure 31 =========================-->
    <measure number="31">
''' + insert_c + '''      <note>'''
    content = content.replace(old_m31, new_m31, 1)

    # 4. Add barline + rehearsal D at measure 46
    insert_d = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">D</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><mp/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>D</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m46 = '''    <!--========================= Measure 46 =========================-->
    <measure number="46">
      <note>'''
    new_m46 = '''    <!--========================= Measure 46 =========================-->
    <measure number="46">
''' + insert_d + '''      <note>'''
    content = content.replace(old_m46, new_m46, 1)

    # 5. Add barline + rehearsal E at measure 61
    insert_e = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">E</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><p/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>G</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m61 = '''    <!--========================= Measure 61 =========================-->
    <measure number="61">
      <note>'''
    new_m61 = '''    <!--========================= Measure 61 =========================-->
    <measure number="61">
''' + insert_e + '''      <note>'''
    content = content.replace(old_m61, new_m61, 1)

    # 6. Add barline + rehearsal F at measure 76
    insert_f = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction>
        <direction-type>
          <rehearsal enclosure="rectangle">F</rehearsal>
        </direction-type>
      </direction>
      <direction>
        <direction-type>
          <dynamics><pp/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>D</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m76 = '''    <!--========================= Measure 76 =========================-->
    <measure number="76">
      <note>'''
    new_m76 = '''    <!--========================= Measure 76 =========================-->
    <measure number="76">
''' + insert_f + '''      <note>'''
    content = content.replace(old_m76, new_m76, 1)

    # 7. Update movement title
    content = content.replace(
        "<movement-title>Sylva Narrative No.2</movement-title>",
        "<movement-title>V6Sylva_Narrative_No2</movement-title>"
    )

    dst.write_text(content, encoding="utf-8")
    print(f"Wrote {dst}")

if __name__ == "__main__":
    main()
