# Repository Organisation

## Composition Logic

Future compositions are generated using a **guitar-first chamber-jazz logic**: the guitar's harmonic and rhythmic identity drives the piece, with the string quartet built in response. See `rules/guitar-first-composition-rule.md`. This applies to all generation prompts and templates unless explicitly overridden.

All compositions follow **Anti-Monotony rules** to avoid repetitive textures and enforce evolving chamber interaction. See `rules/anti-monotony-composition-rule.md`.

All MusicXML exports must follow the **Score Readability Standard** for professional rehearsal charts: chord symbols, boxed rehearsal letters, double barlines, tempo and dynamics. See `rules/score-readability-standard.md`.

## Folder Logic

- **compositions/** — One folder per composition. All versions of the same piece live together.
- **compositions/composition-template/** — Template to copy when starting a new piece. Do not use for real compositions.
- **compositions/_index.md** — Master index of all compositions and their assets.
- **rules/** — Composition and engraving rules.
- **prompts/** — Master engine, MusicXML template, arrangement templates.
- **templates/** — Score headers, checklists.
- **references/** — Listening notes, project notes.
- **docs/** — Style guide, workflow, album concept.
- **scratch/** — Ideas, motifs, harmonic cells (development scratchpad).

## Version Logic

- **One folder per piece** — Do not create separate top-level folders for v2, v3, regenerated, etc.
- **Version info stays in filenames** — e.g. `glass_engine_v3_gce9.musicxml`, `piece_name_v02.sib`.
- **Archive for duplicates** — Obsolete copies, uncertain extras go in `archive/` within the composition folder.
- **revisions.md** — Log version history and rationale in each composition folder.

## Naming Rules for New Pieces

### Folder names
- Lowercase, hyphenated: `glass-engine`, `drift-study-no1`, `mist-over-still-waters`
- No instrumentation in folder name unless distinguishing genuinely different pieces
- No version suffixes (v2, v3) in folder names

### Filenames (recommended)
- MusicXML: `<piece-name>_v01.musicxml`, `<piece-name>_v02_gce9.musicxml`
- Sibelius: `<piece-name>_v01.sib`, `<piece-name>_v02.sib`
- Video: `<piece-name>_playback_v01.wmv`, `<piece-name>_playback_v01.mp4`
- PDF: `<piece-name>_score.pdf`, `<piece-name>_parts.pdf`

## File Placement

| Type | Destination |
|------|--------------|
| .musicxml, .xml | `musicxml/` |
| .sib | `sibelius/` |
| .mp4, .wmv, .mov | `video/` |
| .pdf | `pdf/` |
| .wav, .mp3, .flac, .aif, .aiff | `audio/` |
| .mid, .midi, draft .txt | `sketches/` |
| Obsolete duplicates | `archive/` |

## Handling Future Versions

1. **Save directly into the composition folder** — Do not dump new exports into `compositions/` root.
2. **Use the correct subfolder** — musicxml/, sibelius/, video/, etc.
3. **Keep version info in the filename** — `piece_v03.musicxml` not `piece.musicxml`.
4. **Update revisions.md** — Log what changed and why.
5. **Update README.md** — Set "latest recommended file" to the best version.
6. **Never create** `compositions/glass-engine-v2/` or similar — all versions go in `glass-engine/`.

## Automatic File Organiser

Run `py scripts/organise-compositions.py` (or `organise-compositions.bat`) to:

- Move loose composition files from `compositions/` root into correct piece folders
- Create missing composition folders and subfolders (musicxml/, sibelius/, video/, etc.)
- Update `compositions/_index.md` with latest versions and asset types
- Never delete files; uncertain items go to `archive/` and are logged in README.md

## Album Composition Index

**See `docs/Album_Composition_Index.md`.** Tracks all compositions with key, engine, duration, latest version. Update this index when creating new compositions or exporting new versions. See `rules/repository-maintenance.md`.

## TODO

- When generating new MusicXML, Sibelius exports, or video, save directly into the correct composition folder (`compositions/[piece-name]/musicxml/`, etc.) instead of the compositions root.
