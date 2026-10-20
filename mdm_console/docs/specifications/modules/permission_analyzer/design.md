# Design: Permission Risk Analyzer page

## Layout

```
[Banner: Simulation: not a real MDM or DLP]
Title: Permission Risk Analyzer
Short line: Check what an app asks for against what it needs.

App type      [Flashlight v]
Permissions   [multiselect: ACCESS_FINE_LOCATION, READ_CONTACTS, ...]
[Analyze]     [Load demo example]

Result card
  Needs review        (icon + word + colour)
  Risk level: Medium    Score: 3
  Why:
   - ACCESS_FINE_LOCATION is not needed by a Flashlight app (weight 3)

Note: Permissions alone do not prove data leakage.
```

## Result card

| Action | Label | Icon | Colour |
|---|---|---|---|
| Allow | Allowed | check mark | green #2E7D32 |
| Review | Needs review | warning sign | amber #F5A524 |
| Block | Blocked | stop sign | red #C62828 |

Always show the word, not just the colour.

## Wording

- Empty permissions: "No permissions selected. This is valid and scores 0."
- Error: "Please choose an app type."
- Demo example fills Flashlight with CAMERA, ACCESS_FINE_LOCATION and READ_CONTACTS.

## States

- Before first click: show only the form.
- After click: show the result card below the form.
