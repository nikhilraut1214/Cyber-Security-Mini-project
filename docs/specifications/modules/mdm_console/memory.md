# Memory: MDM Console

## Facts

- Owner: Person C
- Part of the Mobile Data Leakage Prevention Console, deadline Saturday 24 Oct 2026
- Hub that calls the Permission Risk Analyzer (Person A) and the DLP-style scanner (Person B)
- Stack: Python, Streamlit, pytest

## Decisions

| ID | Date | Decision |
|---|---|---|
| M-D1 | 2026-10-20 | store.py functions take a `state` argument so they can be tested with a plain dict. |
| M-D2 | 2026-10-20 | The audit log holds finding counts and types only, never raw values. |
| M-D3 | 2026-10-20 | A Review result needs an admin click (Approve or Reject). |
| M-D4 | 2026-10-20 | State resets on page reload. Accepted for the demo. |
| M-D5 | 2026-10-20 | The console works with stubs first. Real modules replace them without console changes. |

## Dependencies

| Need | From | Status |
|---|---|---|
| `analyze_app` stub | Person A | Not started |
| `scan_text` stub | Person B | Not started |

## Status log

| Date | Done | Tests |
|---|---|---|
| | | |

## Known issues

(none yet)

## Open questions

- Does the professor want the demo to include a wipe? (Currently P2.)
