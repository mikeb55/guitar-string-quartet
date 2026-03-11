# MUSICXML ENGRAVING STANDARD

All generated scores must use correct MusicXML element types so notation imports cleanly into Sibelius.

---

## 1. CHORD SYMBOLS

Chord symbols must be written using the MusicXML element:

`<harmony>`

Example structure:

```xml
<harmony>
  <root>
    <root-step>D</root-step>
  </root>
  <kind>major-seventh</kind>
</harmony>
```

Rules:

- chord symbols must appear above the guitar staff
- chord symbols must match the actual harmonic sonority
- avoid writing chord symbols as plain text

**Never use:**

```xml
<direction><words>Dmaj7</words></direction>
```

---

## 2. REHEARSAL MARKS

Section letters must be encoded using:

```xml
<direction>
  <direction-type>
    <rehearsal>A</rehearsal>
  </direction-type>
</direction>
```

Rules:

- Sibelius will automatically box rehearsal letters
- letters must be placed at the first measure of each section
- letters must appear above the system

---

## 3. SECTION BARLINES

Major structural transitions must use:

```xml
<barline location="right">
  <bar-style>light-light</bar-style>
</barline>
```

Do not use plain text for section changes.

---

## 4. TEMPO MARKINGS

Tempo markings must use:

```xml
<direction>
  <direction-type>
    <metronome>...</metronome>
  </direction-type>
</direction>
```

or words + metronome marking.

---

## 5. DYNAMICS

Dynamics must use:

```xml
<direction>
  <direction-type>
    <dynamics>
      <f/>
    </dynamics>
  </direction-type>
</direction>
```

Do not encode dynamics as plain text.

---

## VALIDATION BEFORE EXPORT

Before exporting MusicXML confirm:

- chord symbols use `<harmony>`
- rehearsal marks use `<rehearsal>`
- tempo uses `<metronome>`
- dynamics use `<dynamics>`
- section changes use proper barlines

If any of these appear as plain text objects, regenerate.
