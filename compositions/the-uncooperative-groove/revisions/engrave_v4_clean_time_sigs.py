#!/usr/bin/env python3
"""
Engraving cleanup for The Uncooperative Groove.
Emits <time> only at meter change points (not every bar).
Output: V4_The_Uncooperative_Groove_Engraved.musicxml
"""
import os
import xml.etree.ElementTree as ET

def get_time_from_attrs(attrs):
    """Extract (beats, beat_type) from attributes or None."""
    time_el = attrs.find("time")
    if time_el is None:
        return None
    beats = time_el.find("beats")
    beat_type = time_el.find("beat-type")
    if beats is not None and beat_type is not None:
        return (beats.text, beat_type.text)
    return None

def attrs_has_only_time(attrs):
    """True if attributes has only time (no divisions, no key)."""
    if attrs is None:
        return False
    time_el = attrs.find("time")
    divs = attrs.find("divisions")
    key_el = attrs.find("key")
    if time_el is None:
        return False
    return divs is None and key_el is None

def clean_measure(measure, last_time, is_first_measure_of_first_part):
    """
    Remove redundant <time> when meter unchanged.
    Emit <time> only at meter change points.
    Return new last_time.
    """
    attrs = measure.find("attributes")
    if attrs is None:
        return last_time

    current_time = get_time_from_attrs(attrs)
    if current_time is None:
        return last_time

    # Always keep time in first measure (establishes meter)
    if is_first_measure_of_first_part:
        return current_time

    # Remove time when meter unchanged (redundant)
    if attrs_has_only_time(attrs) and current_time == last_time:
        time_el = attrs.find("time")
        attrs.remove(time_el)
        if len(attrs) == 0:
            measure.remove(attrs)
        return last_time

    # Meter changed: keep time
    return current_time

def clean_musicxml(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    parts = root.findall("part")
    first_part = True

    for part in parts:
        last_time = None
        for i, measure in enumerate(part.findall("measure")):
            is_first = (i == 0) and first_part
            last_time = clean_measure(measure, last_time, is_first)
        first_part = False

    # Preserve DOCTYPE from original
    with open(input_path, "r", encoding="utf-8") as f:
        header_lines = []
        for _ in range(2):
            line = f.readline()
            if line.startswith("<?xml") or line.strip().startswith("<!DOCTYPE"):
                header_lines.append(line.rstrip())
            if not line:
                break

    tree.write(output_path, encoding="unicode", default_namespace="", method="xml", xml_declaration=False)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Prepend proper header (ElementTree drops DOCTYPE)
    doctype = '<!DOCTYPE score-partwise  PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'
    if "<!DOCTYPE" not in content:
        content = '<?xml version="1.0" encoding="utf-8"?>\n' + doctype + "\n" + content
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    base = os.path.dirname(__file__)
    inp = os.path.join(base, "..", "musicxml", "V3_The_Uncooperative_Groove_Final.musicxml")
    out = os.path.join(base, "..", "musicxml", "V4_The_Uncooperative_Groove_Engraved.musicxml")
    inp = os.path.abspath(inp)
    out = os.path.abspath(out)
    clean_musicxml(inp, out)
    print(f"Exported: {out}")

if __name__ == "__main__":
    main()
