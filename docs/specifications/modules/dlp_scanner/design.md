# Design: DLP-style Scanner page

## Layout

```
[Banner: Simulation: not a real MDM or DLP]
Title: DLP Scanner
Short line: Check text before it leaves the device.

Message   [text area]
[Scan]    [Load demo example]

Result card
  Masked and sent        (icon + word + colour)
  Found: 1 phone, 1 email

Masked text
  Call me on **********, mail ****************

Note: Pattern matching can miss disguised numbers and flag harmless ones.
```

## Result card

| Action | Label | Icon | Colour |
|---|---|---|---|
| Allow | Allowed | check mark | green #2E7D32 |
| Mask | Masked and sent | shield | amber #F5A524 |
| Block | Blocked | stop sign | red #C62828 |

Always show the word, not just the colour.

## Findings table

Columns: Type, Count. Never show the matched values.

## Wording

- Empty text: "Type a message to scan."
- Too long: "Text is too long for this demo. Use under 5,000 characters."
- Demo example text uses a clearly labelled synthetic phone number and a published test-only card number (4111 1111 1111 1111); never use real personal data.

## States

- Before first click: only the form.
- After click: result card, findings table and masked text below the form.
