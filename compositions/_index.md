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
   - Output to `[composition-folder]/musicxml/` (increment version for each revision; never overwrite)

5. **Revise**
   - Apply GCE rubric (`rules/gce-rubric.md`)
   - Use `prompts/revision-template.md`
   - Log changes in `revisions.md`

6. **Export**
   - PDF to `pdf/`
   - Audio to `audio/`
   - Video to `video/`
   - Generator scripts to `revisions/`

## Target Folder Structure (per composition)

See `rules/composition-bootstrap-rules.md`. Before generating any composition, ensure this structure exists:

```
<piece-folder>/
  README.md
  notes.md
  lead-sheet.md
  arrangement-plan.md
  revisions.md
  archive/
  audio/
  musicxml/
  pdf/
  sibelius/
  sketches/
  video/
  revisions/
```

- **Musical outputs:** `musicxml/`
- **Generator scripts:** `revisions/`

## Active Compositions

| Folder | Title | Asset Types | Latest Version | Notes |
|--------|-------|-------------|----------------|-------|
| drift-study-no2 | Drift Study No.2 | musicxml | Drift_Study_No2_Scofield_Holland.musicxml | Scofield–Holland Hybrid |
| home-engine | Home Engine | musicxml | V9_Home_Engine_Scofield.musicxml | Scofield–Holland + Zappa (D only) |
| eviscerating-angels | Eviscerating Angels | musicxml sibelius video | V3Eviscerating_Angels.musicxml |  |
| glass-engine | Glass Engine | archive musicxml sibelius | V9_Glass_Engine_Atmospheric_Master.musicxml | ECM atmospheric |
| sylva-fracture | Sylva Fracture | musicxml | Sylva_Fracture.musicxml |  |
| sylva-narrative-no1 | Sylva Narrative No.1 | musicxml | V1_Sylva_Narrative_No1.musicxml | Wayne Shorter Narrative |
| myrtles-prayer | Myrtle's Prayer | musicxml | V5_Myrtles_Prayer_Final.musicxml | Counterpoint/Tonality + Shorter |
| sylva-narrative-no2 | Sylva Narrative No2 | musicxml | V6Sylva_Narrative_No2.musicxml |  |
| sylva-sketch-2 | Sylva Sketch 2 | musicxml | Sylva_Sketch_2.musicxml |  |
| unreliable-gravity | Unreliable Gravity | musicxml revisions notes lead-sheet arrangement-plan | V2_Unreliable_Gravity_7-4.musicxml | Andrew Hill, 7/4 |
| the-uncooperative-groove | The Uncooperative Groove | scaffold created | no musicxml yet | Scofield–Zappa Rhythmic Hybrid |
| labyrinth-of-quiet-motions | Labyrinth of Quiet Motions | musicxml | V1_Labyrinth_of_Quiet_Motions.musicxml | Polyphonic Labyrinth / Counterpoint Hybrid |
| working-title-01 |  | — | — |  |
| composition-template | (template) | — | — | Do not use for real compositions |

## Archived Compositions

| Folder | Title | Notes |
|--------|-------|------|
| archive/drift-study-no1 | Drift Study No.1 | Retired composition experiment |

## TODO

— **Save new files directly into the correct composition folder** — When generating MusicXML, Sibelius exports, or video, save into `compositions/[piece-name]/musicxml/`, `sibelius/`, or `video/` rather than the compositions root.

— **Run organiser:** `py scripts/organise-compositions.py` to move loose files into correct folders.
