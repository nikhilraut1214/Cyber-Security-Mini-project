# Technical Documentation: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Deep Technical Reference & Algorithm Implementation  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Permission Risk Heuristic Engine

### 1.1 Weight Catalog & Expected Sets (`core/rules.py`)

Static heuristics are defined in `core/rules.py`. Weights range from 2 (medium risk) to 3 (high concern):

```python
WEIGHTS = {
    "ACCESS_FINE_LOCATION": 3,
    "READ_CONTACTS": 3,
    "RECORD_AUDIO": 3,
    "READ_SMS": 3,
    "READ_CALL_LOG": 3,
    "CAMERA": 2,
    "READ_EXTERNAL_STORAGE": 2,
}

EXPECTED = {
    "Flashlight": {"CAMERA"},
    "Calculator": set(),
    "Maps": {"ACCESS_FINE_LOCATION", "READ_EXTERNAL_STORAGE"},
    "Messaging": {"READ_CONTACTS", "READ_SMS", "RECORD_AUDIO", "CAMERA"},
    "Camera": {"CAMERA", "RECORD_AUDIO", "READ_EXTERNAL_STORAGE", "ACCESS_FINE_LOCATION"},
    "Game": set(),
}
```

### 1.2 Scoring Function & Thresholds (`core/rules.py`)

```python
def level_for_score(score: int) -> tuple[str, str]:
    if score == 0:
        return "Low", "Allow"
    if score <= 3:
        return "Medium", "Review"
    return "High", "Block"
```

### 1.3 Analysis Algorithm (`core/analyzer.py`)

Function signature: `analyze_app(app_type: str, permissions: list[str]) -> dict`
1. **Input Validation:** Confirms `app_type` exists in `rules.EXPECTED` and `permissions` is an iterable containing only valid keys from `rules.WEIGHTS`.
2. **Deduplication:** Deduplicates requested permissions while preserving order via `list(dict.fromkeys(permissions))`.
3. **Unexpected Permission Identification:**
   $$\text{unexpected} = \{p \in \text{requested} \mid p \notin \text{EXPECTED}[\text{app\_type}]\}$$
4. **Score Calculation:**
   $$\text{score} = \sum_{p \in \text{unexpected}} \text{WEIGHTS}[p]$$
5. **Output Schema:**
   ```python
   {
       "app_type": str,
       "requested": list[str],
       "unexpected": list[str],
       "score": int,
       "level": "Low" | "Medium" | "High",
       "reasons": list[str],
       "action": "Allow" | "Review" | "Block"
   }
   ```

---

## 2. Outbound DLP Text Pattern Detection Engine

### 2.1 Pattern Regular Expressions (`core/dlp.py`)

```python
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,15}\d(?!\d)")
AADHAAR_RE = re.compile(r"(?<!\d)\d{4}[ -]\d{4}[ -]\d{4}(?!\d)")
PHONE_RE = re.compile(r"(?<!\d)(?:(?:\+?91)[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)")
EMAIL_RE = re.compile(r"(?i)(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])")
```

### 2.2 Luhn Checksum Algorithm (`core/dlp.py`)

Candidate numbers matching `CARD_RE` are verified using the modulo 10 Luhn algorithm to eliminate arbitrary 16-digit sequences:

```python
def _luhn_valid(number: str) -> bool:
    digits = [int(char) for char in number if char.isdigit()]
    total = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return bool(digits) and total % 10 == 0
```

### 2.3 Priority Resolution & Overlap Deconfliction

To prevent ambiguous matches (e.g., credit card segments mistakenly matching phone formats), candidates are extracted, assigned priority weights, and sorted:

```python
priority = {"card": 0, "aadhaar_like": 1, "phone": 2, "email": 3}
candidates.sort(key=lambda item: (item["start"], priority[item["type"]], -(item["end"] - item["start"])))
```

Overlapping matches are resolved by dropping any subsequent candidate whose span intersects an already accepted candidate.

### 2.4 Masking & Policy Enforcement

- **Masking:** Each character position between `start` and `end` in the candidate text is overwritten with `*`.
- **Policy Decision Rule:**
  - If any finding is of type `card` or `aadhaar_like` $\rightarrow$ Action: **`Block`**.
  - Else if any findings exist (`phone` or `email`) $\rightarrow$ Action: **`Mask`**.
  - Otherwise $\rightarrow$ Action: **`Allow`**.

---

## 3. Session State Management (`core/store.py`)

All mutations to the simulated device, pending review queue, and audit log pass through `core/store.py`.

### 3.1 Input Validation (`validate_app_name`)
- Validates string length between 1 and 60 characters.
- Executes `scan_text(clean)["findings"]` to prevent sensitive numbers from entering package manifests or audit logs.
- Enforces character regex: `^[A-Za-z0-9][A-Za-z0-9 _().-]*$`.

### 3.2 Device Mutators
- `install_app(state, name, app_type, permissions, analysis)`: Appends record to `device["installed_apps"]` and records an `Install` log event. Rejects installs if `device["wiped"]` is `True`.
- `wipe_device(state)`: Clears `device["installed_apps"]`, sets `device["wiped"] = True`, clears `pending_install`, and records a `Wipe` event.
- `reenrol_device(state)`: Restores `device["wiped"] = False` and logs a `Re-enrol` event.

### 3.3 Audit Logging & Privacy Boundaries
- `add_log(state, event, detail, result)`: Prepends a structured event row containing timestamp, event category, detail, and result.
- **Privacy Rule:** The `detail` parameter must never contain raw text. For outbound checks, callers pass `summarize_findings(result["findings"])` (e.g., `"1 phone, 1 email"`).
- `log_to_csv(state)`: Serializes session audit records to standard CSV with headers `time,event,detail,result`.

---

## 4. UI Theming Engine (`core/ui.py`)

- **`apply_theme()`**: Inspects `st.session_state["theme_mode"]` (`"dark"` or `"light"`) and injects scoped CSS overriding Streamlit defaults.
- **`badge_html(text, kind)`**: Returns sanitized HTML spans with classes matching theme tokens (`soc-badge-allow`, `soc-badge-review`, `soc-badge-block`, `soc-badge-mask`).
- **`render_sidebar_nav()`**: Renders a Streamlit `radio` selector allowing dynamic theme toggling with instant `st.rerun()`.
