# Repository Maintenance Rules

## Album Composition Index

**See `docs/Album_Composition_Index.md`.**

Whenever a new composition is created or a new version is exported:

1. **Create its folder** in `compositions/` (if new)
2. **Detect its title** from README.md or folder name
3. **Detect key signature** from MusicXML (`<fifths>`) or lead-sheet when possible
   - If ambiguous or modal, mark: **modal / ambiguous**
4. **Detect latest version** — highest version number in `musicxml/` folder
   - e.g. V3Eviscerating_Angels.musicxml > V2Eviscerating_Angels.musicxml
5. **Append or update entry** in `docs/Album_Composition_Index.md`

**If the title already exists:** Update the version and any changed fields (key, tempo, etc.) rather than creating a new row.

**Sort order:** Alphabetically by composition title.

---

## Engine Column Standard

Use only these engine names:

- Frisell Atmosphere
- Slonimsky Harmonic
- Andrew Hill
- Wayne Shorter
- Tonality Vault
- Counterpoint
- Hybrid

**Dual Engine:** Primary + Secondary (e.g. Wayne Shorter + Frisell Atmosphere)

---

## Optional Columns

Include when available:

- **Mood** — e.g. "Dark, tense", "Floating, spacious"
- **Tempo** — e.g. "q = 76"

---

## Integration with Organiser

Run `py scripts/organise-compositions.py` to:

- Move loose composition files into correct folders
- Create missing composition folders and subfolders
- Update `compositions/_index.md`

After running the organiser, **manually update** `docs/Album_Composition_Index.md` if new compositions or versions were added, or extend the organiser script to update the album index automatically.
