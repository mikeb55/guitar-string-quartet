# Composition Repository Audit Report

**Date:** 2026-03-09  
**Root:** `compositions/`

---

## Summary

- All active compositions now have the standardized directory structure.
- All MusicXML files are inside `musicxml/` (or `archive/` for retired versions).
- One index file (`_index.md`) exists in compositions root — project metadata, not a composition file.

---

## Composition Directory Status

| Composition | MusicXML Versions | Directory Status |
|-------------|------------------|------------------|
| composition-template | 0 | OK |
| drift-study-no2 | 1 | OK |
| eviscerating-angels | 3 | OK |
| glass-engine | 8 (1 in archive) | OK |
| home-engine | 9 | OK |
| myrtles-prayer | 1 | OK |
| sylva-fracture | 1 | OK |
| sylva-narrative-no1 | 1 | OK |
| sylva-narrative-no2 | 4 | OK |
| sylva-sketch-2 | 1 | OK |
| working-title-01 | 0 | OK |
| archive/drift-study-no1 | 2 | OK |

---

## Loose Files in compositions/

- `_index.md` — project index (metadata). Consider moving to `docs/` if strict "no files in root" is required.

---

## Actions Completed

1. Created missing directories for `drift-study-no2`, `sylva-narrative-no1`, `composition-template`.
2. `home-engine` and `myrtles-prayer` already had full structure.
3. Created `rules/composition-folder-structure.md`.
4. Updated `prompts/musicxml-generation-template.md` and `prompts/master-composition-engine.md` with export/folder rules.
5. Updated `docs/composition_engine_reference.md` with Repository Composition Folder Structure section.
6. Regenerated `docs/composition_engine_reference.docx`.
