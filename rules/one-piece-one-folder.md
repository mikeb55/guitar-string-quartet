# ONE PIECE – ONE FOLDER RULE

Each composition must have exactly one canonical folder.

All versions and related assets must remain inside that folder.

---

## CANONICAL STRUCTURE

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

---

## FOLDER NAMING

Folder names must use lowercase and hyphens.

Examples:

- glass-engine
- sylva-narrative-no2
- eviscerating-angels
- drift-study-no1

Do not create multiple folders for versioned files.

---

## VERSION NAMING RULE

All new compositions must follow version naming.

**Format:** `V{number}_{title}.musicxml`

**Rules:**
- Never overwrite earlier versions
- Increment version number for every revision
- Store all versions inside the same piece folder

**Example:**

```
musicxml/
   V1_Home_Engine_Scofield.musicxml
   V2_Home_Engine_Scofield.musicxml
   V3_Home_Engine_Scofield.musicxml
```

Older versions must never be overwritten.

---

## LATEST VERSION RULE

The latest version of each piece should be clearly identifiable.

Optionally create:

`latest.musicxml`

pointing to the newest version.

---

## FILE PLACEMENT RULES

| Extension | Destination |
|-----------|-------------|
| .musicxml, .xml | musicxml/ |
| .sib | sibelius/ |
| .mp4, .mov, .wmv | video/ |
| .wav, .mp3, .flac | audio/ |
| .pdf | pdf/ |
| .mid, .txt | sketches/ |

---

## README CONTENT

Each piece folder must contain README.md describing:

- piece title
- engine used
- tonal center
- current latest version
- notes about revisions

---

## REVISIONS LOG

Each piece must include revisions.md recording:

- version number
- change summary
- date
