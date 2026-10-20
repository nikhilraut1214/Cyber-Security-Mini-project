# Project memory

Working memory for the team and the AI agent. Read this first every session. Update it after every finished task.

## Project facts

- **Name:** Mobile Data Leakage Prevention Console
- **Course:** Cyber Security, second-year Computer Science
- **Related work:** group video "Your Flashlight App Is Watching You" on the same topic, with a 4-slide PPT
- **Team:** Person A, Person B, Person C (replace with real names)
- **Deadline:** Saturday 24 Oct 2026
- **Stack:** Python, Streamlit, pytest, no network
- **Real case used in the story:** FTC action on Brightest Flashlight Free (announced Dec 2013, final order Apr 2014)

## Decisions

| ID | Date | Decision |
|---|---|---|
| D1 | 2026-10-20 | Build one Streamlit app. The MDM console is the hub and calls the analyzer and the DLP scanner as functions. |
| D2 | 2026-10-20 | Modules: Permission Risk Analyzer (A), DLP-style scanner (B), MDM console and audit log (C). |
| D3 | 2026-10-20 | Everything is simulated. No real devices, no real personal data. |
| D4 | 2026-10-20 | Function contracts in trd.md are frozen. Changes need all three to agree. |
| D5 | 2026-10-20 | Weights and thresholds in rules.md are defaults. Person A may change them and must justify changes in the report. |
| D6 | 2026-10-20 | Cut order if time runs out: CSV export, dashboard counts, remote wipe (and remove the wipe demo step if cut), standalone scanner page polish, then masking only if the demo/acceptance criteria are explicitly revised. Preserve the end-to-end send flow, analyzer, install flow, audit log, and automated tests unless the team formally revises scope. |
| D7 | 2026-10-20 | store.py functions take a `state` argument so they can be tested with a plain dict. |

## Ownership

| Area | Owner |
|---|---|
| core/rules.py, core/analyzer.py, tests/test_analyzer.py | Person A |
| core/dlp.py, tests/test_dlp.py | Person B |
| core/store.py, app.py, pages/, design | Person C |

## Status log

Add one line per finished task: `YYYY-MM-DD | person | what was done | tests passing?`

| Date | Person | Done | Tests |
|---|---|---|---|
| 2026-10-20 | Team | Core modules (analyzer, DLP scanner, store), three pages and home page built | 27 passed |
| 2026-10-20 | Team | Review: all demo steps ran headless; found 7 issues (see Fixed issues) | 27 passed |
| 2026-10-20 | Team | Fixed demo buttons, form defaults, app-name rule, DLP formats, `pytest` import path; added page tests | 48 passed |

## Phase status

| Phase | Status |
|---|---|
| 0 Setup and contracts | Done |
| 1 Core modules | Done |
| 2 Integration | Done |
| 3 Test and report | In progress (screenshots, report, rehearsal) |
| 4 Freeze and submit | Not started |

## Known issues (open limits, state in the report)

- 12-digit ID-like numbers with no separators are not detected.
- Phone numbers in other layouts (for example 5 + 5 digits with different spacing) can be missed.
- State resets when the page reloads.
- Approving a Review app writes two log rows: Install and Approve.

## Fixed issues (2026-10-20)

- "Load demo example" buttons on the console and analyzer pages did nothing; they now fill the form.
- Form defaults depended on the app type inside a form; the widgets now use session_state keys.
- App-name rules differed between page and store; both use `store.validate_app_name`.
- Hyphenated 12-digit IDs and phones written as `+91 98765 43210` were missed; now detected.
- Plain `pytest -q` failed to import `core`; `pytest.ini` fixes it.

## Open questions

- What must be submitted besides the demo?
- Is Python allowed?
- Where will the demo run?

## Glossary

- **MDM:** Mobile Device Management. Lets administrators control apps and settings on phones and wipe a lost phone.
- **DLP:** Data Loss Prevention. Detects and blocks sensitive data leaving a device.
- **Luhn check:** a simple formula that tells whether a card-like number is plausibly valid.
- **Audit log:** a record of every decision the console made.
- **Simulation:** nothing here controls a real phone.
