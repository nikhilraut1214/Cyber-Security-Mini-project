# Installation & Setup Guide: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Installation, Environment Configuration & Troubleshooting  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Prerequisites

Before installing the project, verify that your development environment satisfies the following requirements:
- **Operating System:** Windows 10/11, macOS, or modern Linux distribution.
- **Python Version:** Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Package Manager:** `pip` (standard with Python distributions).
- **Network Access:** Required **only once** to install dependencies from PyPI. After initial setup, the application runs **100% offline** with zero external network calls.

---

## 2. Installation on Windows (PowerShell)

### Step 1: Open PowerShell in the Project Directory
Navigate to the root directory where the repository is located:
```powershell
cd D:\Cyber-Security-Mini-project
```

### Step 2: Create a Virtual Environment
```powershell
py -3 -m venv .venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

> **Note on PowerShell Execution Policy:** If activation is blocked by Windows execution policy, execute the scripts using the virtual environment's Python binary directly:
> ```powershell
> .\.venv\Scripts\python.exe -m pip install --upgrade pip
> .\.venv\Scripts\python.exe -m pip install -r requirements.txt
> ```

### Step 4: Install Dependencies
If the virtual environment is activated:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 3. Installation on macOS & Linux

### Step 1: Open Terminal in the Project Directory
```bash
cd Cyber-Security-Mini-project
```

### Step 2: Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 4. Running the Application

From the repository root (the folder containing `app.py`):
```bash
streamlit run app.py
```

Streamlit will initialize the local web server and print the local access URL:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in any modern web browser (Chrome, Firefox, Edge, Safari). Use the Streamlit sidebar to navigate between pages and toggle display themes.

---

## 5. Running the Automated Test Suite

To run all automated tests and verify system integrity:
```bash
pytest -q
```

To run tests with detailed test-case reporting:
```bash
pytest -v
```

The repository includes a root `pytest.ini` configuring `pythonpath = .`, ensuring tests run without manual `PYTHONPATH` exports.

---

## 6. Troubleshooting Common Issues

### Issue 1: `Script execution is disabled on this system` (Windows)
**Cause:** PowerShell execution policy restricts running unsigned activation scripts.  
**Resolution:** Either bypass the policy for the active session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Or execute commands directly via the virtual environment executable:
```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

### Issue 2: `Port 8501 is already in use`
**Cause:** Another Streamlit process or background service is listening on port 8501.  
**Resolution:** Specify an alternate port using the `--server.port` flag:
```bash
streamlit run app.py --server.port 8502
```

### Issue 3: `ModuleNotFoundError: No module named 'core'` during Pytest
**Cause:** Executing pytest from a nested directory without the root on Python's path.  
**Resolution:** Always run `pytest` from the repository root, where `pytest.ini` automatically configures the project root as an import root.
