# System Limitations: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Verified System Boundaries, Heuristic Limitations & Known Issues  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Educational Simulation Boundaries

- **Simulated Environment Only:** The application does not interface with actual mobile devices, manage Android runtime permissions, install real APK files, or intercept physical hardware. It is a desktop web simulation designed for classroom demonstration and conceptual learning.
- **No Network Egress Filtering:** The system does not inspect operating system sockets, HTTP requests, or cellular network interfaces. Outbound text checks apply strictly to synthetic text submitted through the application's Streamlit forms.

---

## 2. Pattern Detection Engine Limitations (`core/dlp.py`)

### 2.1 Unspaced 12-Digit Identifiers
- **Limitation:** The 12-digit ID regex (`\d{4}[ -]\d{4}[ -]\d{4}`) strictly requires 4-digit groups separated by a space or hyphen.
- **Consequence:** A continuous 12-digit number (e.g., `123456789012`) is deliberately not detected and will receive an `Allow` disposition. This behavior is documented and asserted in `tests/test_dlp.py::test_unspaced_12_digit_number_is_a_documented_miss`.
- **Rationale:** Matching arbitrary continuous 12-digit numbers without separators produces unacceptable false positive rates on benign timestamps, serial numbers, and tracking IDs.

### 2.2 Phone Number Layouts
- **Limitation:** The phone regular expression targets Indian 10-digit mobile formats starting with digits 6–9, with an optional `+91` country code.
- **Consequence:** International telephone numbers with differing lengths, area codes, or punctuation styles (such as North American `+1 (555) 019-2834` or European layouts) may not be detected.

### 2.3 Potential False Positives
- **Limitation:** Any arbitrary digit sequence between 13 and 16 digits that mathematically satisfies the Luhn modulo-10 checksum will be classified as a `card` and blocked.
- **Consequence:** Benign order numbers, tracking numbers, or inventory IDs that randomly satisfy the Luhn algorithm will be blocked.

### 2.4 Obfuscation & Evasion
- **Limitation:** The scanner utilizes static regular expressions without natural language processing or semantic decoding.
- **Consequence:** Text obfuscated with intentional whitespace (`c a r d`), spelled-out words (`nine eight seven`), character substitutions (`test[at]example[dot]com`), or Base64 encoding will bypass the pattern matching engine.

---

## 3. Heuristic Permission Analyzer Limitations (`core/analyzer.py`)

- **Permissions Do Not Prove Malice:** Granting sensitive permissions does not prove that an application exfiltrates data or behaves maliciously. Conversely, an application with few permissions may still misuse the permissions it possesses.
- **Static Team Heuristic:** The permission weights (2 for medium concern, 3 for high concern) and category expectation baselines in `core/rules.py` represent an educational model of least privilege. They do not constitute a commercial security certification or an authoritative industry standard.
- **Covered Scope:** The heuristic catalog covers 7 common sensitive Android permissions across 6 application categories. It does not encompass the full Android permission manifest (150+ permissions) or custom vendor permissions.

---

## 4. State & Runtime Limitations (`core/store.py`)

- **In-Memory Session Volatility:** All device state, installed package manifests, administrative review queues, and audit logs reside in Streamlit's in-memory `st.session_state`.
- **Browser Refresh Purge:** Hard-refreshing the web page (`F5` or `Ctrl+R`), navigating away, or restarting the Streamlit server completely purges all session data and resets the device to its default active state with zero installed packages.
- **Single-Operator Context:** The application is architected for a single evaluator or presenter on a local machine. It does not support concurrent multi-tenant access or role-based user authentication.
