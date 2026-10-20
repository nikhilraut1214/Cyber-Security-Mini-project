# Mobile Data Leakage Prevention Console

A small, explainable **simulation** for a Cyber Security mini-project. It demonstrates app permission risk scoring, a DLP-style outgoing-text scanner, an MDM-style console, simulated wipe/re-enrol, and a privacy-conscious audit log.

> **Simulation: not a real MDM or DLP.** This application does not control real phones, install real apps, send messages, contact a server, or use a database. Use synthetic examples only.

## Features

- **Permission Risk Analyzer:** scores requested permissions that are unexpected for an app type.
- **MDM Console:** simulates install decisions (`Allow`, `Review`, `Block`), outbound text checks (`Allow`, `Mask`, `Block`), and lost-device wipe/re-enrol.
- **DLP-style Scanner:** detects phone-like, email, Luhn-valid card-like, and grouped 12-digit ID-like patterns.
- **Audit log:** newest event first; message events contain finding types/counts only, never message contents or matched values.
- **Dashboard:** summary counts and CSV export.
- **Tests:** pytest coverage for the analyzer, scanner, store and the Streamlit pages (headless).

## Requirements

- Python 3.10 or newer
- pip
- Internet access only to install dependencies the first time; runtime behavior is local and makes no network calls.

## Setup (Windows PowerShell)

```powershell
# 1. Open PowerShell in the extracted mdm_console folder
py -3 -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# If PowerShell blocks activation, run commands using the venv Python directly:
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# If activation worked, use:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Setup (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the application

From the project root (the folder containing `app.py`):

```bash
streamlit run app.py
```

Streamlit prints a local URL, normally `http://localhost:8501`. Open that URL in your browser. Use the sidebar navigation to open the three pages.

## Run tests

```bash
pytest -q
```

`pytest.ini` puts the project folder on the import path, so plain `pytest -q` works. Keep the Streamlit version pinned in `requirements.txt`; newer versions deprecate `use_container_width`.

## Five-minute demo

1. On **MDM Console**, install `Calculator` with no permissions: it should be allowed.
2. Try `Flashlight` with `CAMERA`, `ACCESS_FINE_LOCATION`, and `READ_CONTACTS`: score 6, high risk, blocked.
3. Try `Flashlight` with `CAMERA` and `ACCESS_FINE_LOCATION`: score 3, review; approve or reject.
4. Send `Call me on 9876543210`: the phone-like value is masked in the simulated outgoing text.
5. Send `card 4111 1111 1111 1111`: the Luhn-valid test card pattern is blocked.
6. Use **Lost phone — wipe**, then re-enrol the device if you want to continue.
7. Return to Home to show the audit log and optionally export the CSV.

The numbers above are synthetic examples for demonstration, not real personal data.

## Decision rules

### Permission risk

| Score | Level | Action |
|---:|---|---|
| 0 | Low | Allow |
| 1–3 | Medium | Review |
| 4+ | High | Block |

The score is the sum of weights for permissions not expected for the selected app type. The rules live in `core/rules.py` so students can explain and adjust them.

### DLP-style scanner

- A valid Luhn card-like pattern or a 12-digit ID-like pattern in groups of 4 triggers `Block`.
- Phone-like or email patterns trigger `Mask`.
- No supported pattern triggers `Allow`.
- The scanner returns positions and types, not matched values.
- Text longer than 5,000 characters is rejected.

## Privacy and limitations

- The audit log must never store raw messages, masked message text, or matched values.
- Detection is heuristic: benign numbers can be flagged, obfuscated patterns can be missed, and only four categories are supported.
- The ID-like pattern is a demonstration pattern and does not validate an identity. It needs groups of 4 digits separated by a space or hyphen; 12 digits with no separators are not detected.
- Phone numbers are detected as 10 digits (optionally with +91 and one space or hyphen in the middle). Other layouts can be missed.
- The in-memory state resets when the app session is restarted.
- Permission choices alone do not prove that an app leaks data.
- Do not use real personal information in tests, screenshots, or the report.

## Project structure

```text
mdm_console/
├── app.py
├── pages/
│   ├── 1_MDM_Console.py
│   ├── 2_Permission_Analyzer.py
│   └── 3_DLP_Scanner.py
├── core/
│   ├── __init__.py
│   ├── rules.py
│   ├── analyzer.py
│   ├── dlp.py
│   └── store.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_dlp.py
│   ├── test_pages.py
│   └── test_store.py
├── .streamlit/config.toml
├── pytest.ini
├── requirements.txt
└── README.md
```
