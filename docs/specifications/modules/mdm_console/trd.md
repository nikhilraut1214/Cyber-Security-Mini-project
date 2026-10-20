# TRD: MDM Console

## 1. Files

```
app.py                       home page, summary counts, audit log
pages/1_MDM_Console.py       device panel, install, send, wipe
core/store.py                device state and audit log
tests/test_store.py
```

## 2. Dependencies on other modules

The console imports `analyze_app` from `core/analyzer.py` and `scan_text` from `core/dlp.py`. Persons A and B put stubs with the exact contract shape in those files on Tuesday. Replace nothing in the console when the real versions arrive.

## 3. Shared state

State lives in `st.session_state`. To make `store.py` testable, every function takes a `state` dict as its first argument. The app passes `st.session_state`. Tests pass a plain `{}`.

```python
get_device(state) -> dict                 # creates default if missing
install_app(state, name, app_type, permissions) -> None
wipe_device(state) -> None
reenrol_device(state) -> None
add_log(state, event, detail, result) -> None
get_log(state) -> list[dict]              # latest first
log_to_csv(state) -> str
get_counts(state) -> dict                 # blocked apps, masked, blocked messages
```

Default device:
```python
{"name": "Student Phone", "installed_apps": [], "wiped": False}
```
Log row: `{"time": "HH:MM:SS", "event": "Install|Send|Wipe|Approve|Reject|Re-enrol", "detail": str, "result": str}`.

## 4. Flows

### Install

```
if device wiped: show message, stop
result = analyze_app(app_type, permissions)
Allow  -> install_app, log("Install", "<name> (<type>)", "Allowed")
Block  -> log("Install", "<name> (<type>)", "Blocked: score <n>")
Review -> show Approve and Reject buttons, keep result in session_state until pressed
  Approve -> install_app, log("Approve", ..., "Approved by admin")
  Reject  -> log("Reject", ..., "Rejected by admin")
```

### Send

```
if device wiped: show message, stop
result = scan_text(text)
Allow -> log("Send", "no findings", "Sent")
Mask  -> log("Send", "<counts by type>", "Masked and sent")
Block -> log("Send", "<counts by type>", "Blocked")
```
`<counts by type>` looks like `1 phone, 1 email`. Never log the text or masked text.

### Wipe and re-enrol

- Wipe: clear `installed_apps`, set `wiped` true, log "Wipe".
- Re-enrol: set `wiped` false, log "Re-enrol". The app list stays empty.

## 5. Error handling

- Catch `ValueError` from either module and show a friendly message. Log nothing for invalid input.
- Page reload resets state. Say so in the UI.

## 6. Tests (tests/test_store.py, plain dict as state)

| # | Check |
|---|---|
| 1 | New state creates the default device |
| 2 | install_app adds the app once, not twice |
| 3 | wipe_device empties the apps and sets wiped true |
| 4 | reenrol_device clears wiped |
| 5 | add_log puts the newest row first |
| 6 | log_to_csv has a header and one line per row |
| 7 | get_counts counts blocked installs and masked or blocked sends |

The flows are checked by running the demo script by hand.

## 7. Run

```
pytest tests/test_store.py
streamlit run app.py
```
