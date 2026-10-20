# PRD: DLP-style Scanner

- **Owner:** Person B
- **Part of:** Mobile Data Leakage Prevention Console (see the main prd.md)
- **Course tool it represents:** Data Loss Prevention (DLP)
- **Used by:** the "send message" flow in the MDM console

## 1. Purpose

Check text before it leaves the device. Find sensitive items (phone numbers, emails, card-like numbers, 12-digit ID-like numbers), then allow, mask or block the message.

## 2. In scope

- Detect four finding types: phone, email, card, aadhaar_like.
- Mask findings with `*`.
- Decide an action: Allow, Mask or Block.
- A standalone page to try it alone.

## 3. Out of scope

- Scanning files, images or real messages.
- Real personal data of any kind. Fake test data only.
- Machine learning, network calls, storing text.

## 4. Features

| ID | Feature | Priority |
|---|---|---|
| D1 | Detection of the four finding types | P1 |
| D2 | Card check with the Luhn formula to cut false alarms | P1 |
| D3 | Masking of findings | P1 |
| D4 | Action decision: Allow, Mask, Block | P1 |
| D5 | Standalone Streamlit page with demo example | P1 |

All five are needed for the module to be complete.

## 5. Acceptance criteria

1. All 7 DLP test cases pass (listed in trd.md).
2. Findings hold type and position only, never the matched value.
3. Text over 5,000 characters raises `ValueError`, and the page shows a friendly message.
4. The MDM console can call `scan_text` with no changes to its code.
5. Person B can explain the Luhn check and the pattern order.

## 6. Limits to state in the report

- Pattern matching may flag harmless numbers and miss spaced-out or written-out numbers.
- A 12-digit match is only "ID-like". It does not verify a real ID.
- Only four types are covered.

## 7. Done when

Tests pass, the page works offline, and the output never contains raw sensitive values in findings.
