# Engine Library Link

This project uses the **global composition engine system** located at:

**Library path:**  
`C:\Users\mike\Documents\Cursor AI Projects\composition-engine-library`

---

## Purpose

All composition prompts in this project should reference engines from this global library. The library provides:

- **10 composition engines** — instrumentation-agnostic definitions
- **Master composition prompt** — engine selection, GCE evaluation, regeneration rules
- **GCE quality rules** — minimum score 9.0, anti-monotony, asymmetry
- **Engine selection template** — reusable for all projects

---

## Usage

1. **Engine definitions:** Read from `composition-engine-library/engines/*.md`  
2. **Composition prompts:** Reference `composition-engine-library/prompts/master_composition_prompt.md`  
3. **Quality rules:** Apply `composition-engine-library/rules/gce_quality_rules.md`  
4. **Engine selection:** Use `composition-engine-library/templates/engine_selection_template.md`  

---

## Project-Specific Adaptation

This project (guitar-string-quartet) maps the global engines to:

- **Guitar** — harmonic engine, melodic voice, counterline
- **Violin I** — primary melodic
- **Violin II** — secondary melodic / harmonic colour
- **Viola** — inner voice
- **Cello** — bass anchor

The engine *definitions* are global; the *instrumentation mapping* is project-specific.

---

## Library Location

```
C:\Users\mike\Documents\Cursor AI Projects\composition-engine-library\
    engines/
    prompts/
    templates/
    docs/
    rules/
```

---

*Do not duplicate engine definitions. Reference the global library.*
