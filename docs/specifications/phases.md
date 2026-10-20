# Phases

Deadline: Saturday 24 Oct 2026. Start: Tuesday 20 Oct 2026. Update the status table in memory.md at the end of each day.

## Phase 0. Setup and contracts (Tuesday)

Goal: everyone can start building in parallel.

| Task | Owner |
|---|---|
| Create the folder, virtual environment, requirements.txt, run "hello" Streamlit page | C |
| Copy the folder structure from trd.md with empty files | C |
| Write rules.py from rules.md, justify each weight in a short note | A |
| Write function stubs with fake outputs in the exact contract shape | A, B, C |
| Write test cases from trd.md as failing tests | A, B |

Exit criteria: `streamlit run app.py` opens, `pytest` runs, stubs return the contract shape.

## Phase 1. Core modules (Wednesday)

| Task | Owner |
|---|---|
| analyze_app with scoring, reasons, action. All 6 analyzer tests pass | A |
| scan_text with Luhn, ordered patterns, masking. All 7 DLP tests pass | B |
| store.py with install, wipe, log. MDM console shell with fake module calls | C |

Exit criteria: both module test suites pass. Console runs with stubs.

## Phase 2. Integration (Thursday)

| Task | Owner |
|---|---|
| Swap stubs for real functions in the console | C |
| Install flow with Allow, Review (Approve and Reject) and Block | C, A |
| Send flow with Allow, Mask, Block | C, B |
| Standalone analyzer and scanner pages | A, B |
| Audit log table, never showing raw sensitive values | C |

Exit criteria: the 6-step demo script from prd.md runs end to end.

## Phase 3. Test and report (Friday)

| Task | Owner |
|---|---|
| Run the full demo three times, fix bugs only | All |
| P2 features if time allows: wipe, dashboard, CSV export | C |
| Screenshots of each screen using fake data | C |
| Report draft: problem, architecture, tools, results, limitations | All, one writer per section |
| Each person rehearses a 2-minute explanation of their module | All |

Exit criteria: report drafted, screenshots taken, everyone can explain their part.

## Phase 4. Freeze and submit (Saturday)

- **No new features.** Bug fixes only.
- Final test run, copy the project to a pen drive and a second backup.
- Print what must be printed.
- Do one last demo run on the machine you will present on.

## Cut order if time runs short

1. CSV export
2. Dashboard counts
3. Remote wipe (if the demo script is revised to omit the wipe step)
4. Standalone scanner page polish (keep `scan_text` and its tests)
5. Masking (only if the demo script and acceptance criteria are explicitly revised to demonstrate Block-only behaviour)

Do not silently cut the send flow: it is part of the end-to-end demo. If time forces a cut, update the PRD, demo script, acceptance criteria, and module plans together before changing implementation.

Never cut: the analyzer, the install flow, the audit log.

## Daily check at the end of the day

- Does everything still run with one command?
- Do all tests pass?
- Was memory.md updated?
- Is a working copy saved?
