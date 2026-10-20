# Rules: MDM Console

## Part A. Rules for the AI agent (this module)

1. Read this module's prd.md, trd.md, design.md and memory.md first, then the main trd.md for the shared contracts.
2. Show a plan before coding and wait for approval.
3. Never put analyzer or DLP logic in the console. Call `analyze_app` and `scan_text` only.
4. Never log or display raw sensitive values. Counts and types only.
5. All state changes go through `store.py`. No loose session_state edits in pages.
6. Show the banner "Simulation: not a real MDM or DLP" on every page.
7. Write tests for store.py first. Run them and report the real result.
8. Keep the code short and commented. No new packages, no network calls.
9. Update memory.md after each finished task.

## Part B. Decision rules

| Analyzer action | Console behaviour |
|---|---|
| Allow | Install and log |
| Review | Ask for Approve or Reject |
| Block | Do not install, log with the score |

| Scanner action | Console behaviour |
| --- | --- |
| Allow | Send unchanged |
| Mask | Send the masked text |
| Block | Do not send |

## Part C. Audit log rules

- One row per event. Latest first.
- Events: Install, Send, Wipe, Approve, Reject, Re-enrol.
- Detail holds the app name and type, or finding counts. Never the message.
- The log is cleared only when the page reloads.

## Part D. Safety rules

1. Simulation only. Never control a real device.
2. Fake data only in screenshots and the report.
3. Say "MDM-style", never claim to be a real MDM.

## Part E. Priority rules if time is short

Cut in this order: CSV export, dashboard counts, remote wipe (and remove its demo step if cut), standalone scanner page polish, then masking only after the demo and acceptance criteria are explicitly revised. Preserve the end-to-end send flow, install flow, audit log, and tests unless the team formally revises scope.
