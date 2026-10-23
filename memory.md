# Project Memory: Mobile Data Leakage Prevention Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Role:** Persistent Architectural Context and Project Memory for Maintainers and AI Agents  
**Last Updated:** 2026-10-23  

---

## 1. Project Identity & Objective

- **Project Name:** Mobile Data Leakage Prevention Console (MDM & DLP Simulation)
- **Primary Objective:** Provide a clear, educational, explainable demonstration of mobile application permission risk analysis, outbound data leakage detection, and MDM policy enforcement for academic evaluation and technical portfolio demonstrations.
- **Academic Context:** Course project for Cyber Security (Computer Science), connected to the case study of the FTC action against "Brightest Flashlight Free" (Dec 2013 / Apr 2014) regarding unauthorized transmission of device location and identifiers.
- **Critical Limitation & Scope:** This is a **local, educational software simulation**. It is **not** a production MDM system, does not manage physical Android devices, does not intercept operating system APIs, does not perform network-layer traffic inspection, and does not provide production security guarantees. All demonstrations use synthetic data.

---

## 2. Technology Stack

- **Runtime:** Python 3.10+ (Standard Library: `re`, `datetime`, `csv`, `io`)
- **Web Interface:** Streamlit (Multi-page architecture, headless testing via `streamlit.testing.v1.AppTest`)
- **Testing:** Pytest (Configured via `pytest.ini` with `pythonpath = .`)
- **Design & Theming:** Custom SOC Technical Minimal CSS injection engine via `core/ui.py`
- **Networking/Database:** None (Fully offline, local in-memory session state storage)

---

## 3. System Architecture & Module Map

```text
Streamlit Multi-page Interface
├── app.py                     [Operational Dashboard & Device Ledger]
└── pages/
    ├── 1_MDM_Console.py       [Simulated MDM Hub: App Install Flow, Wipe, Send Flow]
    ├── 2_Permission_Analyzer.py [Standalone Category Baseline Permission Analyzer]
    └── 3_DLP_Scanner.py       [Standalone Outbound Text Pattern Scanner]
            │
            ▼ (calls pure logic)
Core Business Heuristics & Presentation
├── core/analyzer.py           [analyze_app: calculates unexpected permission score & action]
├── core/dlp.py                [scan_text: regex matching, Luhn validation, masking]
├── core/rules.py              [Static WEIGHTS & EXPECTED dictionary baselines]
├── core/store.py              [In-memory session state mutators & privacy-safe audit logging]
└── core/ui.py                 [SOC Technical Minimal design tokens, CSS variables, theme toggle]
```

---

## 4. Architectural Decisions (Historical & Current)

| ID | Date | Decision & Rationale |
| :--- | :--- | :--- |
| **D1** | 2026-10-20 | Single Streamlit multi-page application. The MDM console serves as the operational hub and invokes `analyzer.py` and `dlp.py` as pure library functions. |
| **D2** | 2026-10-20 | Decoupled core logic from UI: `analyzer.py` and `dlp.py` have zero Streamlit dependencies and return pure Python dictionaries for independent testing. |
| **D3** | 2026-10-20 | Strictly simulated environment: Synthetic demo data only. No real personal data, credit cards, or identity identifiers. |
| **D4** | 2026-10-20 | Frozen function contracts: `analyze_app(app_type, permissions)` and `scan_text(text)` maintain consistent return dictionary schemas. |
| **D5** | 2026-10-20 | Centralized heuristic rules: All scoring weights and category expectations live in `core/rules.py` as plain dictionaries, never embedded in execution code. |
| **D6** | 2026-10-20 | Isolated session state: All mutations pass through `core/store.py` helper functions accepting an explicit `state` dictionary (allowing tests to use standard dicts). |
| **D7** | 2026-10-23 | Enterprise SOC Technical Minimal visual identity: Replaced toy emojis and orange theme with dual-theme (Dark SOC Analyst / Light) system in `core/ui.py`. |

---

## 5. Protected Source Files (Do Not Modify Without Explicit Authorization)

The following core source files contain frozen business logic, contracts, and test assertions:
- `core/analyzer.py` (Heuristic scoring algorithm)
- `core/dlp.py` (Pattern matching, Luhn verification, asterisk masking)
- `core/rules.py` (Permission weight definitions and category baselines)
- `core/store.py` (Device state mutations, app name validation, audit log functions)
- `core/ui.py` (Design tokens, CSS injection, theme toggle)
- `app.py` & `pages/*.py` (User interface workflows matching automated test contracts)

---

## 6. Heuristic Rules & Scoring Logic

### Permission Risk Analysis (`core/rules.py` & `core/analyzer.py`)
- **Weights:**
  - `ACCESS_FINE_LOCATION`: 3
  - `READ_CONTACTS`: 3
  - `RECORD_AUDIO`: 3
  - `READ_SMS`: 3
  - `READ_CALL_LOG`: 3
  - `CAMERA`: 2
  - `READ_EXTERNAL_STORAGE`: 2
- **Expected Baselines:**
  - `Flashlight`: `{"CAMERA"}`
  - `Calculator`: `{}` (empty set)
  - `Maps`: `{"ACCESS_FINE_LOCATION", "READ_EXTERNAL_STORAGE"}`
  - `Messaging`: `{"READ_CONTACTS", "READ_SMS", "RECORD_AUDIO", "CAMERA"}`
  - `Camera`: `{"CAMERA", "RECORD_AUDIO", "READ_EXTERNAL_STORAGE", "ACCESS_FINE_LOCATION"}`
  - `Game`: `{}` (empty set)
- **Scoring & Actions:**
  - Score = Sum of weights for requested permissions not present in the expected category set.
  - Score `0`: **Low Risk** $\rightarrow$ Action: `Allow`
  - Score `1–3`: **Medium Risk** $\rightarrow$ Action: `Review` (triggers administrative approval queue)
  - Score `> 3`: **High Risk** $\rightarrow$ Action: `Block`

### DLP Text Pattern Detection (`core/dlp.py`)
- **Priority Resolution:**
  1. `card`: 13–16 digits with spaces/hyphens; must pass Luhn checksum $\rightarrow$ Action: `Block`
  2. `aadhaar_like`: 12-digit grouped pattern (`\d{4}[ -]\d{4}[ -]\d{4}`) $\rightarrow$ Action: `Block`
  3. `phone`: Indian 10-digit mobile pattern with optional `+91` prefix $\rightarrow$ Action: `Mask`
  4. `email`: Standard `user@domain.tld` pattern $\rightarrow$ Action: `Mask`
- **Masking:** Detected sensitive character spans are replaced with `*`.
- **Privacy & Storage Behavior:** Audit logs record event metadata, finding types, and counts only (e.g., `1 phone, 1 email`). Raw message text and detected sensitive substrings are never stored in session state, written to disk, or exported in CSV.

---

## 7. Current Implementation Status & Test Verification

- **Automated Tests:** 53 tests across 5 test modules (`tests/test_analyzer.py`, `tests/test_dlp.py`, `tests/test_pages.py`, `tests/test_store.py`, `tests/test_ui.py`).
- **Test Status:** 53 passed in ~2.0 seconds.
- **Headless UI Tests:** `test_pages.py` exercises full Streamlit AppTest flows including demo benchmark loaders, install blocks, admin review approval, name validation, and theme switching.
- **WCAG Contrast Ratios:** Verified $\ge 4.5:1$ across all normal text tokens in both Light and Dark themes.

---

## 8. Known Limitations

1. **Unspaced 12-digit IDs:** The regex checks grouped patterns (`XXXX XXXX XXXX` or `XXXX-XXXX-XXXX`); raw unspaced 12-digit strings are not matched (documented educational choice).
2. **Phone Layouts:** Matches standard 10-digit formats (with optional +91 and space/dash); unusual international formatting may be missed.
3. **Session Volatility:** State resides entirely in Streamlit `st.session_state`. Hard-refreshing the browser resets the simulated device and audit trail.
4. **Dual Log on Approval:** When a reviewed app is approved by an administrator, the log reflects the original `Install` attempt and the subsequent `Approve` action.
