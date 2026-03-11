# Four-Engine Album Composition Plan

**Version 1.0**  
**Last updated:** 2026-03-09

This document defines the album engine architecture for the guitar-string-quartet composition project. It establishes four primary engines, an optional secondary engine, rotation strategy, and composition guidelines.

---

## Table of Contents

1. [Overview](#overview)
2. [The Four Engine System](#the-four-engine-system)
3. [Engine Specifications](#engine-specifications)
4. [Optional Zappa Secondary Engine](#optional-zappa-secondary-engine)
5. [Album Rotation Strategy](#album-rotation-strategy)
6. [Composition Guidelines](#composition-guidelines)
7. [Reference Locations](#reference-locations)

---

## Overview

The album is built around **six primary composition engines** (plus optional secondary engines), each with distinct harmonic, rhythmic, and structural character. Pieces may use one engine exclusively or combine a primary engine with the optional Zappa secondary engine for limited disruptive moments.

**Core principle:** Guitar-first generation. The guitar drives harmonic rhythm; strings respond, frame, and contrast.

**Ensemble:** Guitar, Violin I, Violin II, Viola, Cello

---

## The Engine System

**Primary engines:**

| Engine | Character | Best For |
|--------|-----------|----------|
| **Frisell Atmosphere** | Spacious, floating, lyrical | ECM-style ballads, cinematic pieces |
| **Wayne Shorter Narrative** | Motif-driven, dramatic arcs, narrative harmony | Sophisticated chamber jazz |
| **Scofield–Holland Groove** | Syncopated, bass-driven, rhythmically forward | Medium groove, ensemble dialogue |
| **Counterpoint / Tonality Hybrid** | Independent lines, rotating tonal systems | String-driven, large-scale works |
| **Wheeler Lyric** | Luminous, floating harmony, emotional transparency | ECM lyric ballads, violin-led melody |
| **Stravinsky Chamber Pulse** | Rhythmic cells, shifting meters, ensemble gestures | Rhythmically energetic chamber pieces |

---

## Engine Specifications

### 1. Frisell Atmosphere Engine

**Characteristics:**
- Spacious harmony
- Floating tonal centres
- Strong guitar identity
- Evolving texture
- Lyrical phrasing
- Restraint and silence

**Guitar role:** Dyads, chord voicings, sustained harmony, lyrical fragments.

**String role:** Independent voices, responsive counterpoint, transparent orchestration.

**Best for:** ECM-style ballads, cinematic pieces, slow harmonic bloom.

**Album suitability:** 10/10

---

### 2. Wayne Shorter Narrative Engine

**Characteristics:**
- Narrative harmony
- Evolving motifs
- Dramatic structural arcs
- Motifs evolve rather than repeat
- Harmony behaves narratively rather than functionally
- Phrases often asymmetrical (5, 7, 9 bar groupings)
- Melody leads harmony

**Guitar role:** Motif development, harmonic narrative, non-functional progressions.

**String role:** Melodic counterlines, dialogue, structural support.

**Best for:** Sophisticated modern jazz chamber music.

**Album suitability:** 9.6/10

**Full specification:** `rules/wayne-shorter-composition-engine.md`

---

### 3. Scofield–Holland Groove Engine

**Characteristics:**
- Groove-based harmony
- Syncopated guitar language
- Strong bass movement (cello-driven)
- Active ensemble dialogue
- Rhythmically forward-moving, not floating

**Inspiration:** John Scofield + Dave Holland ECM album "Memories of Home".

**Guitar role:** Dyads, triad pairs, short syncopated melodic fragments, chord punctuations. Avoid long monophonic passages.

**Strings:**
- Violin I: Melodic responses and fragments
- Violin II: Rhythmic echoes and harmonic colour
- Viola: Inner counterpoint engine
- Cello: Bass anchor (Dave Holland style)

**Harmony:** Modern modal jazz — Dm9, G13sus, Bbmaj7#11, Fmaj9, A7alt.

**Best for:** Medium groove pieces, ~100–110 bpm.

**Album suitability:** 9.5/10

---

### 4. Counterpoint / Tonality Hybrid Engine

**Characteristics:**
- Independent melodic lines
- Rotating tonal systems
- Large harmonic palette
- Evolving ensemble interaction
- String-driven texture

**Guitar role:** Harmonic engine; supports and responds to string counterpoint.

**String role:** Primary melodic independence; quartet drives texture and development.

**Best for:** Large-scale compositions, string-driven pieces.

**Album suitability:** 9.6/10

---

### 5. Wheeler Lyric Engine

**Characteristics:**
- Long melodic arcs
- Lyrical phrasing
- Slow harmonic drift
- Emotional openness
- Transparent orchestration

**Influences:** Kenny Wheeler, ECM lyric writing, ECM chamber jazz orchestration.

**Guitar role:** Colour chords, dyads, quiet harmonic punctuation. Avoid rhythmically aggressive guitar.

**Strings:** Violin I (primary lyrical melody), Violin II (secondary melodic support), Viola (inner harmonic motion), Cello (lyrical bass lines).

**Best for:** Luminous ECM-style ballads, emotionally transparent chamber jazz.

**Album suitability:** 9.4/10

**Full specification:** `engines/wheeler_lyric_engine.md`

---

### 6. Stravinsky Chamber Pulse Engine

**Characteristics:**
- Rhythmic cells
- Shifting meters
- Sudden ensemble gestures
- Motivic rhythmic development

**Influences:** Stravinsky chamber music, modern chamber jazz, ECM rhythmic ensemble writing.

**Guitar role:** Dyads, rhythmic chords, percussive attacks.

**Strings:** Violin I (rhythmic motif leader), Violin II (counter-rhythm layer), Viola (inner rhythmic motor), Cello (percussive harmonic anchor).

**Best for:** Rhythmically energetic chamber pieces, syncopated ensemble writing.

**Album suitability:** 9.2/10

**Full specification:** `engines/stravinsky_chamber_pulse_engine.md`

---

## Optional Zappa Secondary Engine

Zappa may be used as a **secondary engine only** (not primary). It contributes:

- Ensemble hits
- Rhythmic fractures
- Harmonic collisions
- Orchestral accents

**Restrictions:**
- May **not** dominate the piece
- Must **not** replace the primary engine structure
- Should appear in **limited sections** only

**Recommended usage:**
- Development section
- Climax section
- Contrasting episode

**Example:** Sylva Fracture — Wayne Shorter primary, Zappa secondary (section E only). Home Engine — Scofield–Holland primary, Zappa secondary (section D only).

---

## Album Rotation Strategy

To ensure variety across the album:

1. **Rotate by engine:** No two consecutive pieces should use the same primary engine.
2. **Balance:** Aim for roughly equal representation of the four engines across the album.
3. **Zappa sparingly:** Use Zappa secondary in ≤ 2 pieces per album.
4. **Tempo contrast:** Alternate between slow (Frisell, Shorter) and medium groove (Scofield–Holland) where possible.
5. **Texture contrast:** Alternate between spacious (Frisell, Shorter) and rhythmically active (Scofield–Holland, Counterpoint).

**Suggested rotation order:** Frisell → Shorter → Scofield–Holland → Counterpoint → Wheeler Lyric → Stravinsky Chamber Pulse → (repeat)

---

## Composition Guidelines

1. **Guitar-first:** Generate guitar harmonic vocabulary before strings. See `rules/guitar-first-composition-rule.md`.

2. **No monophonic guitar:** Guitar must use dyads, triads, or chord fragments. Avoid long single-note passages.

3. **Texture evolution:** Every 6–10 bars, introduce variation in texture, rhythm, or harmony.

4. **Score format:** All MusicXML must include:
   - Guitar chord symbols (`<harmony>`)
   - Boxed rehearsal letters
   - Double barlines at section changes
   - Tempo marking
   - Dynamics at major structural shifts

5. **Anti-monotony:** Max 2 identical motif repetitions; no static texture > 6 bars. See `rules/anti-monotony-composition-rule.md`.

6. **Structural evolution:** Each piece should have 5–7 distinct textures, 3 harmonic fields, 1 transformed return. See `rules/structural-evolution-engine.md`.

---

## Reference Locations

| Resource | Path |
|----------|------|
| Composition Engine Guide | `docs/Composition_Engine_Guide.md` |
| Album Composition Index | `docs/Album_Composition_Index.md` |
| Engine menu | `prompts/engine_menu.md` |
| Guitar-first rule | `rules/guitar-first-composition-rule.md` |
| Wayne Shorter engine | `rules/wayne-shorter-composition-engine.md` |
| Wheeler Lyric engine | `engines/wheeler_lyric_engine.md` |
| Stravinsky Chamber Pulse engine | `engines/stravinsky_chamber_pulse_engine.md` |
| Dual engine mode | `rules/dual-engine-composition-mode.md` |
| Score readability standard | `rules/score-readability-standard.md` |

---

*This plan is synchronized with the composition engine system. Update when engines or album strategy change.*
