# MusicXML Generation Template

Use when generating MusicXML for guitar and string quartet compositions.

**Final Pass mode:** When in FINAL PASS, plan full structure first, verify harmony and orchestration internally, apply engraving rules, validate MusicXML, and export only when GCE ≥ 9.5. Do not emit intermediate drafts. See `rules/final-pass-generation-mode.md`.

**Guitar-first rule applies:** Generate guitar harmonic material first; build strings around it. See `rules/guitar-first-composition-rule.md`.

**Score readability standard applies:** All scores must follow professional rehearsal chart standards. See `rules/score-readability-standard.md`.

**MusicXML engraving standard applies:** Use correct element types for chord symbols, rehearsal marks, tempo, and dynamics. See `rules/musicxml-engraving-standard.md`.

## Pre-Generation Checklist

- [ ] Lead sheet complete (melody, chords, form)
- [ ] Arrangement plan complete (texture, roles, dynamics)
- [ ] Score readability standard reviewed (`rules/score-readability-standard.md`)
- [ ] Engraving rules reviewed (`rules/engraving-rules.md`)
- [ ] MusicXML engraving standard reviewed (`rules/musicxml-engraving-standard.md`)
- [ ] MusicXML pre-export validation reviewed (`rules/musicxml-pre-export-validation.md`)
- [ ] Guitar-first rule reviewed (`rules/guitar-first-composition-rule.md`) — guitar harmonic vocabulary generated before strings
- [ ] Guitar writing rules reviewed (`rules/guitar-writing-rules.md`) — guitar parts include dyads, triads, harmonic colour; ≥40% polyphonic
- [ ] Anti-monotony rule reviewed (`rules/anti-monotony-composition-rule.md`)

## Anti-Monotony Check

Confirm:

- [ ] Motifs evolve (max 2 identical, max 3 with variation)
- [ ] Guitar gestures vary (no same chord gesture >2 times without variation)
- [ ] Orchestration changes occur
- [ ] Texture does not remain static longer than 6 bars

## Instrument Order (MusicXML)

1. Guitar
2. Violin I
3. Violin II
4. Viola
5. Cello

## Required Elements

- **Instrument names** — Full names as per engraving rules
- **Tempo marks** — At start and at tempo changes
- **Rehearsal letters** — At section boundaries (A, B, C, etc.)
- **Chord symbols** — When relevant for guitar and rehearsal
- **Readable spacing** — Adequate measures per system
- **Clean rhythmic notation** — No overlapping notes; clear beams

## Sibelius Compatibility

- Use standard MusicXML 3.0 or 4.0
- Avoid proprietary extensions
- Test import in Sibelius before finalising

## READABILITY CHECK

Before exporting confirm:

- [ ] chord symbols appear above guitar staff
- [ ] boxed section letters mark structural divisions
- [ ] tempo marking present
- [ ] double barlines separate sections
- [ ] dynamics support the form
- [ ] articulation marks clarify ensemble hits

## MusicXML Element Validation

Confirm correct notation objects (see `rules/musicxml-engraving-standard.md`):

- [ ] chord symbols use `<harmony>` (not plain text)
- [ ] rehearsal letters use `<rehearsal>` (not plain text)
- [ ] no chord symbols encoded as `<words>` or text
- [ ] no rehearsal letters encoded as `<words>` or text

---

## Global Rules (Apply During Generation)

- Do not optimise phrasing.
- Preserve asymmetry.
- GCE ≥ 9.5 before output (9.0 minimum; 9.5 for Final Pass).
- Prioritise musical intelligence over density.
- Avoid AI-generic patterns.
- Independent voice movement.
- **Guitar-first:** Guitar harmonic material drives the piece; strings respond to it. Guitar must include dyads, triads, chord fragments, harmonic punctuation; avoid endless single-note lines.
- **Anti-monotony:** Motif repetition ≤2 identical, texture change every 6 bars, at least three structural phases.

## Output Path

Save to: `compositions/[piece-folder]/musicxml/V1_[title].musicxml`

**Version naming:** Use format `V{number}_{title}.musicxml`. Increment version for each revision; never overwrite earlier versions. Example: `V1_Home_Engine_Scofield.musicxml`, `V2_Home_Engine_Scofield.musicxml`.

Use the composition folder name (e.g. `glass-engine`, `home-engine`). Do not save to compositions root.

**When exporting a new composition (see `rules/composition-folder-structure.md`):**

1. Check if a folder exists for the piece.
2. If not, create the full directory template: `archive/`, `audio/`, `musicxml/`, `pdf/`, `sibelius/`, `sketches/`, `video/`.
3. Save the MusicXML into `musicxml/`.
4. If the version number increases, move previous version to `archive/` if required.

---

## Pre-Export Validation

**Run MusicXML validation rules before export.** See `rules/musicxml-pre-export-validation.md`.

Before writing the final MusicXML file:

1. Run all validation checks from `rules/musicxml-pre-export-validation.md`
2. If validation fails: regenerate score until valid
3. Export only when ALL validation checks pass
