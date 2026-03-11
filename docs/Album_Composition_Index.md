# Guitar + String Quartet Album — Composition Index

This document tracks all compositions generated for the project.

**Last updated:** 2026-03-09

**Album architecture:** See `docs/album_engine_plan.md` for the Four-Engine Album Plan (Frisell Atmosphere, Wayne Shorter Narrative, Scofield–Holland Groove, Counterpoint / Tonality Hybrid, optional Zappa secondary).

---

## Engine Column Standard

Engines allowed:

- Frisell Atmosphere
- Slonimsky Harmonic
- Andrew Hill
- Wayne Shorter
- Tonality Vault
- Counterpoint
- Hybrid

**Dual Engine:** Primary + Secondary (e.g. Wayne Shorter + Frisell Atmosphere)

---

## Key Tracking

- Extract key signature from MusicXML when possible
- If ambiguous or modal, mark: **modal / ambiguous**

---

## Composition Index

| Title | Key | Engine | Duration | Tempo | Mood | Latest Version | Folder | Readability |
|-------|-----|--------|----------|-------|------|----------------|--------|-------------|
| Drift Study No.2 | Dm (modal) | Scofield–Holland Hybrid | ~5 min | q = 105 | Groove, contrapuntal | Drift_Study_No2_Scofield_Holland | compositions/drift-study-no2 | Yes |
| Home Engine | Dm (modal) | Scofield–Holland + Zappa | ~5 min | q = 104 | Groove, Zappa in D | V5_Home_Engine_Scofield | compositions/home-engine | Yes |
| Eviscerating Angels | Am / Em | Hybrid | ~5 min | q = 76 | Dark, tense | V3Eviscerating_Angels | compositions/eviscerating-angels | Yes |
| Glass Engine | C | Tonality Vault | ~5 min | q = 66 | — | V8glass_engine_guitar_string_quartet | compositions/glass-engine | Yes |
| Sylva Fracture | F# Lydian | Wayne Shorter + Zappa | ~5 min | q = 72 | Dramatic narrative | Sylva_Fracture | compositions/sylva-fracture | Yes |
| Sylva Narrative No.2 | D Lydian (modal) | Wayne Shorter + Frisell | ~5 min | q = 72 | Floating, spacious | V6Sylva_Narrative_No2 | compositions/sylva-narrative-no2 | Yes |
| Sylva Sketch 2 | modal / ambiguous | Andrew Hill | ~5 min | q = 88 | Angular, chromatic | Sylva_Sketch_2 | compositions/sylva-sketch-2 | Needs verification |

---

## Update Instructions

When a new composition is created or a new version is exported:

1. Ensure the piece uses its canonical folder (one piece, one folder — see `rules/one-piece-one-folder.md`)
2. Add or update the row in the table above
3. Record the engine used (from engine menu selection)
4. Sort alphabetically by composition title
5. Extract key from MusicXML (`<fifths>`) or lead-sheet when available
6. Record the latest MusicXML filename (highest version number wins)
7. Folder column must use canonical path: `compositions/[piece-name]/`
