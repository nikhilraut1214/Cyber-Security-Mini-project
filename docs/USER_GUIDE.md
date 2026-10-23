# User & Demonstration Guide: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** End-User Operational Manual & Evaluation Demo Script  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Application Navigation & Theme Controls

When launched, the application provides a sidebar navigation menu containing:
1. **Multi-Page Navigation:** Access the Home Dashboard, MDM Console, Permission Analyzer, and DLP Scanner.
2. **Display Theme Switcher:** Select between **`Dark (SOC)`** (low-glare analyst view) and **`Light`** (presentation report view). The theme selection persists across all pages during the session.
3. **System Telemetry Strip:** Displays the static heuristic engine version (`v1.2`) and simulated sandbox profile.

---

## 2. Page Workflows

### 2.1 Operational Dashboard (`app.py`)
- **KPI Metrics:** View the number of approved packages on the simulated endpoint, rejected installation attempts, and outbound messages blocked or masked.
- **Device Ledger:** Review the active software manifest on the device, including individual package risk levels and heuristic scores.
- **Policy Reference:** Expand the Heuristic Policy Reference drawer to inspect static permission weights and category baselines.
- **Audit Export:** Click **`Export audit log as CSV`** to download the complete event history as `mdm_audit_log.csv`.

### 2.2 MDM Console (`pages/1_MDM_Console.py`)
- **Package Installation:**
  1. Enter an application name (e.g., `Torch-Pro`) or click **`Load demo example: risky flashlight`**.
  2. Select the application type and requested permissions.
  3. Click **`Check and install`**.
  4. If the app is evaluated as `Allow`, it appears in the **Installed Packages** ledger immediately.
  5. If the app is evaluated as `Block`, an error banner displays the policy violation and score.
  6. If the app requires `Review`, the **Administrative Approval Queue** surfaces with **`Approve install`** and **`Reject install`** controls.
- **Outbound Message Transmission Check:**
  1. Enter a text message draft in the **Message to check** text box.
  2. Click **`Check and send`**.
  3. The DLP engine evaluates the text: clean text is allowed; phone numbers or emails are masked before transmission; payment cards or 12-digit IDs are blocked.
- **Remote Device Wipe & Re-enrolment:**
  - Click **`Lost phone — wipe`** in the sidebar to simulate device wipe. All installed packages are purged, and further actions are disabled.
  - Click **`Re-enrol device`** to restore active operational status.

### 2.3 Permission Risk Analyzer (`pages/2_Permission_Analyzer.py`)
- **Standalone Heuristic Analysis:**
  1. Select an application category (e.g., `Calculator`, `Flashlight`, `Messaging`).
  2. The **Category Baseline** card dynamically updates to show expected permissions.
  3. Tick candidate permissions or click **`Load flashlight demo`**.
  4. Click **`Analyze permissions`**.
  5. Inspect the policy decision pill (`[ALLOW]`, `[REVIEW]`, `[BLOCK]`), numeric score, unexpected permissions badges, and rule justification list.

### 2.4 DLP Text Scanner (`pages/3_DLP_Scanner.py`)
- **Standalone Payload Inspection:**
  1. Enter synthetic text or click **`Load demo example`**.
  2. Click **`Scan text`**.
  3. Inspect the policy disposition badge, sanitized masked output, and detected entity offsets table.

---

## 3. Status Badges Reference

| Badge | Meaning | Action Taken |
| :--- | :--- | :--- |
| `[ALLOW]` | Zero or expected permissions / clean text | Application installed; message sent unchanged |
| `[REVIEW]` | Score between 1 and 3 (moderate least-privilege violation) | Held in administrative review queue for manual decision |
| `[BLOCK]` | Score $\ge 4$ or payment card / 12-digit ID detected | Installation rejected; outbound message transmission blocked |
| `[MASK]` | Phone number or email address detected | Message sanitized with asterisks prior to transmission |
| `[ACTIVE]` | Simulated endpoint is enrolled and operational | Full installation and outbound checks enabled |
| `[WIPED]` | Simulated endpoint was wiped by administrator | Package ledger cleared; actions blocked until re-enrolment |

---

## 4. The 5-Minute Evaluation Demonstration Script

Follow this verified sequence during live academic evaluation or presentation:

| Step | Page | Action | Expected Result |
| :--- | :--- | :--- | :--- |
| **1** | MDM Console | Select `Calculator`, request **no permissions**, click `Check and install`. | **`[ALLOW]`**: Score 0. Calculator installs into the active ledger. |
| **2** | MDM Console | Click `Load demo example: risky flashlight` (`CAMERA`, `LOCATION`, `CONTACTS`), click `Check and install`. | **`[BLOCK]`**: Score 6 (High Risk). Installation blocked; app excluded from device. |
| **3** | MDM Console | Configure `Flashlight` with `CAMERA` and `ACCESS_FINE_LOCATION`, click `Check and install`. | **`[REVIEW]`**: Score 3 (Medium Risk). Surfaces Approval Queue. Click `Approve install` to install. |
| **4** | MDM Console | In message box, type: `Call me on 9876543210`, click `Check and send`. | **`[MASK]`**: Phone detected. Masked output `Call me on **********` displayed and logged. |
| **5** | MDM Console | In message box, type: `card 4111 1111 1111 1111`, click `Check and send`. | **`[BLOCK]`**: Luhn-valid card detected. Transmission blocked. |
| **6** | MDM Console | Click `Lost phone — wipe` in sidebar. | Device status changes to **`WIPED`**; installed apps cleared. |
| **7** | Dashboard | Navigate to Home (`app.py`). | Review the updated KPI metrics and Audit Trail table. Click `Export audit log as CSV` to demonstrate log export. |
