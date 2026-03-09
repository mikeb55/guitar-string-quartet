# Composition Engine Reference Manual

**Version 1.0**  
**Last updated:** 2026-03-09

This manual is the central rulebook describing every composition engine used in the guitar-string-quartet project. It is synchronized in both Markdown and Word formats.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Engine Architecture](#2-engine-architecture)
3. [Frisell Atmosphere Engine](#3-frisell-atmosphere-engine)
4. [Wayne Shorter Narrative Engine](#4-wayne-shorter-narrative-engine)
5. [Scofield–Holland Groove Engine](#5-scofieldholland-groove-engine)
6. [Counterpoint / Tonality Hybrid Engine](#6-counterpoint--tonality-hybrid-engine)
7. [Zappa Disruption Engine](#7-zappa-disruption-engine)
8. [Hybrid Engine Strategies](#8-hybrid-engine-strategies)
9. [Album Rotation Strategy](#9-album-rotation-strategy)
10. [Score Engraving Standards](#10-score-engraving-standards)
11. [MusicXML Validation Rules](#11-musicxml-validation-rules)
12. [Composition Quality Rules (GCE ≥ 9)](#12-composition-quality-rules-gce--9)
13. [Repository Structure Rules](#13-repository-structure-rules)
14. [Synchronization Rule](#14-synchronization-rule)

---

## 1. Overview

The repository uses a **modular engine system** to generate compositions for a guitar + string quartet ECM-style album. Each engine defines distinct harmonic, rhythmic, and structural logic. Compositions may use one engine exclusively or combine a primary engine with the optional Zappa disruption engine for limited contrasting moments.

**Core principle:** Guitar-first generation. The guitar drives harmonic rhythm; the string quartet responds, frames, and contrasts.

**Ensemble:** Guitar, Violin I, Violin II, Viola, Cello

---

## 2. Engine Architecture

The system is built around **four primary engines**:

| Engine | Character |
|--------|-----------|
| **Frisell Atmosphere** | Spacious, lyrical, ECM ambience |
| **Wayne Shorter Narrative** | Motif-driven, dramatic arcs |
| **Scofield–Holland Groove** | Syncopated, bass-driven, medium tempo |
| **Counterpoint / Tonality Hybrid** | Independent string voices, chamber counterpoint |

**Zappa** acts as a **secondary disruption engine** — never primary. It contributes ensemble hits, rhythmic fractures, and harmonic collisions in selected sections only.

---

## 3. Frisell Atmosphere Engine

**Characteristics:**
- Slow harmonic rhythm
- Lyrical guitar
- Pedal tones
- Suspended harmony
- ECM ambience

**Guitar role:** Dyads, chord voicings, sustained harmony, lyrical fragments.

**String role:** Independent voices, responsive counterpoint, transparent orchestration.

**Best for:** ECM-style ballads, cinematic pieces, slow harmonic bloom.

---

## 4. Wayne Shorter Narrative Engine

**Characteristics:**
- Motif transformation
- Dramatic harmonic shifts
- Clear sectional architecture
- Motifs evolve rather than repeat
- Harmony behaves narratively rather than functionally
- Phrases often asymmetrical (5, 7, 9 bar groupings)
- Melody leads harmony

**Guitar role:** Motif development, harmonic narrative, non-functional progressions.

**String role:** Melodic counterlines, dialogue, structural support.

**Best for:** Sophisticated modern jazz chamber music.

**Full specification:** `rules/wayne-shorter-composition-engine.md`

---

## 5. Scofield–Holland Groove Engine

**Characteristics:**
- Syncopated guitar dyads
- Bass-driven harmony
- Medium tempo groove
- Ensemble dialogue
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

---

## 6. Counterpoint / Tonality Hybrid Engine

**Characteristics:**
- Independent string voices
- Chamber counterpoint
- Evolving textures
- Rotating tonal systems
- Large harmonic palette

**Guitar role:** Harmonic engine; supports and responds to string counterpoint.

**String role:** Primary melodic independence; quartet drives texture and development.

**Best for:** Large-scale compositions, string-driven pieces.

---

## 7. Zappa Disruption Engine

**Role:** Secondary engine only. Never primary.

**Allowed contributions:**
- Ensemble hits
- Rhythmic fractures
- Harmonic collisions
- Orchestral accents

**Restrictions:**
- Used only in selected sections
- May not dominate the piece
- Must not replace the primary engine structure

**Recommended placement:** Development section, climax section, contrasting episode.

---

## 8. Hybrid Engine Strategies

Engines can combine while maintaining a clear **primary engine**. The primary engine controls structural logic and melodic development; the secondary engine contributes texture, harmonic vocabulary, or limited disruptive moments.

**Example pairings:**

| Primary | Secondary | Use Case |
|---------|-----------|----------|
| Wayne Shorter | Zappa | Narrative + fractured moments (e.g. Sylva Fracture) |
| Scofield–Holland | Zappa | Groove + ensemble hits in one section (e.g. Home Engine) |
| Frisell Atmosphere | Counterpoint | Atmospheric + contrapuntal |
| Wayne Shorter | Frisell | Narrative + spacious |
| Tonality Vault | Counterpoint | Large-scale + string-driven |

**Validation:** Both engines must influence the final composition. If either engine's influence is weak, regenerate.

---

## 9. Album Rotation Strategy

To ensure variety across the album, rotate engines and avoid consecutive pieces with the same character.

**Example 9-track structure:**

| Track | Engine |
|-------|--------|
| 1 | Frisell Atmosphere |
| 2 | Wayne Shorter Narrative |
| 3 | Scofield–Holland Groove |
| 4 | Counterpoint Hybrid |
| 5 | Wayne Shorter Narrative |
| 6 | Frisell Atmosphere |
| 7 | Scofield–Holland Groove |
| 8 | Counterpoint Hybrid |
| 9 | Frisell Atmosphere |

**Guidelines:**
- No two consecutive pieces use the same primary engine
- Zappa secondary in ≤ 2 pieces per album
- Alternate tempo and texture contrast

---

## 10. Score Engraving Standards

Every generated score must include:

- **Guitar chord symbols** — above the guitar staff, reflecting actual harmony
- **Boxed rehearsal letters** — A, B, C, D, E, F aligned with first measure of each section
- **Double barlines** — at section changes
- **Tempo marking** — at the beginning
- **Dynamics** — at structural shifts

**Full specification:** `rules/score-readability-standard.md`

---

## 11. MusicXML Validation Rules

Before export, verify:

- **Guitar staff contains music** — not empty, not rest-only
- **Chord symbols use `<harmony>`** — not plain text
- **Rehearsal letters use `<rehearsal>`** — boxed
- **No repeated time signatures** — only in measure 1 and when meter changes
- **Measures balance correctly** — duration matches time signature

**Reject exports if:**
- Guitar part is empty or contains fewer than 4 events per section
- Chord symbols contradict the actual harmony
- Rehearsal marks are missing
- Time signature appears in every measure

**Full specification:** `rules/musicxml-pre-export-validation.md`

---

## 12. Composition Quality Rules (GCE ≥ 9)

Music must reach **GCE ≥ 9** before export.

**Reject pieces that:**
- Repeat harmonic loops excessively
- Lack sectional contrast
- Contain monotony longer than 8 bars

**GCE criteria:** Melodic identity, harmonic clarity, ensemble interaction, voice independence, texture control, emotional resonance.

**Full specification:** `rules/gce-rubric.md`

---

## 13. Repository Structure Rules

Each composition must follow the **one-piece-one-folder** structure.

**Structure:**

```
compositions/
   piece-name/
      musicxml/
      sibelius/
      video/
      audio/
      pdf/
      sketches/
      archive/
      README.md
      revisions.md
      notes.md
```

**Folder naming:** Lowercase with hyphens (e.g. `glass-engine`, `sylva-narrative-no2`).

**Full specification:** `rules/one-piece-one-folder.md`

---

## 14. Synchronization Rule

**Whenever engines or composition rules change:**

Update **BOTH** files:

- `docs/composition_engine_reference.md`
- `docs/composition_engine_reference.docx`

Regenerate the `.docx` from the `.md` using pandoc:

```bash
pandoc docs/composition_engine_reference.md -o docs/composition_engine_reference.docx
```

---

## Reference Locations

| Resource | Path |
|----------|------|
| Four-Engine Album Plan | `docs/album_engine_plan.md` |
| Composition Engine Guide | `docs/Composition_Engine_Guide.md` |
| Album Composition Index | `docs/Album_Composition_Index.md` |
| Engine menu | `prompts/engine_menu.md` |
| Guitar-first rule | `rules/guitar-first-composition-rule.md` |
| Wayne Shorter engine | `rules/wayne-shorter-composition-engine.md` |
| Score readability standard | `rules/score-readability-standard.md` |
| MusicXML pre-export validation | `rules/musicxml-pre-export-validation.md` |
| GCE rubric | `rules/gce-rubric.md` |
| One piece – one folder | `rules/one-piece-one-folder.md` |

---

*This manual is the central rulebook for the composition engine system. Keep it synchronized with all engine and rule changes.*
