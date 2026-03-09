# Composition Workflow

A repeatable workflow for each composition in this project.

## 1. Idea

Capture the initial impulse: mood, harmonic colour, texture, or melodic fragment. Record in `scratch/ideas.md` or in the composition’s `notes.md`.

## 2. Motif Sketch

Develop core melodic or rhythmic material. Use `scratch/motifs.md` or `compositions/[title]/sketches/`. Prioritise identity over density.

## 3. Harmonic Sketch

Define harmonic language: key areas, modal shifts, non-root support tones, suspension chains. Use `scratch/harmonic-cells.md` or composition notes.

## 4. Lead Sheet

Produce a lead sheet: melody, chord symbols, form. Store in `compositions/[title]/lead-sheet.md` or equivalent. This is the compositional backbone.

## 5. Arrangement Plan

Plan orchestration before generating full score:
- Texture choices (see `rules/quartet-texture-rules.md`)
- Instrument roles per section
- Entry and exit points
- Dynamic arc

Document in `compositions/[title]/arrangement-plan.md`.

## 6. MusicXML Generation

Generate MusicXML using prompts in `prompts/`. Output to `compositions/[title]/exports/musicxml/`. Apply engraving rules from `rules/engraving-rules.md`.

## 7. Revision

Review against GCE rubric (`rules/gce-rubric.md`). Score must be ≥ 9.0. Apply revision template (`prompts/revision-template.md`). Log changes in `revisions.md`.

## 8. Final Engraving

Polish for Sibelius compatibility: instrument names, tempo marks, rehearsal letters, chord symbols, spacing, clean notation. Use `templates/part-preparation-checklist.md` before rehearsal or recording.
