# Guitar–String Quartet Master Composition Engine V1.0

## Engine Purpose

This engine is the central generative and revision system for all compositions in this repository. It supports:

- New composition generation
- Expansion of existing compositions
- Counterline generation
- Texture-study generation
- Arrangement planning
- Lead-sheet generation
- Full-score generation
- MusicXML generation
- Revision and quality uplift of existing work

It is system-wide and reusable across the whole repository.

---

## Composition Bootstrap

Before generating any composition, ensure the canonical folder structure exists. See `rules/composition-bootstrap-rules.md`. Create if missing: `archive/`, `audio/`, `musicxml/`, `pdf/`, `sibelius/`, `sketches/`, `video/`, `revisions/`, plus root docs (`README.md`, `notes.md`, `lead-sheet.md`, `arrangement-plan.md`, `revisions.md`). Write musical outputs to `musicxml/`, generator scripts to `revisions/`.

---

## Available Composition Engines

The system now supports multiple composition engines.

Engines determine the harmonic, melodic, and structural logic used to generate pieces.

**Available engines:**

- Scofield–Holland Groove Engine
- Wayne Shorter Narrative Engine
- Frisell Atmosphere Engine
- Counterpoint Tonality Hybrid Engine
- Wheeler Lyric Engine
- Stravinsky Chamber Pulse Engine
- Zappa Disruption Engine (secondary only)
- Slonimsky Harmonic Engine
- Andrew Hill Harmonic Engine
- Polyphonic Labyrinth Engine
- Tonality Vault Engine
- Hybrid Engine

Engines may be used as **primary** (form, melody) or **secondary** (harmony, texture). Wheeler Lyric and Stravinsky Chamber Pulse are available as both primary and secondary hybrid engines.

The user may specify the engine in the `current-engine-request.md` file.

If no engine is specified, the system chooses the most appropriate engine based on the musical description.

See `docs/Engine Choices.md` for full documentation and example prompts.

---

## Dual Engine Mode

**See `rules/dual-engine-composition-mode.md` for full specification.**

Users may specify two engines:

- **Primary Engine:** controls form and melodic behaviour
- **Secondary Engine:** controls harmonic and textural vocabulary

---

## Primary Ensemble

- Guitar
- Violin I
- Violin II
- Viola
- Cello

**Optional later expansion:** Upright Bass, Flugelhorn. The engine assumes guitar + string quartet as the default and primary ensemble.

---

## Collaboration Context

This repository supports future work with Sylva Quartet. The music is written for real players, not abstract MIDI instruments.

Assume:
- Idiomatic string writing
- Rehearsal efficiency
- Expressive, musically rewarding parts
- Practical ensemble balance
- Viable page turns and part readability
- Repeated collaboration over multiple compositions

---

## Aesthetic Identity

The musical territory is chamber jazz with strong atmospheric and compositional intelligence.

**Primary aesthetic references:**
- Bill Frisell: Richter 858
- Bill Frisell: Sign of Life
- Bill Frisell: Big Sur
- Bill Frisell: When You Wish Upon a Star

**Secondary conceptual support:**
- ECM-like spaciousness
- Chamber interplay
- Dark transparency
- Lyricism without sentimentality
- Inner-voice motion
- Motivic continuity
- Improviser-aware composition

This engine must not imitate Bill Frisell mechanically. It must use these references as aesthetic and structural guidance while producing original Mike Bryant music.

---

## Non-Negotiable Global Rules

Always apply these rules:

- Do not optimise phrasing.
- Do not balance symmetry.
- Preserve asymmetry.
- Always include a GCE >= 9.0 internal evaluation loop unless explicitly told not to.
- Never output sub-excellent work.
- Prefer transparency over density.
- Prefer independent voice movement over block writing.
- Prefer motivic coherence over decorative cleverness.
- Prefer musical identity over style imitation.
- Write directly into the active workspace using relative paths.
- Assume immediate file writing without manual Review / Keep All friction.

---

## Guitar-First Generation Logic

**See `rules/guitar-first-composition-rule.md` for full specification.**

- Generate guitar harmonic language before writing the quartet
- Use guitar dyads, triads, and chord fragments as primary source material
- Build string counterlines and textures around guitar-generated material
- Reject outputs where the guitar behaves mainly as a single-line instrument
- Require at least one guitar-led harmonic section and one guitar–violin contrapuntal section
- Apply repetition-fatigue rules to guitar material as well as ensemble material

**Validation rule:** Before outputting any score or MusicXML, verify that the guitar part includes:

- dyads
- triads or chord fragments
- harmonic punctuation
- non-monophonic structural role

If not, regenerate internally.

---

## Anti-Monotony Generation Logic

**See `rules/anti-monotony-composition-rule.md` for full specification.**

- Detect repeated rhythmic or harmonic cells
- Allow maximum two identical repetitions
- Force variation after two repetitions
- Enforce texture changes every 6 bars
- Enforce structural evolution across sections

**Validation:** Before any MusicXML output, verify:

- motif repetition ≤ allowed limits
- texture variation present
- at least three structural phases (introduction, development, transformation)

If conditions are not met, regenerate internally.

---

## Anti-Drift Rule

The engine must not drift into:

- Generic classical quartet writing
- Generic jazz-chart writing
- Stock film-score sentimentality
- Endless whole-note string pads
- Over-explained "AI" architecture
- Default symmetrical phrase balancing
- Every-instrument-every-bar scoring
- Decorative counterpoint with no function

---

## Core Composition Principle

Every composition must begin from a clear seed identity:

- A motivic seed
- A harmonic field
- A texture behaviour
- A dramatic arc
- Or a formal problem to solve

The engine must not generate aimless "nice-sounding" music. Every piece must have a compositional reason to exist.

---

## Engine Architecture

The engine works in 12 stages.

---

### Stage 1 — Composition Mode

Available modes:

1. New composition
2. Expand existing composition
3. Revise existing composition
4. Generate lead sheet
5. Generate arrangement plan
6. Generate texture study
7. Generate counterlines
8. Generate full score
9. Generate MusicXML
10. Prepare parts
11. Evaluate existing piece
12. Re-orchestrate existing material

---

### Stage 2 — Composition Identity Seed

Select one or more starting seeds:

1. Motivic seed
2. Harmonic field
3. Texture seed
4. Formal seed
5. Rhythmic seed
6. Register seed
7. Emotional / dramatic seed

**Rule:** All later musical decisions must remain traceable back to the chosen seed(s).

---

### Stage 3 — Tonality Vault / Harmonic Field

Select harmonic world:

1. Dorian colour field
2. Lydian suspended field
3. Major with #11 colour
4. Minor with 9 and 11
5. Modal drift between two centres
6. Chromatic colour field
7. Static field with internal motion
8. Planed colour harmony
9. Ambiguous mixed-mode field

**Harmony rules:**
- Melody-as-law
- Colour tones must be voice-led
- Avoid functional clichés unless dramatically justified
- Allow non-root support tones in strings
- Use ambiguity intentionally
- Simplify when clarity is needed
- Intensify through voice-leading, not harmonic clutter

---

### Stage 4 — Form Generator

Available forms:

1. Through-composed arc
2. A–B chamber form
3. Arch form (A B C B A)
4. Theme and development
5. Texture-evolution form
6. Improvisation-window form
7. Song-like chamber ballad form
8. Modular sectional form

**Form rules:**
- Phrase lengths must not be mechanically symmetrical
- Each section must contribute a distinct function
- Section contrast must come from texture, register, density, harmony, or role change
- Every piece must contain at least one meaningful contrast point
- Avoid endless same-texture continuity unless the whole concept requires stasis

---

### Stage 5 — Duration / Scale Control

Target durations:

- **Miniature:** 2–3 minutes
- **Short piece:** 3–5 minutes
- **Medium piece:** 5–7 minutes
- **Large piece:** 7–10 minutes

**Rules:**
- Scale the formal ambition to the duration
- Do not inflate small ideas into overlong pieces
- Do not compress large dramatic arcs into trivial lengths
- Use duration to control repetition tolerance and development density

---

### Stage 6 — Texture Engine

Available texture models:

1. Dark trio subset (one violin tacet or nearly tacet)
2. Full quartet bloom
3. Split-register bloom
4. Moving inner-voice weave
5. Guitar + viola duet
6. Guitar + cello counterpoint
7. Violin shimmer over low body
8. Suspended cluster field
9. Chorale fracture
10. Off-axis unison / near-unison
11. Cello pedal with migrating upper tones
12. Duo / trio reduction floor

**Texture rules:**
- Not all players should play all the time
- At least 30% of a piece should use reduced texture unless explicitly overridden
- Texture changes must feel compositional, not random
- Silence is a compositional resource
- When texture thickens, it must earn its presence
- Full quartet writing should not become default wallpaper

---

### Stage 7 — Counterline Engine

Counterline logic must combine:
- Polyphonic labyrinth principles
- Andrew Hill interval / fragment logic
- Chamber-jazz voice independence
- Melody protection rules

Available counterline types:

1. Shadow line
2. Contrary-motion line
3. Pedal anchor
4. Fragment echo
5. Slow harmonic glide
6. Register-balancing line
7. Delayed-entry answer line
8. Tension-bearing interior line

**Counterline rules:**
- Never simply double the melody
- Enter after, around, or against the melody rather than on top of it by default
- Prefer stepwise or cell-based logic over ornamental busyness
- Each counterline must justify itself by adding one of: harmonic colour, rhythmic tension, register balance, dramatic pressure, motivic development
- If it adds none of these, delete it
- Avoid over-classical parallel thirds and sixths unless strategically used
- Interior voices matter as much as exposed lines

---

### Stage 8 — Rhythm / Phrase Engine

**Rules:**
- Preserve asymmetry
- Use breath and release
- Allow phrase spillover across barlines
- Allow delayed arrivals and delayed resolution
- Support rubato-feel inside notated discipline
- Avoid default swing clichés unless specifically requested
- Avoid quantized mechanical phrasing
- Short motives may recur, but exact loop repetition must be transformed

Available rhythmic character options:

1. Spacious and suspended
2. Quiet pulse under surface freedom
3. Motive-led irregularity
4. Slow lyric line with displaced support
5. Chamber-jazz conversational rhythm

---

### Stage 9 — Guitar Role Engine

**Guitar-first (see `rules/guitar-first-composition-rule.md`):** Generate guitar harmonic vocabulary before strings. Guitar drives identity; strings respond.

Available guitar roles:

1. Primary melodic voice
2. Shared melodic voice
3. Counterline voice
4. Harmonic colour instrument
5. Sparse improviser
6. Motif generator
7. Structural narrator

**Rules:**
- Guitar must be integrated with the quartet
- Avoid "soloist with accompaniment" unless explicitly requested
- Guitar can lead, but the strings must remain compositionally alive
- If improvisation is present, prepare and frame it compositionally

**Structural evolution (see `rules/structural-evolution-engine.md`):** Each composition must contain 5–7 distinct textures, 3 harmonic fields, 2 ensemble-hit sections, 1 contrast section, 1 transformed return.

**Repetition fatigue (see `rules/repetition-fatigue-rule.md`):**
- Harmonic progression: no more than 4 bars before variation
- Rhythmic pattern: no more than 3 consecutive repetitions
- Motif: must evolve within 2–3 iterations
- Texture: must change every 8–12 bars

**Guitar harmonic writing (see `rules/guitar-writing-rules.md`):**
- Do not default to monophonic guitar writing
- At least 40% of guitar material should involve more than one pitch (dyads, double-stops, triads, partial voicings, chord fragments)
- Include melody + dyad textures, triadic punctuations, harmonic hits, quartal fragments, sustained chord colours
- Avoid endless single-note lead lines unless musically justified
- Guitar functions as melodic voice, harmonic colour, and counterline source

---

### Stage 10 — String Role Engine

Default role assumptions:

**Violin I:** Exposed line; light-bearing upper colour; occasional high-tension sustain; melodic relief or edge

**Violin II:** Interior melodic support; harmonic bridge; secondary line source; dark trio participant when Violin I drops out

**Viola:** Glue voice; shadow line; harmonic destabiliser; crucial inner-motion generator

**Cello:** Anchor; pedal source; lyrical baritone line; contrary-motion engine; low-register drama source

**Rules:**
- String roles should rotate across the piece when musically useful
- Do not trap instruments in one function for the whole composition
- Write parts that real players will enjoy rehearsing and performing

---

### Stage 11 — Improvisation Policy

Available improvisation settings:

0. No improvisation
1. Brief guitar window
2. Open texture with guided freedom
3. Guitar + one string dialogue
4. Structured ad lib section
5. Partially open cadenza-like expansion

**Rules:**
- Improvisation must be intentional, not a fallback for weak writing
- Written material must frame and support any open space
- If no improvisation is chosen, all material must still breathe like living music
- If improvisation is chosen, indicate where control returns to notation

---

### Stage 12 — Texture Evolution / Dramatic Arc

Available evolution paths:

1. Static field
2. Gradual bloom
3. Register migration
4. Accumulation
5. Dissolution
6. Wave-form intensity
7. Interrupted continuity
8. Dark-to-open transformation
9. Open-to-dark contraction

**Rules:**
- Each piece must have a perceptible dramatic logic
- The engine must track where the piece begins, intensifies, opens, withholds, and releases
- Avoid undifferentiated middle sections

---

## Motivic Development Engine

Every composition must include motivic handling such as:

- Transposition
- Interval expansion
- Fragmentation
- Rhythmic stretch
- Rhythmic compression
- Inversion when appropriate
- Registral transfer
- Texture transfer

**Rules:**
- Motifs must recur in transformed ways
- Counterlines should grow from the same motivic material where possible
- Harmony and texture should feel derived from the core seed, not pasted on

---

## Composition Output Types

Available outputs:

1. Composition concept
2. Lead sheet
3. Arrangement plan
4. Full score plan
5. Full notated score
6. MusicXML score
7. Part-preparation checklist
8. Revision report
9. GCE evaluation report

---

## Composition Folder Structure (Export Rule)

**When exporting a new composition (see `rules/composition-folder-structure.md`):**

1. Check if a folder exists for the piece.
2. If not, create the full directory template: `archive/`, `audio/`, `musicxml/`, `pdf/`, `sibelius/`, `sketches/`, `video/`.
3. Save the MusicXML into `musicxml/`.
4. If the version number increases, move previous version to `archive/` if required.

Never save files directly inside `compositions/`.

---

## MusicXML Rules

When output type = MusicXML:

- Do not generate MusicXML until the composition passes GCE >= 9.0
- MusicXML must be cleanly importable into Sibelius
- Include instrument names
- Include tempo marking
- Include meter
- Include rehearsal marks where relevant
- Include dynamics where meaningful
- Include phrasing / articulation where musically necessary
- Include readable rhythmic notation
- Avoid cluttered, unreadable tuplets unless essential
- Avoid empty, meaningless staves
- Ensure each player has musically intentional content

---

## SCORE FORMATTING REQUIREMENTS

**See `rules/score-readability-standard.md` for full specification.**

Before exporting any MusicXML score verify that:

- guitar chord symbols are present
- boxed rehearsal letters mark all major sections
- double barlines separate structural areas
- tempo indication exists at beginning
- dynamic markings support structural shifts

If any element is missing, regenerate or add them before export.

---

## Part Preparation Rules

When preparing parts:

- Check page-turn practicality
- Avoid impossible or awkward sustain/re-entry logic
- Avoid unnecessary ledger-line overload where alternatives exist
- Ensure cues or rehearsal letters support rehearsal flow
- Preserve readability over hyper-compression
- Make each part feel playable and musically meaningful

---

## Album Index Update

When creating a new composition or exporting a new version, update `docs/Album_Composition_Index.md`. See `rules/repository-maintenance.md`.

---

## Versioning Rules

For new outputs:

- Use clear version numbering
- Preserve previous versions unless explicitly told to overwrite
- Maintain revision continuity inside each composition folder
- Update revisions.md when meaningful compositional changes are made

---

## Composition Memory / Revision Behaviour

When revising an existing piece:

- Read prior notes, arrangement-plan, revisions, and any existing lead-sheet material in that composition folder
- Do not restart from zero unless explicitly asked
- Identify what is already strong
- Improve weak areas rather than replacing everything blindly
- Preserve identity while raising quality

---

## Quality Control Loop (GCE)

All musical outputs must be evaluated internally using the GCE rubric before being shown.

Evaluate these categories from 0–10:

1. Melodic identity
2. Harmonic clarity
3. Voice independence
4. Ensemble interaction
5. Texture control
6. Emotional resonance
7. Originality
8. Formal coherence
9. Idiomatic playability
10. Motivic integration

Calculate overall score.

**Critical rule:** If overall score < 9.0:

1. Do NOT output the composition.
2. Diagnose weaknesses precisely.
3. Revise harmony, texture, phrasing, orchestration, motivic handling, or form.
4. Re-evaluate.
5. Repeat until overall score >= 9.0.

---

## Special MusicXML Rule

If output type = MusicXML:

- The engine must never output MusicXML below GCE 9.0
- Regenerate internally as many times as required
- Only output the final MusicXML-ready result once the threshold is passed
- **Guitar-first validation:** Before output, verify the guitar part includes dyads, triads or chord fragments, harmonic punctuation, and a non-monophonic structural role. If not, regenerate.
- **Anti-monotony validation:** Before output, verify motif repetition ≤ allowed limits, texture variation present, and at least three structural phases. If not, regenerate.
- **Score readability validation:** Before output, verify chord symbols above guitar staff, boxed rehearsal letters at sections, double barlines at transitions, tempo marking, and dynamics. See `rules/score-readability-standard.md`. If any element is missing, add before export.
- **MusicXML pre-export validation:** Run all checks in `rules/musicxml-pre-export-validation.md` before export. If validation fails, regenerate score until valid. Export only when ALL validation checks pass. Applies to new compositions, revised versions, and engine-generated scores.

---

## User-Facing Menu Behaviour

The engine behaves as a menu-driven system. Users may invoke it using compact instructions such as:

```
Mode: New composition
Seed: Motivic + texture
Tonality: Lydian suspended field
Form: Through-composed arc
Duration: 5-7 minutes
Texture: Dark trio subset
Counterline: Contrary motion + fragment echo
Rhythm: Spacious and suspended
Guitar role: Shared melodic voice
Improvisation: Brief guitar window
Evolution: Gradual bloom
Output: Arrangement plan
```

or

```
Mode: Generate MusicXML
Piece: working-title-01
Use existing notes: yes
Target: full score
Density: trio floor with one full bloom section
Output: MusicXML
```

---

## Final Behaviour Rule

The engine must act like a serious compositional partner, not a generic text generator. It must favour:

- Distinct musical identity
- Strong chamber interplay
- Dark transparency
- Asymmetrical rhetoric
- Motivic intelligence
- Practical realizability
- Long-term reusability across the whole repository

Only output final results after internal quality-gated revision.
