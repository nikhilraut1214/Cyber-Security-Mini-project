# Rules

Not to be confused with `core/rules.py`. This file holds the working rules for the AI agent and the team, and the scoring rules the code must follow. If this file and the code disagree, fix the code or update this file on purpose, and note it in memory.md.

## Part A. Rules for the AI agent

1. Read prd.md, trd.md, design.md and memory.md before writing code.
2. Show a plan first and wait for approval before large changes.
3. Follow the function contracts in trd.md exactly. Do not rename them.
4. Keep code simple and readable. Short functions, clear names, a comment on the purpose of each function. A second-year student must be able to explain it.
5. Use only the allowed stack. No new packages without asking.
6. Keep all scoring data in `core/rules.py` as plain dictionaries, never inside the logic.
7. Write or update tests with every change. Run them and report the result honestly.
8. Do not add features outside prd.md. Suggest them instead.
9. After each completed task, add a line to the status log in memory.md.
10. Never use real personal data. Test data only.
11. Do not claim something works unless you ran it.

## Part B. Permission scoring rules

Weights (1 is mild, 3 is high concern). These are defaults. Person A owns them and must be able to justify each one.

| Permission | Weight |
|---|---|
| ACCESS_FINE_LOCATION | 3 |
| READ_CONTACTS | 3 |
| RECORD_AUDIO | 3 |
| READ_SMS | 3 |
| READ_CALL_LOG | 3 |
| CAMERA | 2 |
| READ_EXTERNAL_STORAGE | 2 |

Expected permissions per app type (anything else counts as unexpected):

| App type | Expected |
|---|---|
| Flashlight | CAMERA |
| Calculator | none |
| Maps | ACCESS_FINE_LOCATION, READ_EXTERNAL_STORAGE |
| Messaging | READ_CONTACTS, READ_SMS, RECORD_AUDIO, CAMERA |
| Camera | CAMERA, RECORD_AUDIO, READ_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION |
| Game | none |

Score is the sum of weights of requested permissions that are not expected for that app type.

| Score | Level | Action |
|---|---|---|
| 0 | Low | Allow |
| 1 to 3 | Medium | Review |
| 4 or more | High | Block |

Reason text format: `<PERMISSION> is not needed by a <app type> app (weight <n>)`.

## Part C. DLP scanning rules

Check in this order so patterns do not overlap:

| Order | Type | Pattern idea | Extra check |
|---|---|---|---|
| 1 | card | 13 to 16 digits, spaces or dashes allowed | Luhn check must pass |
| 2 | aadhaar_like | 12 digits in groups of 4 | none (dummy data only) |
| 3 | phone | optional +91 or 91, then 10 digits starting 6 to 9 | none |
| 4 | email | standard `name@domain.tld` | none |

Action rule: card or aadhaar_like found means Block. Otherwise phone or email found means Mask. Otherwise Allow.

Masking: replace each matched character with `*`.

Known limits to state: harmless numbers may be flagged, written-out or spaced-out numbers may be missed.

## Part D. Safety and ethics rules

1. Simulation only. Never control a real device or scan a real person's phone.
2. No real personal data anywhere: code, tests, screenshots, report.
3. Label every screen as a simulation.
4. Use "MDM-style" and "DLP-style", never claim to be a real product.
5. Do not build anything that collects or steals data. This tool only checks and warns.

## Part E. Code style rules

- Python naming: `snake_case` for functions and variables, `UPPER_CASE` for constants.
- No function longer than about 40 lines.
- No global mutable state outside `store.py`.
- Messages shown to users are plain English.

## Part F. Team rules

- One shared folder or repository. Commit or copy a working version after every finished task.
- Never edit another person's module without telling them.
- Each person can explain their own module in two minutes.
