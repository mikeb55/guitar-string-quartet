# Composition Bootstrap Rules

**REPOSITORY RULE — COMPOSITION BOOTSTRAP**

Before generating any composition, ensure the canonical folder structure exists.

## Given PIECE_SLUG (kebab-case title)

**Base path:** `compositions/PIECE_SLUG/`

## Create if missing

- `archive/`
- `audio/`
- `musicxml/`
- `pdf/`
- `sibelius/`
- `sketches/`
- `video/`
- `revisions/`

## Create root documentation files if missing

- `README.md`
- `notes.md`
- `lead-sheet.md`
- `arrangement-plan.md`
- `revisions.md`

## Output locations

- **Musical outputs:** `compositions/PIECE_SLUG/musicxml/`
- **Generator scripts:** `compositions/PIECE_SLUG/revisions/`

## Path rules

- Do not use absolute paths
- Use only relative paths inside the workspace
- Overwrite existing files if versions match
