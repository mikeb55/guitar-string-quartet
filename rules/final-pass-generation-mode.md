# Final Pass Generation Mode

When creating a composition in **FINAL PASS** mode, follow this workflow.

---

## Workflow

1. **Plan full structure first** — Form, sections, harmonic progression, orchestration roles
2. **Verify harmony and orchestration internally** — Before writing notes, confirm chord symbols match intended harmony; confirm all five parts have meaningful material
3. **Apply engraving rules** — Chord symbols (`<harmony>`), boxed rehearsal letters (`<rehearsal>`), double barlines, tempo, dynamics
4. **Validate MusicXML** — Run all checks in `rules/musicxml-pre-export-validation.md`
5. **Export only when GCE ≥ 9.5** — Do not export below threshold

---

## Rule

**Do not emit intermediate drafts.**

Generate once, validate, and export only when the piece meets all criteria.

---

## References

- GCE rubric: `rules/gce-rubric.md`
- MusicXML validation: `rules/musicxml-pre-export-validation.md`
- Score readability: `rules/score-readability-standard.md`
- MusicXML generation template: `prompts/musicxml-generation-template.md`
