# Composition Folder Template

Use this structure when creating a new composition folder. See `rules/composition-bootstrap-rules.md`.

## Required Structure

```
compositions/[piece-slug]/
├── README.md
├── notes.md
├── lead-sheet.md
├── arrangement-plan.md
├── revisions.md
├── archive/
├── audio/
├── musicxml/
├── pdf/
├── sibelius/
├── sketches/
├── video/
└── revisions/
```

## Output Locations

- **Musical outputs:** `compositions/[piece-slug]/musicxml/`
- **Generator scripts:** `compositions/[piece-slug]/revisions/`

## Creation Steps

1. Copy `compositions/composition-template/` to `compositions/[piece-slug]/`
2. Rename and update README.md
3. Fill notes.md, lead-sheet.md, arrangement-plan.md
4. Generate MusicXML to `musicxml/`
5. Log revisions in `revisions.md`
6. Place generator scripts in `revisions/`

## Naming Convention

Use lowercase, hyphenated slugs (e.g. `mist-over-still-waters`, `first-light`).
