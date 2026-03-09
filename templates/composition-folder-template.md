# Composition Folder Template

Use this structure when creating a new composition folder.

**Guitar-first rule applies:** Compositions are generated with guitar harmonic material first; strings built around it. See `rules/guitar-first-composition-rule.md`.

**Anti-monotony rule applies:** Motifs evolve; texture changes every 6 bars; at least three structural phases. See `rules/anti-monotony-composition-rule.md`.

**Score readability standard applies:** All MusicXML exports must include chord symbols, boxed rehearsal letters, and rehearsal-friendly layout. See `rules/score-readability-standard.md`.

## Required Files

```
compositions/[title]/
├── README.md           — Brief description, key, form
├── notes.md            — Ideas, sketches, development notes
├── lead-sheet.md       — Melody, chords, form
├── arrangement-plan.md — Texture, roles, orchestration plan
├── revisions.md        — Revision log
├── exports/
│   ├── musicxml/       — MusicXML files
│   ├── pdf/            — Rendered scores
│   └── audio/          — Recordings, mockups
└── sketches/          — Motif sketches, harmonic drafts
```

## Creation Steps

1. Copy `compositions/composition-template/` to `compositions/[title]/`
2. Rename and update README.md with composition-specific info
3. Fill notes.md with initial ideas
4. Develop lead-sheet.md
5. Complete arrangement-plan.md
6. Generate MusicXML to musicxml/
7. Log revisions in revisions.md
8. **Update `docs/Album_Composition_Index.md`** — add or update the composition row (see `rules/repository-maintenance.md`)

## Naming Convention

Use lowercase, hyphenated titles (e.g. `mist-over-still-waters`, `first-light`).
