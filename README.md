# Guitar String Quartet — Composition Workspace

A long-term composition environment for original music for guitar and string quartet by Mike Bryant, intended for collaboration with the Sylva Quartet.

## Purpose

This repository is a structured workspace for composing a new album of chamber-jazz works. It supports the full creative cycle from initial ideas through arrangement, MusicXML generation, revision, and final engraving. The system is designed for multiple compositions over time, with future recording and performance in mind.

## Instrumentation

**Core ensemble:**
- Guitar
- Violin I
- Violin II
- Viola
- Cello

Optional later expansions: Upright Bass, Flugelhorn. The repository assumes the core ensemble is guitar + string quartet.

## Collaboration Context

The music is written for real players in collaboration with the **Sylva Quartet**. Parts prioritise idiomatic string writing, expressive independence, clear rehearsal logic, and playable but sophisticated material.

## Composition Logic

Future compositions in this repo are generated using a **guitar-first chamber-jazz logic**: the guitar's harmonic and rhythmic identity drives the piece, and the string quartet is built in response to it. See `rules/guitar-first-composition-rule.md`.

**Four-Engine Album Plan:** The album architecture is defined by four primary engines (Frisell Atmosphere, Wayne Shorter Narrative, Scofield–Holland Groove, Counterpoint / Tonality Hybrid) plus optional Zappa secondary. See `docs/album_engine_plan.md`.

**Composition Engine Reference Manual:** Central rulebook for all composition engines, score standards, and validation rules. See `docs/composition_engine_reference.md`.

## Aesthetic Orientation

Chamber jazz inspired by Bill Frisell’s string work (Richter 858, Sign of Life, Big Sur, When You Wish Upon a Star). Key characteristics:

- Spacious chamber textures
- Slow harmonic bloom
- Independent string voices
- Lyrical guitar writing
- Conversational ensemble interaction
- Asymmetrical phrasing
- Transparent orchestration
- Silence and restraint

## Repository Structure

```
docs/           — Album concept, Four-Engine Album Plan, Composition Engine Reference Manual, workflow, style guide
prompts/        — Master composition engine, MusicXML, arrangement, revision templates
rules/          — Instrumentation, texture, harmony, rhythm, anti-generic, engraving, GCE rubric
compositions/   — Individual works (each as a folder from composition-template)
references/     — Frisell notes, Sylva Quartet project notes, comparative models
templates/      — Folder template, score header, part preparation checklist
scratch/        — Ideas, motifs, harmonic cells, titles
```

## Adding New Compositions

1. Copy `compositions/composition-template/` to a new folder under `compositions/` (e.g. `compositions/song-title/`).
2. Fill in `notes.md`, `lead-sheet.md`, and `arrangement-plan.md`.
3. Generate MusicXML into `exports/musicxml/`.
4. Track revisions in `revisions.md`.
5. Export PDF and audio into their respective folders.

See `compositions/_index.md` for full instructions.

## Prompts and Rules

- **Prompts** (`prompts/`) define how to generate material: master engine, MusicXML, arrangement, revision.
- **Rules** (`rules/`) constrain output: instrumentation, texture, harmony, rhythm, anti-generic patterns, engraving, score readability standard.
- **GCE rubric** (`rules/gce-rubric.md`) scores outputs 0–10; only accept ≥ 9.0 unless explicitly disabled.

All prompts and rules enforce: no optimisation of phrasing, no forced symmetry, preservation of asymmetry, musical intelligence over density, and avoidance of AI-generic composition patterns.
