# Security & Privacy Documentation: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Security Boundaries, Privacy Architecture & Threat Model  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Educational Simulation Boundaries

The Mobile DLP Console is an educational software simulation engineered to illustrate mobile security principles. To prevent misunderstanding, maintainers, students, and evaluators must recognize the following technical boundaries:

- **No Operating System Control:** The application does not interface with the Android framework, Linux kernel, or mobile runtime environments. It does not monitor physical hardware, intercept system calls, or enforce OS-level sandboxing.
- **No Network Egress Interception:** The application does not monitor network interfaces, sockets, VPN tunnels, or HTTP proxies. It inspects only synthetic text manually entered into the Streamlit interface.
- **No Real Personal Data:** The application is architected strictly for synthetic demonstration data. Evaluators and users must **never** enter real personal data, actual credit card numbers, or live identity credentials.

---

## 2. Actual Storage & Lifecycle Behavior

### 2.1 In-Memory Volatile Session Storage
- **Storage Mechanism:** Application data is stored strictly in Streamlit's in-memory session cache (`st.session_state`).
- **No Disk or Database Persistence:** The application does not write records to SQLite, PostgreSQL, local JSON files, or external cloud storage.
- **Lifecycle & Volatility:** Session state exists only as long as the active browser session remains connected. Hard-refreshing the browser (`F5` or `Ctrl+R`) or restarting the Streamlit process immediately purges all simulated device records, pending reviews, and audit events.

### 2.2 Privacy Safeguards in Audit Logging
The application enforces strict data-minimization boundaries in `core/store.py` and `pages/1_MDM_Console.py`:
- **Finding Counts Only:** For outbound text inspection events, the audit log records only finding types and counts via `dlp.summarize_findings(result["findings"])` (e.g., `"1 phone, 1 email"`).
- **Zero Raw Payload Retention:** Neither raw outgoing message text nor matched substrings (such as phone numbers or card digits) are ever passed to `store.add_log()`.
- **CSV Export Boundaries:** When a user clicks `Export audit log as CSV`, the downloaded file contains exclusively timestamps, event names, sanitized detail summaries, and outcome results.

### 2.3 Input Sanitization Against Data Injection
To prevent sensitive data from inadvertently entering audit logs via package identifiers, `store.validate_app_name` runs `scan_text(clean)["findings"]` on user input. If an application name contains a sensitive-looking pattern (such as a 10-digit phone number or card string), the installation is rejected before state mutation occurs.

---

## 3. Threat Model & Heuristic Scope

| Threat / Scenario | Simulated Protection | Implementation Reality & Boundary |
| :--- | :--- | :--- |
| **Over-Privileged Package** | High risk score; automated install block or admin review | Evaluates declared permissions against static category expectations. Cannot detect dynamically requested runtime permissions. |
| **Accidental Plaintext Card Leak** | Detected via Luhn algorithm; outbound message blocked | Detects 13–16 digit strings with valid Luhn checksums. Cannot detect encrypted, tokenized, or split card data. |
| **National ID Number Leak** | Detected via 4-4-4 grouped format; message blocked | Flags grouped 12-digit strings. Does not validate against external government registries and misses unspaced 12-digit numbers. |
| **Phone Number / Email Exfiltration** | Sanitized via asterisk replacement; masked before send | Masks standard 10-digit phone formats and email addresses. Cannot detect obfuscated text (e.g., `user [at] domain`). |
| **Lost or Compromised Endpoint** | Remote wipe clears package manifest and revokes active state | Empties simulated session list. Does not perform cryptographic erasure or physical hardware wipe. |

---

## 4. Summary of Security Posture

The application provides an explainable heuristic demonstration of least-privilege analysis and DLP filtering. It is not an enterprise security appliance, does not guarantee data exfiltration prevention, and must be evaluated strictly as an educational software prototype.
