# Composition Folder Structure

All compositions must follow the canonical directory structure.

---

## When a New Composition is Created

1. Create a folder using kebab-case title.
2. Inside create:

   ```
   archive/
   audio/
   musicxml/
   pdf/
   sibelius/
   sketches/
   video/
   ```

3. Save files according to type:

   | File Type | Destination |
   |-----------|-------------|
   | MusicXML | musicxml/ |
   | Sibelius | sibelius/ |
   | Exported PDF | pdf/ |
   | Audio bounce | audio/ |
   | Video render | video/ |
   | Draft ideas | sketches/ |
   | Old versions | archive/ |

4. Never save files directly inside `compositions/`.

---

## Canonical Structure

```
compositions/
    composition-name/
        archive/
        audio/
        musicxml/
        pdf/
        sibelius/
        sketches/
        video/
```

---

## Related Rules

- `rules/one-piece-one-folder.md` — One piece per folder, version naming, file placement
- `rules/repository-maintenance.md` — Version naming, index updates
