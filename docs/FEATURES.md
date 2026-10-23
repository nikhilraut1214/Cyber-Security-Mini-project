# Feature Specifications: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Functional Feature Specifications  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Operational Overview Dashboard (`app.py`)

### Purpose
Provides a centralized executive and operational overview of the simulated endpoint's security posture, active software inventory, and real-time audit telemetry.

### Key Capabilities
- **Simulated Endpoint KPI Telemetry:**
  - `Simulated Device`: Endpoint identifier (`Student Phone`) and active operational status (`ACTIVE` or `WIPED`).
  - `Installed Apps`: Count of currently approved and installed packages on the simulated device.
  - `Blocked Installs`: Count of installations rejected by automated policy or manual administrator rejection.
  - `DLP Blocked/Masked Events`: Aggregate count of outbound text transmissions intercepted or masked by the DLP scanner.
- **Simulated Device Ledger:**
  - Tabular view of installed packages displaying Package Name, Category, Risk Level, and Numeric Heuristic Score.
- **Heuristic Policy Reference:**
  - Interactive reference table displaying static permission risk weights and expected category baselines.
- **Live Audit Trail & CSV Exporter:**
  - Reverse-chronological table of all security events recorded during the current session.
  - `Export audit log as CSV` button triggering instant browser download of `mdm_audit_log.csv`.

---

## 2. Mobile Device Management (MDM) Console (`pages/1_MDM_Console.py`)

### Purpose
Serves as the primary operational hub simulating mobile endpoint policy enforcement, application installations, and remote lifecycle management.

### Key Capabilities
- **Sidebar Endpoint Profile:**
  - Displays endpoint name, operational status pill, and count of active packages.
  - **Remote Device Wipe:** Simulates lost-device wipe; immediately purges all installed packages, sets device status to `WIPED`, logs the wipe event, and disables further installs and sends until re-enrolled.
  - **Device Re-enrolment:** Reactivates a wiped device and restores active operational state.
- **Application Ingestion Workflow:**
  - `Load demo example: risky flashlight` benchmark button pre-populates form with `Flashlight`, `CAMERA`, `ACCESS_FINE_LOCATION`, and `READ_CONTACTS`.
  - Application name validation: Rejects names with sensitive-looking patterns or invalid characters via `store.validate_app_name`.
  - Automated policy disposition:
    - **`Allow`:** Immediately adds the package to the device inventory and logs the installation.
    - **`Block`:** Immediately rejects the installation, displays a policy error card, and logs the blocked install without modifying the device.
    - **`Review`:** Places the application in the **Administrative Approval Queue**.
- **Administrative Approval Queue:**
  - Surfaced when an application receives a `Review` disposition.
  - Displays application name, category, calculated score, and rule violation reasons.
  - Provides dual action buttons:
    - `Approve install`: Completes package installation, records an administrative approval log entry, and clears the pending state.
    - `Reject install`: Discards the package, records an administrative rejection log entry, and clears the pending state.
- **Outbound Message Transmission Check:**
  - Text area supporting simulated SMS/chat drafts up to 5,000 characters.
  - Invokes `dlp.scan_text` on submission:
    - `Allow`: Dispatches payload unchanged.
    - `Mask`: Displays the sanitized, asterisk-masked payload that would be transmitted.
    - `Block`: Halts outbound transmission and displays detected pattern types.
  - Logs finding types and counts only; excludes raw message text.

---

## 3. Permission Risk Analyzer (`pages/2_Permission_Analyzer.py`)

### Purpose
An interactive, standalone inspection tool that evaluates Android package permissions against category least-privilege baselines using weighted heuristics.

### Key Capabilities
- **Package Configuration:**
  - Category selector supporting 6 application types (`Flashlight`, `Calculator`, `Maps`, `Messaging`, `Camera`, `Game`).
  - Permission multiselect supporting 7 sensitive Android permissions.
  - `Load flashlight demo` benchmark button.
- **Dynamic Category Baseline Inspector:**
  - Dynamically displays the expected permission set for the currently selected category (e.g., `Flashlight` $\rightarrow$ `CAMERA`; `Calculator` $\rightarrow$ `None`).
- **Policy Evaluation & Scoring Engine:**
  - Invokes `analyzer.analyze_app()` on demand.
  - Renders a structured policy verdict badge (`ALLOW`, `REVIEW`, `BLOCK`).
  - Displays the numeric calculated risk score and assigned risk level (`Low`, `Medium`, `High`).
  - Highlights unexpected permissions as individual red tag badges.
  - Provides a bulleted list of plain-English heuristic violation rationales detailing permission weights.

---

## 4. Outbound DLP Text Scanner (`pages/3_DLP_Scanner.py`)

### Purpose
A dedicated workbench that demonstrates client-side data loss prevention pattern detection and masking on outbound text.

### Key Capabilities
- **Payload Inspection Workspace:**
  - Text area accepting synthetic outgoing payloads up to 5,000 characters.
  - `Load demo example` button populating synthetic text containing phone, email, card, and ID patterns.
- **Detection Heuristics Engine:**
  - **Payment Card Detection:** Detects 13–16 digit candidates and performs mathematical Luhn checksum validation. Disposition: `Block`.
  - **12-digit ID-like Pattern Detection:** Detects 4-4-4 grouped digit patterns. Disposition: `Block`.
  - **Phone Number Detection:** Detects 10-digit Indian mobile formats with optional `+91` prefix. Disposition: `Mask`.
  - **Email Pattern Detection:** Detects standard `user@domain.tld` formats. Disposition: `Mask`.
- **Inspection Telemetry & Output:**
  - Policy disposition card (`ALLOW`, `MASK`, `BLOCK`) with summary of findings.
  - Masked output viewer displaying asterisks replacing detected spans.
  - Zero-retention detected entity offset table showing pattern type, start index, end index, and character span.
  - Explicit privacy constraints notice.
