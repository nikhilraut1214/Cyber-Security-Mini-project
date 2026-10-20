# Memory: Permission Risk Analyzer

## Facts

- Owner: Person A
- Part of the Mobile Data Leakage Prevention Console, deadline Saturday 24 Oct 2026
- Called by the MDM console's install flow
- Stack: Python, Streamlit, pytest

## Decisions

| ID | Date | Decision |
|---|---|---|
| PA-D1 | 2026-10-20 | Score is the sum of weights of unexpected permissions only. |
| PA-D2 | 2026-10-20 | Thresholds: 0 Low, 1 to 3 Medium, 4 or more High. |
| PA-D3 | 2026-10-20 | Only 7 permissions and 6 app types in version 1. |
| PA-D4 | 2026-10-20 | The function contract is frozen. Changes need all three teammates. |

## Status log

| Date | Done | Tests |
|---|---|---|
| | | |

## Known issues

(none yet)

## Open questions

- Should a Medium result always need admin review in the MDM console? (Currently yes.)
