# Rules: Permission Risk Analyzer

## Part A. Rules for the AI agent (this module)

1. Read this module's prd.md, trd.md, design.md and memory.md first, then the main trd.md for the shared contracts.
2. Show a plan before coding and wait for approval.
3. Keep all data in `core/rules.py`. No weights or app types inside the logic.
4. Do not change the `analyze_app` signature or output keys.
5. Write the tests first, run them, report the real result.
6. Keep the code short and commented so a student can explain it.
7. No new packages, no network calls, no real app data.
8. Update memory.md after each finished task.

## Part B. Scoring rules

| Permission | Weight |
|---|---|
| ACCESS_FINE_LOCATION | 3 |
| READ_CONTACTS | 3 |
| RECORD_AUDIO | 3 |
| READ_SMS | 3 |
| READ_CALL_LOG | 3 |
| CAMERA | 2 |
| READ_EXTERNAL_STORAGE | 2 |

| App type | Expected permissions |
|---|---|
| Flashlight | CAMERA |
| Calculator | none |
| Maps | ACCESS_FINE_LOCATION, READ_EXTERNAL_STORAGE |
| Messaging | READ_CONTACTS, READ_SMS, RECORD_AUDIO, CAMERA |
| Camera | CAMERA, RECORD_AUDIO, READ_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION |
| Game | none |

| Score | Level | Action |
|---|---|---|
| 0 | Low | Allow |
| 1 to 3 | Medium | Review |
| 4 or more | High | Block |

## Part C. Change control

- If a weight or an expected permission changes, update the tests and write one line in the justification note: what changed and why.
- Person A writes the justification in their own words. These are defaults, not facts from a standard.

## Part D. Justification note (Person A fills this in)

For each weight, write one sentence on why it is 2 or 3. Example: "READ_SMS is 3 because messages can contain one-time passwords and private conversations."
