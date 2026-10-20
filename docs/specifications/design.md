# Design

## 1. Principles

- Simple and readable. A first-time viewer understands each screen in 10 seconds.
- Never rely on colour alone. Every risk level has a word and an icon too.
- Every page shows the banner: "Simulation: not a real MDM or DLP".
- Plain English text, no jargon without a short explanation.

## 2. Pages

| Page | Purpose |
|---|---|
| Home (`app.py`) | Short explanation, summary counts, audit log table |
| 1 MDM Console | Simulated phone, install app, send message, lost phone |
| 2 Permission Analyzer | Standalone check of one app |
| 3 DLP Scanner | Standalone check of one text |

## 3. Wireframes

### 1 MDM Console
```
[Banner: Simulation: not a real MDM or DLP]
Title: MDM Console
+---------------------------+  +--------------------------------------+
| Device: Student Phone     |  | Install an app                       |
| Status: Active            |  | App name   [____________]            |
| Installed apps:           |  | App type   [Flashlight v]            |
|  - Calculator             |  | Permissions [x] CAMERA  [ ] ...      |
|  - ...                    |  | [Check and install]                  |
| [Lost phone]              |  | Result card: level, reasons, action  |
+---------------------------+  | (Review: [Approve] [Reject])         |
                               +--------------------------------------+
                               | Send a message                       |
                               | [text box]   [Check and send]        |
                               | Result card: findings, action        |
                               +--------------------------------------+
Audit log (latest first)
```

### 2 Permission Analyzer
App type dropdown, permission checkboxes, "Analyze" button, result card, note "Permissions alone do not prove data leakage."

### 3 DLP Scanner
Text area, "Scan" button, result card with finding types and counts, masked text shown below.

## 4. Result cards

| Action | Label | Icon | Colour |
|---|---|---|---|
| Allow | Allowed | check mark | green |
| Review | Needs review | warning sign | amber |
| Block | Blocked | stop sign | red |
| Mask | Masked and sent | shield | amber |

Card content: the action word first, then the level or finding types, then the reasons as a short list.

## 5. Colours and type

Match the video deck.

| Use | Colour |
|---|---|
| Primary dark | #0B1F3A |
| Accent | #F5A524 |
| Text | #1B2B44 |
| Light background | #F1F4F9 |
| Success | #2E7D32 |
| Danger | #C62828 |

Use Streamlit's default sans-serif font.

`.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#F5A524"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1F4F9"
textColor = "#1B2B44"
```

## 6. Audit log table

Columns: Time, Event (Install, Send, Wipe, Approve, Reject), Detail, Result. Latest row on top. For Send events, Detail shows finding types and counts only, for example "1 phone, 1 email". Never the raw value.

## 7. Wording

| Place | Text |
|---|---|
| Analyzer note | Permissions alone do not prove data leakage. |
| Empty log | No events yet. Try installing an app. |
| Wiped device | This device was wiped. Re-enrol it to continue. |
| Too long text | Text is too long for this demo. Use under 5,000 characters. |

## 8. States

- **Empty:** no apps installed, no log rows. Show a one-line hint.
- **Error:** invalid input gives a friendly message in a red box.
- **Wiped:** install and send are disabled until the device is re-enrolled.

## 9. Demo mode

Add a small "Load demo example" button on each input screen that fills in the flashlight example and the sample message, so the demo never depends on typing.
