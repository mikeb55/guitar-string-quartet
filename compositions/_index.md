# Compositions Index

**Album overview:** See `docs/Album_Composition_Index.md` for the full album composition index (key, engine, duration, latest version).

## Composition Logic

**Guitar-first rule applies:** Generate guitar harmonic material first; build strings around it. See `rules/guitar-first-composition-rule.md`.

## Adding a New Composition

1. **Copy the template**
   - Copy the entire `composition-template/` folder
   - Paste into `compositions/` with the new composition's title as folder name
   - Use lowercase, hyphenated names (e.g. `mist-over-still-waters`)

2. **Update README.md**
   - Replace placeholder with composition-specific description
   - Add key, tempo, form overview

3. **Develop the composition**
   - `notes.md` — Ideas, sketches, development notes
   - `lead-sheet.md` — Melody, chords, form
   - `arrangement-plan.md` — Texture, roles, orchestration (use `prompts/arrangement-template.md`)

4. **Generate MusicXML**
   - Use `prompts/musicxml-generation-template.md`
   - Apply score readability standard (`rules/score-readability-standard.md`) — chord symbols, rehearsal letters, double barlines
   - Output to `[composition-folder]/musicxml/[title]_v01.musicxml`

5. **Revise**
   - Apply GCE rubric (`rules/gce-rubric.md`)
   - Use `prompts/revision-template.md`
   - Log changes in `revisions.md`

6. **Export**
   - PDF to `pdf/`
   - Audio to `audio/`
   - Video to `video/`

## Target Folder Structure (per composition)

```
<piece-folder>/
  README.md
  notes.md
  lead-sheet.md
  arrangement-plan.md
  revisions.md
  musicxml/
  sibelius/
  video/
  pdf/
  audio/
  sketches/
  archive/
```

## Active Compositions

| Folder | Title | Asset Types | Latest Version | Notes |
|--------|-------|-------------|----------------|-------|
| drift-study-no1 | Drift Study No1 | musicxml | drift_study_no1_guitar_string_quartet.musicxml |  |
| drift-study-no1-guitar-string-quartet | Drift Study No1 Guitar String Quartet | sibelius video | drift_study_no1_guitar_string_quartet.sib |  |
| eviscerating-angels | Eviscerating Angels | musicxml | Eviscerating_Angels.musicxml |  |
| glass-engine | Glass Engine | archive musicxml sibelius | V7glass_engine_guitar_string_quartet.musicxml | Some files in archive |
| sylva-fracture | Sylva Fracture | musicxml | Sylva_Fracture.musicxml | Wayne Shorter + Zappa |
| sylva-narrative-no2 | Sylva Narrative No2 | musicxml | Sylva_Narrative_No2.musicxml |  |
| sylva-sketch-2 | Sylva Sketch 2 | musicxml | Sylva_Sketch_2.musicxml |  |
| working-title-01 |  | — | — |  |
| composition-template | (template) | — | — | Do not use for real compositions |

## TODO

— **Save new files directly into the correct composition folder** — When generating MusicXML, Sibelius exports, or video, save into `compositions/[piece-name]/musicxml/`, `sibelius/`, or `video/` rather than the compositions root.

— **Run organiser:** `py scripts/organise-compositions.py` to move loose files into correct folders.
