# TRD: Mobile Data Leakage Prevention Console

## 1. Stack

- Python 3.10 or newer
- Streamlit for the interface (multipage app)
- pytest for tests
- Standard library only for logic (`re`, `datetime`, `csv`)
- No database, no network calls, no external APIs

Create `requirements.txt` with `streamlit` and `pytest`. After installing, pin the exact versions that work on your laptops, and use the same ones on all three.

## 2. Architecture

```
Streamlit UI (pages/)
      |
      v
MDM Console page  ---- calls ---->  core/analyzer.py   analyze_app()
      |                       \--->  core/dlp.py        scan_text()
      v
core/store.py  (device state + audit log in st.session_state)
core/rules.py  (permission rules and weights, plain dictionaries)
```

The MDM console is the only page that changes device state. The analyzer and DLP modules are pure functions with no UI code, so they can be tested alone.

## 3. Folder structure

```
mdm_console/
  app.py                       home page, summary, audit log
  pages/
    1_MDM_Console.py           install, send, wipe
    2_Permission_Analyzer.py   standalone analyzer screen
    3_DLP_Scanner.py           standalone scanner screen
  core/
    __init__.py
    rules.py                   data only
    analyzer.py
    dlp.py
    store.py
  tests/
    test_analyzer.py
    test_dlp.py
    test_store.py
  .streamlit/config.toml       theme (see design.md)
  requirements.txt
  README.md
```

## 4. Function contracts (freeze on day 1)

### 4.1 `analyze_app(app_type, permissions) -> dict`

Input: `app_type` is one of the keys in `rules.EXPECTED`. `permissions` is a list of Android permission names that are keys in `rules.WEIGHTS`.

Output:
```python
{
  "app_type": "Flashlight",
  "requested": ["CAMERA", "ACCESS_FINE_LOCATION"],
  "unexpected": ["ACCESS_FINE_LOCATION"],
  "score": 3,
  "level": "Medium",          # Low | Medium | High
  "reasons": ["ACCESS_FINE_LOCATION is not needed by a Flashlight app (weight 3)"],
  "action": "Review"          # Allow | Review | Block
}
```
Rules: unknown app type or unknown permission raises `ValueError` with a clear message. Scoring thresholds are in `rules.md`.

### 4.2 `scan_text(text) -> dict`

Output:
```python
{
  "findings": [{"type": "phone", "start": 11, "end": 21}],
  "masked_text": "Call me on **********",
  "action": "Mask"            # Allow | Mask | Block
}
```
Finding types: `phone`, `email`, `card`, `aadhaar_like`. Findings hold positions and type only, never the matched value. Empty text returns Allow with no findings.

### 4.3 `store.py`

```python
get_device(state) -> dict        # {"name", "installed_apps": [], "wiped": False}
install_app(state, name, app_type, permissions) -> None
wipe_device(state) -> None
reenrol_device(state) -> None
add_log(state, event, detail, result) -> None
get_log(state) -> list[dict]     # latest first: {"time", "event", "detail", "result"}
log_to_csv(state) -> str
get_counts(state) -> dict
```
`state` is `st.session_state` in the app and a plain dict in tests. State lives under the keys `device` and `audit_log`. A page reload resets it, which is acceptable.

## 5. Module behaviour

- **Review flow:** the console shows Approve and Reject. Approve installs and logs "Approved by admin". Reject logs "Rejected by admin".
- **Send flow:** run `scan_text`. Allow sends as is. Mask sends `masked_text`. Block does not send. Log the action and the finding types and counts only.
- **Wipe:** clear `installed_apps`, set `wiped` true, log the event. Installing after a wipe is allowed again after a "Re-enrol device" button.

## 6. Test cases

Analyzer:

| # | App type | Permissions | Expected |
|---|---|---|---|
| 1 | Calculator | none | Low, Allow |
| 2 | Flashlight | CAMERA | Low, Allow |
| 3 | Flashlight | CAMERA, ACCESS_FINE_LOCATION | Medium, Review (score 3) |
| 4 | Flashlight | CAMERA, ACCESS_FINE_LOCATION, READ_CONTACTS | High, Block (score 6) |
| 5 | Maps | ACCESS_FINE_LOCATION | Low, Allow |
| 6 | Messaging | READ_CONTACTS, READ_SMS, READ_CALL_LOG | Medium, Review (score 3) |

DLP (use fake data only):

| # | Text | Expected |
|---|---|---|
| 1 | "Call me on 9876543210" | Mask, one phone |
| 2 | "mail test@example.com" | Mask, one email |
| 3 | "card 4111 1111 1111 1111" | Block, one card (valid test number) |
| 4 | "ref 1234 5678 9012" | Block, one aadhaar_like |
| 5 | "order 1234567890123456" (fails Luhn) | Allow |
| 6 | "see you at 5 pm" | Allow |
| 7 | "" | Allow |

## 7. Error handling

- Show friendly Streamlit messages for invalid input, never a stack trace.
- Empty permission list is valid.
- Very long text (over 5,000 characters) is rejected with a message.

## 8. Security and ethics

- Simulation only. No real device control, no network access.
- Never use real personal data, real card numbers or real ID numbers in tests, screenshots or the report.
- The audit log must not hold raw sensitive values or masked message text; record finding types/counts only.
- Show the banner "Simulation: not a real MDM or DLP" on every page.

## 9. Run and test

```
pip install -r requirements.txt
streamlit run app.py
pytest
```
Works offline after install.

## 10. Definition of done

- All pytest tests pass.
- App starts with one command and runs the 6-step demo script from the PRD.
- No hard-coded demo results: the UI calls the real functions.
