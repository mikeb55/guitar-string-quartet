#!/usr/bin/env python3
"""
Upgrade Drift Study No.1 to V2 with score readability standard.
"""
import re
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent.parent
    src = base / "compositions/drift-study-no1/musicxml/drift_study_no1_guitar_string_quartet.musicxml"
    dst = base / "compositions/drift-study-no1/musicxml/V2drift_study_no1_guitar_string_quartet.musicxml"

    content = src.read_text(encoding="utf-8")

    # 1. Replace <words>A</words> with <rehearsal enclosure="rectangle">A</rehearsal>
    content = content.replace(
        """      <direction placement="above">
        <direction-type>
          <words>A</words>
        </direction-type>
      </direction>""",
        """      <direction placement="above">
        <direction-type>
          <rehearsal enclosure="rectangle">A</rehearsal>
        </direction-type>
      </direction>"""
    )

    # 2. Add barline + rehearsal B + harmony at measure 11 (guitar part - first occurrence)
    # Find first part (P1) and within it, measure 11
    barline_rehearsal_b = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction placement="above">
        <direction-type>
          <rehearsal enclosure="rectangle">B</rehearsal>
        </direction-type>
      </direction>
      <direction placement="below">
        <direction-type>
          <dynamics><mp/></dynamics>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>A</root-step></root>
        <kind>minor-seventh</kind>
      </harmony>
'''
    # Insert before first note of measure 11 in P1 - use unique context
    # Guitar measure 11: <measure number="11">\n      <note>\n        <rest/>
    old_m11_p1 = '''    <measure number="11">
      <note>
        <rest/>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>'''
    new_m11_p1 = '''    <measure number="11">
''' + barline_rehearsal_b + '''      <note>
        <rest/>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>'''
    content = content.replace(old_m11_p1, new_m11_p1, 1)

    # 3. Add harmony at measure 1 (after rehearsal A, before first note)
    harmony_cmaj7 = '''      <harmony>
        <root><root-step>C</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m1_notes = '''      </direction>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <octave>5</octave>
        </pitch>'''
    new_m1_notes = '''      </direction>
''' + harmony_cmaj7 + '''      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <octave>5</octave>
        </pitch>'''
    content = content.replace(old_m1_notes, new_m1_notes, 1)

    # 4. Add barline + rehearsal C + harmony at measure 21 (guitar)
    barline_rehearsal_c = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction placement="above">
        <direction-type>
          <rehearsal enclosure="rectangle">C</rehearsal>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>F</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    # Guitar measure 21 - need to find unique pattern
    # Search for measure 21 in P1 - it's the 21st measure, after measure 20
    old_m21 = '''    <measure number="21">
      <note>'''
    new_m21 = '''    <measure number="21">
''' + barline_rehearsal_c + '''      <note>'''
    # Only replace first occurrence (P1)
    content = content.replace(old_m21, new_m21, 1)

    # 5. Add barline + rehearsal D at measure 31
    barline_rehearsal_d = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction placement="above">
        <direction-type>
          <rehearsal enclosure="rectangle">D</rehearsal>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>G</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m31 = '''    <measure number="31">
      <note>'''
    new_m31 = '''    <measure number="31">
''' + barline_rehearsal_d + '''      <note>'''
    content = content.replace(old_m31, new_m31, 1)

    # 6. Add barline + rehearsal E at measure 41
    barline_rehearsal_e = '''
      <barline location="right">
        <bar-style>light-light</bar-style>
      </barline>
      <direction placement="above">
        <direction-type>
          <rehearsal enclosure="rectangle">E</rehearsal>
        </direction-type>
      </direction>
      <harmony>
        <root><root-step>C</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
'''
    old_m41 = '''    <measure number="41">
      <note>'''
    new_m41 = '''    <measure number="41">
''' + barline_rehearsal_e + '''      <note>'''
    content = content.replace(old_m41, new_m41, 1)

    # 7. Add guitar dyads - convert first C+E in measure 1 to dyad (add G as chord tone)
    # Add chord tone G3 before C5 in measure 1
    old_first_note = '''      <harmony>
        <root><root-step>C</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>'''
    new_first_note = '''      <harmony>
        <root><root-step>C</root-step></root>
        <kind>major-seventh</kind>
      </harmony>
      <note>
        <pitch>
          <step>G</step>
          <octave>3</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <chord/>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <octave>5</octave>
        </pitch>
        <duration>8</duration>
        <voice>1</voice>
        <type>quarter</type>
      </note>'''
    content = content.replace(old_first_note, new_first_note, 1)

    # 8. Add movement title for V2
    content = content.replace(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<score-partwise version=\"3.1\">",
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<score-partwise version=\"3.1\">\n  <movement-title>V2drift_study_no1_guitar_string_quartet</movement-title>"
    )

    dst.write_text(content, encoding="utf-8")
    print(f"Wrote {dst}")

if __name__ == "__main__":
    main()
