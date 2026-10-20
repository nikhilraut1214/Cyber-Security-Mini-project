# Memory: DLP-style Scanner

## Facts

- Owner: Person B
- Part of the Mobile Data Leakage Prevention Console, deadline Saturday 24 Oct 2026
- Called by the MDM console's send-message flow
- Stack: Python standard library (`re`), Streamlit page, pytest

## Decisions

| ID | Date | Decision |
|---|---|---|
| D-D1 | 2026-10-20 | Findings hold type and position only, never the matched value. |
| D-D2 | 2026-10-20 | Pattern order: card, aadhaar_like, phone, email. Overlaps are skipped. |
| D-D3 | 2026-10-20 | Card matches need the Luhn check to reduce false alarms. |
| D-D4 | 2026-10-20 | Block for card or aadhaar_like. Mask for phone or email. |
| D-D5 | 2026-10-20 | Text over 5,000 characters raises ValueError. |
| D-D6 | 2026-10-20 | The function contract is frozen. Changes need all three teammates. |

## Status log

| Date | Done | Tests |
|---|---|---|
| | | |

## Known issues

(none yet)

## Open questions

- Should a Mask result also show the masked text in the audit log? (Currently no. Log counts only.)
