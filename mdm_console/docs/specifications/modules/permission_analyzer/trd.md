# TRD: Permission Risk Analyzer

## 1. Files

```
core/rules.py                    data only: WEIGHTS, EXPECTED, THRESHOLDS
core/analyzer.py                 analyze_app()
pages/2_Permission_Analyzer.py   standalone page
tests/test_analyzer.py
```

Python standard library only for the logic. Streamlit only in the page.

## 2. Function contract (frozen)

```python
analyze_app(app_type: str, permissions: list[str]) -> dict
```

Output:
```python
{
  "app_type": "Flashlight",
  "requested": ["CAMERA", "ACCESS_FINE_LOCATION"],
  "unexpected": ["ACCESS_FINE_LOCATION"],
  "score": 3,
  "level": "Medium",     # Low | Medium | High
  "reasons": ["ACCESS_FINE_LOCATION is not needed by a Flashlight app (weight 3)"],
  "action": "Review"     # Allow | Review | Block
}
```

## 3. Algorithm

1. Check `app_type` is a key in `EXPECTED`. If not, raise `ValueError`.
2. Remove duplicates from `permissions`, keep order. Check each is a key in `WEIGHTS`. If not, raise `ValueError`.
3. `unexpected` = requested permissions not in `EXPECTED[app_type]`.
4. `score` = sum of `WEIGHTS[p]` for each unexpected permission.
5. Map score to level and action using `THRESHOLDS` (0 Low Allow, 1 to 3 Medium Review, 4 or more High Block).
6. Build one reason string per unexpected permission: `<PERMISSION> is not needed by a <app type> app (weight <n>)`.
7. If nothing is unexpected, reasons is a single line: `All requested permissions match what a <app type> app normally needs.`

## 4. Data in rules.py

```python
WEIGHTS = {"ACCESS_FINE_LOCATION": 3, "READ_CONTACTS": 3, "RECORD_AUDIO": 3,
           "READ_SMS": 3, "READ_CALL_LOG": 3, "CAMERA": 2, "READ_EXTERNAL_STORAGE": 2}
EXPECTED = {"Flashlight": ["CAMERA"], "Calculator": [], "Maps": ["ACCESS_FINE_LOCATION", "READ_EXTERNAL_STORAGE"],
            "Messaging": ["READ_CONTACTS", "READ_SMS", "RECORD_AUDIO", "CAMERA"],
            "Camera": ["CAMERA", "RECORD_AUDIO", "READ_EXTERNAL_STORAGE", "ACCESS_FINE_LOCATION"],
            "Game": []}
THRESHOLDS = {"medium_from": 1, "high_from": 4}
```
Person A may change these. Any change must update the tests and the justification note.

## 5. Test cases (tests/test_analyzer.py)

| # | App type | Permissions | Expected |
|---|---|---|---|
| 1 | Calculator | none | Low, Allow, score 0 |
| 2 | Flashlight | CAMERA | Low, Allow, score 0 |
| 3 | Flashlight | CAMERA, ACCESS_FINE_LOCATION | Medium, Review, score 3 |
| 4 | Flashlight | CAMERA, ACCESS_FINE_LOCATION, READ_CONTACTS | High, Block, score 6 |
| 5 | Maps | ACCESS_FINE_LOCATION | Low, Allow, score 0 |
| 6 | Messaging | READ_CONTACTS, READ_SMS, READ_CALL_LOG | Medium, Review, score 3 |

Extra tests: unknown app type raises `ValueError`; unknown permission raises `ValueError`; duplicate permissions count once.

## 6. Page behaviour

- `st.selectbox` for app type, `st.multiselect` for permissions.
- Button "Analyze" calls `analyze_app` and shows the result card.
- Catch `ValueError` and show a friendly message.
- No state is saved.

## 7. Run

```
pytest tests/test_analyzer.py
streamlit run app.py
```
