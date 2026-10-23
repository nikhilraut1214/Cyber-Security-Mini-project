# Architecture Documentation: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** System Architecture & Data Flow Specification  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. System Architecture Overview

The Mobile DLP Console is designed with a **layered, decoupled architecture** that separates user interface components from pure domain logic, heuristic data, and state persistence.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      STREAMLIT MULTI-PAGE UI                           │
│   app.py (Dashboard)          pages/1_MDM_Console.py (Operations Hub)  │
│   pages/2_Permission_Analyzer pages/3_DLP_Scanner.py                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION & THEMING LAYER                       │
│                              core/ui.py                                │
│   • Scoped CSS Generation (Dark SOC / Light)  • Theme Switcher         │
│   • Text Status Badges                        • Compliance Banners     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐   ┌────────────────────────────────┐
│        PURE DOMAIN ENGINES        │   │     STATE MUTATION LAYER       │
│                                   │   │          core/store.py         │
│  core/analyzer.py                 │   │  • Device Record Mutators      │
│  • analyze_app(type, perms)       │   │  • Pending Review Queue        │
│                                   │   │  • Privacy-Safe Audit Logger   │
│  core/dlp.py                      │   │  • CSV Exporter                │
│  • scan_text(text)                │   └───────────────┬────────────────┘
│  • Luhn checksum validation       │                   │
│                                   │                   ▼
│  core/rules.py                    │   ┌────────────────────────────────┐
│  • WEIGHTS dictionary             │   │       SESSION STORAGE          │
│  • EXPECTED dictionary            │   │      st.session_state          │
└───────────────────────────────────┘   └────────────────────────────────┘
```

---

## 2. Layer Responsibilities & Architectural Boundaries

### 2.1 Pure Domain Logic (`core/analyzer.py` & `core/dlp.py`)
- **Zero UI Dependencies:** The core modules import only the Python standard library (`re`, `collections.Counter`) and internal data rules (`core.rules`). They contain zero Streamlit imports or references.
- **Deterministic Testing:** Functions are pure; given identical inputs, they produce identical outputs without side effects, enabling rapid unit testing in `tests/test_analyzer.py` and `tests/test_dlp.py`.

### 2.2 Static Heuristic Rules (`core/rules.py`)
- Centralizes all heuristic weights, expected permission sets, and scoring threshold mappings.
- Completely decoupled from execution code, ensuring rules can be inspected or adjusted in a single file without modifying analytical algorithms.

### 2.3 State Management & Audit Storage (`core/store.py`)
- **Explicit State Injection:** All state mutation functions (`get_device`, `install_app`, `wipe_device`, `add_log`, `get_counts`) accept an explicit `state` dictionary parameter. In the live application, `st.session_state` is supplied; during automated unit testing (`tests/test_store.py`), a standard Python dictionary is passed.
- **Privacy Enforcement Boundary:** `store.py` validates that audit log detail fields contain only package names, event labels, or aggregated finding counts, preventing raw message text from entering application memory.

### 2.4 Presentation & Design System (`core/ui.py`)
- Implements the approved **SOC Technical Minimal** design system.
- Employs an injectable CSS variable architecture (`generate_css`) to support instant switching between **Dark (SOC Analyst)** and **Light** modes.
- Generates standardized HTML micro-badges (`ui.badge_html`) without reliance on non-standard Unicode emojis.

---

## 3. Data Flow Workflows

### 3.1 Application Installation Workflow
```
[User Form Input] ──► [store.validate_app_name()]
                              │ (valid)
                              ▼
                      [analyzer.analyze_app()]
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     Action == "Allow"  Action == "Review" Action == "Block"
            │                 │                 │
            ▼                 ▼                 ▼
   [store.install_app()]  [store.set_pending()]  [store.log_decision()]
   • Added to device      • Admin queue shown   • Installation rejected
   • Logged: Installed    • Approve/Reject btns • Logged: Blocked
```

### 3.2 Outbound Text Inspection Workflow
```
[User Text Input] ──► [Input Length Check (<= 5,000 chars)]
                              │ (valid)
                              ▼
                      [dlp.scan_text()]
                      • Card detection (Luhn checksum)
                      • 12-digit ID detection (grouped regex)
                      • Phone number detection (+91 / 10-digit)
                      • Email address detection (user@domain)
                              │
                      [Priority Sort & Overlap Deconfliction]
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     Action == "Allow"   Action == "Mask"  Action == "Block"
            │                 │                 │
            ▼                 ▼                 ▼
   • Sent unchanged      • Asterisk masked • Outbound blocked
   • Logged: Allowed     • Logged: Masked  • Logged: Blocked
```

---

## 4. Session State Schema

State is maintained in Streamlit's `st.session_state` under three primary namespaces initialized lazily via `store._ensure_state(state)`:

```python
{
    "device": {
        "name": "Student Phone",
        "installed_apps": [
            {
                "name": str,
                "app_type": str,
                "permissions": list[str],
                "risk_level": str,     # "Low", "Medium", "High"
                "risk_score": int      # 0 to 18
            }
        ],
        "wiped": bool                  # True if device was wiped
    },
    "audit_log": [
        {
            "time": str,               # "YYYY-MM-DD HH:MM:SS %Z"
            "event": str,              # "Install", "Send", "Wipe", "Approve", "Reject"
            "detail": str,             # Package name or finding types/counts
            "result": str              # "Installed", "Blocked", "Masked and sent", etc.
        }
    ],
    "pending_install": dict or None,   # Holds candidate record awaiting admin review
    "theme_mode": str                  # "dark" or "light"
}
```

---

## 5. Automated Testing Integration Architecture

Automated testing is configured via `pytest.ini` with `pythonpath = .`:
1. **Unit Testing (`tests/test_analyzer.py`, `test_dlp.py`, `test_store.py`, `test_ui.py`):** Pure functional execution verifying mathematical scoring, regex edge cases, Luhn validation, state mutator integrity, and CSS rendering.
2. **Headless Integration Testing (`tests/test_pages.py`):** Utilizes `streamlit.testing.v1.AppTest` to run full browser lifecycle tests against `app.py` and all three pages without launching a graphical browser.
