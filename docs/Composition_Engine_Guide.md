# Guitar–String Quartet Composition Engine Guide

**Version 2.1**  
**Last updated:** 2026-03-09

This guide documents the composition engine system, rules, and score standards for the guitar-string-quartet repository. It is synchronized with `rules/`, `prompts/`, and engine implementations.

---

## Table of Contents

1. [Overview](#overview)
2. [Composition Engine Menu](#composition-engine-menu)
3. [Available Engines](#available-engines)
3. [Dual Engine Mode](#dual-engine-mode)
4. [Secondary Engine Support (Zappa)](#secondary-engine-support-zappa)
5. [Hybrid Engine](#hybrid-engine)
6. [Score Readability Standards](#score-readability-standards)
7. [Composition Rules](#composition-rules)
8. [Engine Combinations](#engine-combinations)
9. [Reference Locations](#reference-locations)

---

## Overview

The composition system supports multiple engines that determine harmonic, melodic, and structural logic. Engines may be used singly, in dual-engine mode (primary + secondary), or in hybrid combinations.

**Primary ensemble:** Guitar, Violin I, Violin II, Viola, Cello

**Core principle:** Guitar-first generation — guitar harmonic vocabulary is generated before strings; strings respond to, frame, or contrast with guitar material.

---

## Composition Engine Menu

New pieces should begin by selecting an engine from the engine menu rather than writing prompts manually.

**Workflow:**
1. Open `prompts/engine_menu.md`
2. Choose an engine (single or dual-engine pairing)
3. Copy `prompts/new_composition_template.md`
4. Fill in the fields (piece name, key, tempo, form, motif seed, etc.)
5. Run the composition generation

**Engine menu options:** Frisell Atmosphere, Wayne Shorter, Slonimsky Harmonic, Andrew Hill, Counterpoint, Tonality Vault, Hybrid, Wayne Shorter + Zappa, Frisell + Counterpoint, Shorter + Slonimsky.

**Helper:** See `tools/start_new_piece.md` for step-by-step instructions.

---

## Available Engines

### Frisell Atmosphere Engine

**Characteristics:**
- Spacious harmony
- Floating tonal centres
- Strong guitar identity
- Evolving texture

**Best for:** ECM-style ballads, cinematic pieces

**Album suitability:** 10/10

---

### Slonimsky Harmonic Engine

**Characteristics:**
- Intervallic symmetry
- Exotic harmonic movement
- Surprising melodic intervals

**Best for:** Modern jazz compositions, angular melodic writing

**Album suitability:** 8.5/10

---

### Andrew Hill Engine

**Characteristics:**
- Asymmetric phrasing
- Unusual harmonic shifts
- Motivic mutation

**Best for:** Experimental chamber jazz

**Album suitability:** 8.7/10

---

### Tonality Vault Engine

**Characteristics:**
- Rotating tonal systems
- Large harmonic palette

**Best for:** Large-scale compositions

**Album suitability:** 9/10

---

### Counterpoint Engine

**Characteristics:**
- Independent melodic lines
- Evolving ensemble interaction

**Best for:** String-driven compositions

**Album suitability:** 9.2/10

---

### Wayne Shorter Engine

**Characteristics:**
- Narrative harmony
- Evolving motifs
- Dramatic structural arcs
- Motifs evolve rather than repeat
- Harmony behaves narratively rather than functionally
- Phrases often asymmetrical (5, 7, 9 bar groupings)
- Melody leads harmony

**Best for:** Sophisticated modern jazz chamber music

**Album suitability:** 9.6/10

**Full specification:** `rules/wayne-shorter-composition-engine.md`

---

## Dual Engine Mode

**Full specification:** `rules/dual-engine-composition-mode.md`

Dual engine mode uses two engines simultaneously with distinct roles.

### Engine Roles

| Role | Controls |
|------|----------|
| **Primary** | Structural logic, melodic development |
| **Secondary** | Harmonic vocabulary, texture design |

### Generation Logic

1. Generate motif using primary engine rules
2. Generate harmonic vocabulary using secondary engine rules
3. Combine both into a unified structural design

### Validation

Both engines must influence the final composition:
- Motif evolution from primary engine
- Harmonic vocabulary from secondary engine

If either engine influence is weak, regenerate.

### Example Pairings

- Shorter + Frisell
- Shorter + Slonimsky
- Shorter + Zappa (limited)
- Frisell + Counterpoint
- Tonality Vault + Counterpoint
- Hill + Slonimsky

---

## Secondary Engine Support (Zappa)

Zappa may be used as a **secondary engine only** (not primary). It contributes:

- Unexpected ensemble hits
- Rhythmic disruption
- Angular voicings
- Sudden dynamics

**Usage:** 1–3 gestures per piece, typically in a designated "fractured" section.

**Example:** Sylva Fracture — Wayne Shorter primary, Zappa secondary (section E only).

---

## Hybrid Engine

**Characteristics:**
- Combines multiple engines
- Maximum contrast

**Best for:** Experimental compositions

**Album suitability:** 9.3/10

---

## Score Readability Standards

**Full specification:** `rules/score-readability-standard.md`

All MusicXML exports must follow professional rehearsal chart standards.

### 1. Chord Symbols (Mandatory)

- Above guitar staff
- Reflect actual harmony
- Appear whenever harmony changes
- Standard lead-sheet format (e.g. Dmaj7, G6, A7sus4, Bm9, Fmaj7#11)

### 2. Boxed Section Letters

- Capital letters: **A** **B** **C** **D** **E** **F**
- Above the system, boxed
- Aligned with first measure of each section
- Sections typically ≥ 6 bars

### 3. Rehearsal-Friendly Layout

- Double barlines at major transitions
- Tempo marking at beginning
- Descriptive tempo text when relevant
- Dynamic markings at texture changes

### 4. Part Clarity

| Instrument | Role |
|------------|------|
| Violin I | Primary melodic line |
| Violin II | Harmonic reinforcement / counterline |
| Viola | Interior motion / counterpoint |
| Cello | Pedal / grounding |
| Guitar | Harmonic engine |

---

## Composition Rules

### Guitar-First Rule

**Full specification:** `rules/guitar-first-composition-rule.md`

**Default generation order:**
1. Guitar harmonic vocabulary
2. Guitar rhythmic identity
3. Guitar melodic / dyadic material
4. String counterlines and textures
5. Full ensemble interaction

**Guitar material requirements:**
- ≥ 3 dyadic passages
- ≥ 3 triadic or chord-fragment passages
- ≥ 1 section where guitar harmony drives ensemble texture
- ≥ 1 guitar–violin contrapuntal passage
- ≥ 1 passage with rhythmic chord hits or punctuations

**Target distribution:** 35–45% dyads, 25–35% triads, 10–20% sustained chords, 10–20% single-note

---

### Anti-Monotony Rule

**Full specification:** `rules/anti-monotony-composition-rule.md`

- Motif: max 2 identical repetitions, max 3 with variation
- Static texture limit: 6 bars — then introduce variation
- Guitar: no same chord gesture > 2 times without variation
- Strings: if 2+ parts sustain same texture > 6 bars, introduce inner motion, register shift, or counterpoint
- Formal evolution: at least 3 structural phases (introduction, development, transformation)

---

### Structural Evolution Engine

**Full specification:** `rules/structural-evolution-engine.md`

Each composition must contain:
- 5–7 distinct textures
- 3 harmonic fields
- 2 ensemble-hit sections
- 1 contrast section
- 1 transformed return

**Variation thresholds:**
- Harmonic progression: no repeat > 4 bars without alteration
- Rhythmic cell: no repeat > 3 times consecutively
- Motif: must evolve after 2–3 iterations
- Texture: change every 8–12 bars

---

### Repetition Fatigue Rule

**Full specification:** `rules/repetition-fatigue-rule.md`

- Harmonic pattern: max 4 bars before variation
- Rhythmic cell: max 3 repeats
- Motif: must evolve after 2 iterations
- Texture: refresh every 10–16 bars

---

## Engine Combinations

| Primary | Secondary | Use Case |
|---------|-----------|----------|
| Wayne Shorter | Frisell | Narrative + spacious |
| Wayne Shorter | Zappa | Narrative + fractured moments |
| Wayne Shorter | Slonimsky | Narrative + angular intervals |
| Frisell | Counterpoint | Atmospheric + contrapuntal |
| Tonality Vault | Counterpoint | Large-scale + string-driven |
| Andrew Hill | Slonimsky | Experimental + intervallic |
| Hybrid | — | Maximum contrast |

---

## Reference Locations

| Resource | Path |
|----------|------|
| Engine menu | `prompts/engine_menu.md` |
| New composition template | `prompts/new_composition_template.md` |
| Start new piece helper | `tools/start_new_piece.md` |
| Master composition engine | `prompts/master-composition-engine.md` |
| MusicXML generation template | `prompts/musicxml-generation-template.md` |
| Engine choices (quick reference) | `docs/Engine Choices.md` |
| Album composition index | `docs/Album_Composition_Index.md` |
| Dual engine mode | `rules/dual-engine-composition-mode.md` |
| Wayne Shorter engine | `rules/wayne-shorter-composition-engine.md` |
| Score readability standard | `rules/score-readability-standard.md` |
| Guitar-first rule | `rules/guitar-first-composition-rule.md` |
| Anti-monotony rule | `rules/anti-monotony-composition-rule.md` |
| Structural evolution engine | `rules/structural-evolution-engine.md` |
| Guitar writing rules | `rules/guitar-writing-rules.md` |
| Repository maintenance | `rules/repository-maintenance.md` |

---

*This guide is synchronized with the rule system. Update when engines or rules change.*
