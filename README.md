# Mobile Data Leakage Prevention Console

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-53%20passed-brightgreen.svg)]()
[![License: Educational Simulation](https://img.shields.io/badge/scope-Educational%20Simulation-informational.svg)]()

An explainable, student-friendly **Mobile Device Management (MDM) and Data Loss Prevention (DLP)** simulation engineered for computer science cybersecurity coursework. Demonstrates pre-install least-privilege permission risk scoring, client-side outbound text pattern inspection, simulated remote wipe/re-enrolment, and privacy-safe audit logging within an enterprise **SOC Technical Minimal** dual-theme interface.

> **Critical Educational Disclaimer:** This application is strictly a local software simulation. It does not control physical phones, interface with the Android OS framework, inspect network-layer traffic, or contact external servers. Use synthetic demonstration examples only.

---

## Key Features

- **SOC Technical Minimal Interface:** Enterprise-grade dual-theme system (Dark SOC Analyst mode and Light mode) with text status badges, monospace telemetry, and a non-flickering sidebar theme toggle.
- **Permission Risk Analyzer:** Evaluates requested Android permissions against category least-privilege baselines using weighted heuristics (`0` = Allow, `1–3` = Review, `>3` = Block).
- **Simulated MDM Hub:** Manages endpoint enrollment, models an administrative approval queue for borderline applications, and executes lost-device remote wipes.
- **Outbound DLP Text Scanner:** Evaluates egress text payloads for payment cards (Luhn-verified), grouped 12-digit ID patterns, phone numbers, and emails with zero raw-text retention.
- **Privacy-Safe Audit Trail:** Reverse-chronological event ledger recording finding categories and counts only; includes one-click CSV export.
- **Automated Test Suite:** 53 automated tests across pure logic modules, session mutators, and headless Streamlit `AppTest` browser workflows.

---

## Architecture at a Glance

```text
Cyber-Security-Mini-project/
├── app.py                     # Operational Dashboard & Device Ledger
├── pages/
│   ├── 1_MDM_Console.py       # MDM Operations, Install Approvals & Egress Checks
│   ├── 2_Permission_Analyzer.py # Category Baseline Permission Analyzer
│   └── 3_DLP_Scanner.py       # Outbound Text Pattern Scanner Workbench
├── core/
│   ├── analyzer.py            # Pure permission scoring heuristic engine
│   ├── dlp.py                 # Pure regex & Luhn text pattern scanner
│   ├── rules.py               # Static permission weights and category baselines
│   ├── store.py               # Session state mutators & privacy-safe audit logger
│   └── ui.py                  # SOC Technical Minimal theme engine & tokens
├── tests/                     # 53 automated unit and headless UI tests
├── docs/                      # Canonical technical documentation suite
├── memory.md                  # Persistent AI agent and maintainer context
├── rule.md                    # Mandatory operating rules for AI agents
├── CHANGELOG.md               # Version & milestone history
└── requirements.txt           # Pinned runtime dependencies
```

---

## Quickstart Setup

### Windows (PowerShell)
```powershell
# 1. Create and activate virtual environment
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Launch application
streamlit run app.py
```

### macOS / Linux
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Launch application
streamlit run app.py
```

Open `http://localhost:8501` in your web browser. After initial setup, the application operates **100% offline** with zero external network calls.

---

## Running Automated Tests

```bash
# Run all 53 automated tests
pytest -q
```
*Expected result:* `53 passed in ~2.0s`.

---

## 5-Minute Evaluation Demo

1. **Install Calculator (Allow):** On the **MDM Console**, install `Calculator` with no permissions $\rightarrow$ Score `0` (`Low`, `Allow`).
2. **Install Risky Flashlight (Block):** Click `Load demo example: risky flashlight` (`CAMERA`, `LOCATION`, `CONTACTS`) $\rightarrow$ Score `6` (`High`, `Block`).
3. **Install Review Flashlight (Approval Queue):** Configure `Flashlight` with `CAMERA` and `LOCATION` $\rightarrow$ Score `3` (`Medium`, `Review`). Click `Approve install`.
4. **Send Phone Number (Mask):** Send `Call me on 9876543210` $\rightarrow$ Phone detected; masked output `Call me on **********` displayed and logged.
5. **Send Test Card (Block):** Send `card 4111 1111 1111 1111` $\rightarrow$ Luhn-valid card detected; outbound transmission blocked.
6. **Simulate Lost Phone (Wipe):** Click `Lost phone — wipe` $\rightarrow$ Endpoint state set to `WIPED`; apps cleared.
7. **Audit Review & CSV Export:** Return to Home (`app.py`), inspect the live event ledger, and click `Export audit log as CSV`.

---

## Detailed Documentation Directory

| Document | Description |
| :--- | :--- |
| **[Project Overview](docs/PROJECT_OVERVIEW.md)** | Problem statement, FTC Brightest Flashlight context, academic objectives, and scope. |
| **[Architecture Guide](docs/ARCHITECTURE.md)** | Layered system design, data flow diagrams, session state schema, and decoupled testing model. |
| **[Feature Catalog](docs/FEATURES.md)** | Exhaustive specifications for Dashboard, MDM Console, Permission Analyzer, and DLP Scanner. |
| **[Installation Manual](docs/INSTALLATION.md)** | Step-by-step environment setup for Windows and Unix, offline verification, and troubleshooting. |
| **[User & Demo Guide](docs/USER_GUIDE.md)** | Operational manual, status badge reference, and complete evaluation demonstration script. |
| **[Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)** | Heuristic algorithms, permission weights, regex pattern specifications, and Luhn checksum implementation. |
| **[Security & Privacy](docs/SECURITY_AND_PRIVACY.md)** | Threat model, in-memory volatile storage behavior, and zero-retention audit logging architecture. |
| **[Testing Suite](docs/TESTING.md)** | Pytest test strategy, test scenario descriptions across all 53 tests, and AppTest guidelines. |
| **[System Limitations](docs/LIMITATIONS.md)** | Explicit documentation of known heuristic boundaries, edge cases, and simulation constraints. |
| **[Project Memory](memory.md)** | Root context for maintainers and AI agents: architecture, decisions (D1–D7), and protected files. |
| **[Operating Rules](rule.md)** | Mandatory governance rules for AI coding agents. |
| **[Changelog](CHANGELOG.md)** | Complete chronological milestone log. |

---

## Verification & Academic Integrity

- **Synthetic Data Exclusively:** All tests, demonstration payloads, and documentation examples use synthetic dummy data. Never submit or test with real personal data or payment credentials.
- **Explainable Heuristics:** Permission weights and pattern matching rules are intentionally transparent to allow second-year computer science students to explain every policy decision during technical evaluation.
