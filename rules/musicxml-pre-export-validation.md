# MUSICXML PRE-EXPORT VALIDATION

Before exporting any MusicXML score the generator must verify the following.

---

## PART STRUCTURE

The score must contain exactly these parts:

- Guitar
- Violin I
- Violin II
- Viola
- Cello

If any part is missing, regenerate.

---

## GUITAR CONTENT

The guitar staff must contain actual musical material.

**Reject the export if:**

- the guitar part contains only rests
- the guitar part is empty
- the guitar part contains fewer than 4 events per section

**Ensure the guitar contains:**

- dyads
- triads or chord fragments
- harmonic role in the ensemble

---

## TIME SIGNATURE RULE

Time signature must appear:

- only in the first measure
- again only when meter actually changes

Reject exports where the time signature appears in every measure.

---

## KEY SIGNATURE RULE

Key signature must appear:

- only when it changes

Reject exports where the key signature repeats unnecessarily.

---

## CHORD SYMBOL VALIDATION

Chord symbols must:

- be encoded using `<harmony>`
- match the actual sounding harmony

**Reject exports if:**

- chord symbols are written as text
- chord symbol says major but chord is minor
- chord symbol says minor but chord is major

---

## REHEARSAL MARKS

Every section must contain a rehearsal letter.

Use MusicXML:

```xml
<rehearsal>
```

Letters must be:

A, B, C, D, etc.

Reject export if rehearsal marks are missing.

---

## MEASURE BALANCE

Each measure must contain correct rhythmic duration.

Reject exports if measures do not balance.

---

## SECTION STRUCTURE

Ensure the score contains:

- multiple sections
- rehearsal marks
- double barlines at structural transitions

Reject exports if the piece is a single unbroken texture.

---

## ANTI-MONOTONY CHECK

Reject exports if:

- harmonic loop repeats more than twice
- identical rhythmic pattern repeats more than twice
- orchestration remains unchanged longer than 6 bars

---

## FINAL EXPORT CONDITION

MusicXML export is allowed only if ALL validation checks pass.

If any rule fails:

**regenerate internally until the score passes validation.**
