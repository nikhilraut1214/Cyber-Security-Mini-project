# Rules: DLP-style Scanner

## Part A. Rules for the AI agent (this module)

1. Read this module's prd.md, trd.md, design.md and memory.md first, then the main trd.md for the shared contracts.
2. Show a plan before coding and wait for approval.
3. Do not change the `scan_text` signature or output keys.
4. Never store or return the matched value. Positions and types only.
5. Write tests first, run them, report the real result.
6. Keep the code short and commented. Each helper has a one-line purpose comment.
7. No new packages, no network calls.
8. Update memory.md after each finished task.

## Part B. Detection rules

| Order | Type | Extra check |
|---|---|---|
| 1 | card | 13 to 16 digits and Luhn passes |
| 2 | aadhaar_like | 12 digits in groups of 4, no check |
| 3 | phone | optional +91 or 91, then 10 digits starting 6 to 9 |
| 4 | email | standard name@domain.tld |

Overlap rule: a later match is ignored if it overlaps an earlier accepted one.

## Part C. Action rules

| Found | Action |
|---|---|
| card or aadhaar_like | Block |
| phone or email only | Mask |
| nothing | Allow |

Masking replaces every character of a finding with `*`.

## Part D. Data and safety rules

1. Fake data only in code, tests, screenshots and the report.
2. The ID-like pattern is for demonstration. Never use a real ID number.
3. Use well-known fake test numbers for cards.
4. Say "DLP-style" in the demo, never claim to be a real DLP product.

## Part E. Known limits (say them out loud in the demo)

- Harmless numbers can be flagged.
- Spaced-out, written-out or obfuscated numbers can be missed.
- Only four types are covered.
