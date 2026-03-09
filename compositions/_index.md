# Compositions Index

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

| Folder | Title | Asset Types | Latest Version | Readability |
|--------|-------|-------------|----------------|-------------|
| drift-study-no1 | Drift Study No.1 | musicxml sibelius video | drift_study_no1_guitar_string_quartet.musicxml | Partial |
| eviscerating-angels | Eviscerating Angels | musicxml | V3Eviscerating_Angels.musicxml | Yes |
| glass-engine | Glass Engine | archive musicxml sibelius | V8glass_engine_guitar_string_quartet.musicxml | Yes |
| sylva-fracture | Sylva Fracture | musicxml | Sylva_Fracture.musicxml | Yes |
| sylva-narrative-no2 | Sylva Narrative No.2 | musicxml | V5Sylva_Narrative_No2.musicxml | Partial |
| sylva-sketch-2 | Sylva Sketch 2 | musicxml | Sylva_Sketch_2.musicxml | Needs verification |
| working-title-01 | working-title-01 | — | — | — |
| composition-template | (template) | — | — | Do not use for real compositions |

## TODO

— **Save new files directly into the correct composition folder** — When generating MusicXML, Sibelius exports, or video, save into `compositions/[piece-name]/musicxml/`, `sibelius/`, or `video/` rather than the compositions root.

— **Run organiser:** `py scripts/organise-compositions.py` to move loose files into correct folders.
