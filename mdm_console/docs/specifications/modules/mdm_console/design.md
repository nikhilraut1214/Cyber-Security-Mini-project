# Design: MDM Console

## Home page (`app.py`)

```
[Banner: Simulation: not a real MDM or DLP]
Title: Mobile Data Leakage Prevention Console
Two lines explaining the project.

Counts:  Apps blocked [n]   Messages masked [n]   Messages blocked [n]

Audit log (latest first)
| Time | Event | Detail | Result |
```
Empty log text: "No events yet. Try installing an app."

## Console page (`pages/1_MDM_Console.py`)

```
[Banner: Simulation: not a real MDM or DLP]
Title: MDM Console
+---------------------------+  +--------------------------------------+
| Device: Student Phone     |  | Install an app                       |
| Status: Active            |  | App name   [____________]            |
| Installed apps:           |  | App type   [Flashlight v]            |
|  - Calculator             |  | Permissions [multiselect]            |
| [Lost phone]              |  | [Check and install] [Load demo]      |
+---------------------------+  | Result card                          |
                               | (Review: [Approve] [Reject])         |
                               +--------------------------------------+
                               | Send a message                       |
                               | [text box]  [Check and send]         |
                               | Result card                          |
                               +--------------------------------------+
Audit log
```

## Result cards

| Action | Label | Icon | Colour |
|---|---|---|---|
| Allow | Allowed | check mark | green #2E7D32 |
| Review | Needs review | warning sign | amber #F5A524 |
| Block | Blocked | stop sign | red #C62828 |
| Mask | Masked and sent | shield | amber #F5A524 |

Always show the word, not just the colour.

## States

- **Wiped:** show "This device was wiped. Re-enrol it to continue." Disable install and send. Show a Re-enrol button.
- **Empty device:** "No apps installed."
- **Invalid input:** friendly message in a red box.

## Style

Match the video deck: dark navy #0B1F3A for headings, amber #F5A524 accent, light background #F1F4F9, text #1B2B44. Streamlit default sans-serif font.

## Demo helpers

"Load demo" buttons fill the flashlight example with CAMERA, ACCESS_FINE_LOCATION and READ_CONTACTS, and a message with a clearly labelled synthetic phone number and the published test-only card number 4111 1111 1111 1111; never use real personal data.
