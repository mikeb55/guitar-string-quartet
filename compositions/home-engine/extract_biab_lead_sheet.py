"""
Extract Band-in-a-Box compatible lead sheet from Home Engine Scofield.
- Guitar melody only (monophonic)
- Chord symbols
- Section markers (A, B, C, D, etc.)
- Removes string quartet and orchestral parts
"""

from pathlib import Path

from music21 import note, stream, duration, key, tempo, metadata

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
MUSICXML_DIR = SCRIPT_DIR / "musicxml"
OUTPUT_DIR = SCRIPT_DIR / "lead-sheet"
SOURCE_FILE = MUSICXML_DIR / "V9_Home_Engine_Scofield.musicxml"
OUTPUT_BASE = "Home_Engine_Scofield_BiaB_LeadSheet"

VALID_TYPES = ('maxima', 'longa', 'breve', 'whole', 'half', 'quarter', 'eighth', '16th', '32nd', '64th', '128th', '256th')

def safe_duration_type(n):
    """Get a valid MusicXML duration type."""
    if n.duration.type and n.duration.type in VALID_TYPES:
        return n.duration.type
    result = duration.quarterLengthToClosestType(n.quarterLength)[0]
    return result if result in VALID_TYPES else 'quarter'

def get_melodic_note(n):
    """From a chord or note, return the highest pitch as a single note."""
    if n.isChord:
        top_pitch = n.sortAscending().pitches[-1]
        new_note = note.Note(top_pitch)
        dur = duration.Duration(n.quarterLength)
        dur.type = safe_duration_type(n)
        new_note.duration = dur
        if n.tie:
            new_note.tie = n.tie
        return new_note
    elif n.isNote:
        n_copy = note.Note(n.pitch)
        dur = duration.Duration(n.quarterLength)
        dur.type = safe_duration_type(n)
        n_copy.duration = dur
        if n.tie:
            n_copy.tie = n.tie
        return n_copy
    return None

def key_centre_from_signature(ks):
    """Get key centre string from KeySignature."""
    if not ks:
        return "Unknown"
    fifths = ks.sharps  # positive=sharps, negative=flats
    majors = ['C', 'G', 'D', 'A', 'E', 'B', 'F#']
    flats_major = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
    if fifths >= 0:
        return majors[fifths % 7] + " major"
    return flats_major[-fifths] + " major" if -fifths < 7 else "Unknown"

def extract_lead_sheet():
    from music21 import converter
    score = converter.parse(SOURCE_FILE)
    
    guitar_part = score.parts[0]
    
    lead_sheet = stream.Score()
    lead_sheet.metadata = metadata.Metadata()
    lead_sheet.metadata.title = "Home Engine Scofield"
    lead_sheet.metadata.composer = "Mike Bryant"
    
    guitar_staff = stream.Part()
    guitar_staff.partName = "Guitar"
    guitar_staff.partAbbreviation = "Gtr"
    
    for m in guitar_part.getElementsByClass(stream.Measure):
        new_measure = stream.Measure(number=m.number)
        
        if m.number == 1:
            if m.timeSignature:
                new_measure.timeSignature = m.timeSignature
            if m.keySignature:
                new_measure.keySignature = m.keySignature
            ts = m.getElementsByClass(tempo.MetronomeMark)
            if ts:
                new_measure.insert(0, ts[0])
        
        for el in m:
            if 'RehearsalMark' in el.classes:
                new_measure.insert(el.offset, el)
            elif 'Harmony' in el.classes or 'ChordSymbol' in el.classes:
                new_measure.insert(el.offset, el)
            elif 'Barline' in el.classes:
                new_measure.append(el)
        
        notes_and_rests = []
        for n in m.notesAndRests:
            if 'ChordSymbol' in n.classes or 'Harmony' in n.classes:
                continue
            if n.quarterLength == 0:
                continue
            if n.isRest:
                r = note.Rest()
                r.duration = duration.Duration(n.quarterLength)
                r.duration.type = safe_duration_type(n)
                notes_and_rests.append((n.offset, r))
            else:
                mel_note = get_melodic_note(n)
                if mel_note:
                    notes_and_rests.append((n.offset, mel_note))
        
        notes_and_rests.sort(key=lambda x: x[0])
        for offset, n in notes_and_rests:
            new_measure.insert(offset, n)
        
        guitar_staff.append(new_measure)
    
    lead_sheet.append(guitar_staff)
    return lead_sheet

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Extracting lead sheet from", SOURCE_FILE.name)
    lead_sheet = extract_lead_sheet()
    
    xml_path = OUTPUT_DIR / f"{OUTPUT_BASE}.musicxml"
    lead_sheet.write("musicxml", fp=str(xml_path))
    print("  MusicXML:", xml_path)
    
    midi_path = OUTPUT_DIR / f"{OUTPUT_BASE}.mid"
    lead_sheet.write("midi", fp=str(midi_path))
    print("  MIDI:", midi_path)
    
    pdf_path = OUTPUT_DIR / f"{OUTPUT_BASE}.pdf"
    try:
        lead_sheet.write("lilypond", fp=str(OUTPUT_DIR / f"{OUTPUT_BASE}.ly"))
        import subprocess
        ly_path = OUTPUT_DIR / f"{OUTPUT_BASE}.ly"
        subprocess.run(["lilypond", "-o", str(OUTPUT_DIR / OUTPUT_BASE), str(ly_path)], 
                      capture_output=True, timeout=30)
        if (OUTPUT_DIR / f"{OUTPUT_BASE}.pdf").exists():
            print("  PDF:", pdf_path)
        else:
            print("  PDF: skipped (LilyPond not in PATH or failed)")
    except Exception as e:
        print("  PDF: skipped (", str(e)[:50], ")")
    
    part = lead_sheet.parts[0]
    measures = list(part.getElementsByClass(stream.Measure))
    bar_count = len(measures)
    ks_list = part.flat.getElementsByClass(key.KeySignature)
    key_centre = key_centre_from_signature(ks_list[0]) if ks_list else "Unknown"
    
    chords_seen = []
    section_layout = []
    for m in measures:
        for el in m:
            if 'RehearsalMark' in el.classes:
                section_layout.append((m.number, str(el.content)))
            if 'ChordSymbol' in el.classes or 'Harmony' in el.classes:
                c = el.figure if hasattr(el, 'figure') else str(el.root())
                if c and (not chords_seen or chords_seen[-1][1] != c):
                    chords_seen.append((m.number, c))
    
    print("\n--- Report ---")
    print("Output file paths:")
    print("  ", xml_path)
    print("  ", midi_path)
    print("  ", pdf_path)
    print("Bar count:", bar_count)
    print("Key centre:", key_centre)
    print("Section layout:", section_layout[:12], "..." if len(section_layout) > 12 else "")
    print("Chord progression summary:", [c for _, c in chords_seen[:20]])
    print("Output path:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
