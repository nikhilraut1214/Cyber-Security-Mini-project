# TRD: DLP-style Scanner

## 1. Files

```
core/dlp.py                  scan_text() and helpers
pages/3_DLP_Scanner.py       standalone page
tests/test_dlp.py
```

Standard library only for the logic (`re`). Streamlit only in the page.

## 2. Function contract (frozen)

```python
scan_text(text: str) -> dict
```

Output:
```python
{
  "findings": [{"type": "phone", "start": 11, "end": 21}],
  "masked_text": "Call me on **********",
  "action": "Mask"       # Allow | Mask | Block
}
```
Finding types: `phone`, `email`, `card`, `aadhaar_like`. Empty text returns Allow and no findings.

## 3. Patterns (suggested starting points, test and adjust)

| Type | Regex idea |
|---|---|
| card | `(?<!\d)(?:\d[ -]?){12,15}\d(?!\d)` then keep only if digits are 13 to 16 and Luhn passes |
| aadhaar_like | `(?<!\d)\d{4}[ -]?\d{4}[ -]?\d{4}(?!\d)` |
| phone | `(?<!\d)(?:\+?91[ -]?)?[6-9]\d{9}(?!\d)` |
| email | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` |

## 4. Algorithm

1. If `len(text) > 5000`, raise `ValueError`.
2. Look for matches in this order: card, aadhaar_like, phone, email.
3. For card matches, strip spaces and dashes, require 13 to 16 digits, and require `luhn_ok`. Otherwise ignore the match.
4. Skip any match whose span overlaps a finding already accepted. This stops a card from also being reported as an ID-like number.
5. Sort findings by start position.
6. Build `masked_text` by replacing each finding's span with `*` of the same length. Work from the end of the text backwards so positions stay correct.
7. Action: any card or aadhaar_like means Block. Else any phone or email means Mask. Else Allow.
8. The console sends the original text only for Allow, sends `masked_text` only for Mask, and sends nothing for Block. The standalone scanner may display `masked_text` for explanation, but must label it as a preview and must not imply that a blocked message was sent.

Luhn check: from the right, double every second digit, subtract 9 if the result is above 9, sum all digits, valid if the sum is divisible by 10.

## 5. Test cases (tests/test_dlp.py, fake data only)

| # | Text | Expected |
|---|---|---|
| 1 | "Call me on 9876543210" | Mask, one phone, masked_text has no digits of the number |
| 2 | "mail test@example.com" | Mask, one email |
| 3 | "card 4111 1111 1111 1111" | Block, one card (a well-known test number), no aadhaar_like |
| 4 | "ref 1234 5678 9012" | Block, one aadhaar_like |
| 5 | "order 1234567890123456" | Allow (fails Luhn) |
| 6 | "see you at 5 pm" | Allow |
| 7 | "" | Allow |

Extra tests: text of 5,001 characters raises `ValueError`; findings never contain a "value" key.

## 6. Page behaviour

- `st.text_area` for input, button "Scan".
- Show action card, a small table of finding types and counts, and the masked text.
- Catch `ValueError` and show a friendly message.
- "Load demo example" fills a message with a fake phone number and a test card number.

## 7. Run

```
pytest tests/test_dlp.py
streamlit run app.py
```
