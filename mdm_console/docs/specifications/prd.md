# PRD: Mobile Data Leakage Prevention Console

Mini project for the Cyber Security course. Same topic as the group video "Your Flashlight App Is Watching You".

- **Team:** 3 students (Person A, Person B, Person C)
- **Start:** Tuesday 20 Oct 2026
- **Deadline:** Saturday 24 Oct 2026
- **Type:** Working software demo plus short report
- **Status of this document:** draft v1, update the Open Questions section as answers arrive

## 1. Overview

A small web app that simulates how an organisation prevents mobile app data leakage. An MDM-style console (the hub) decides what a phone may install and send. It calls two modules: a Permission Risk Analyzer and a DLP-style text scanner. Every decision is written to an audit log.

Everything is a **simulation**. It does not control real phones or touch real user data.

## 2. Problem statement

Mobile apps can collect personal data (location, contacts, device ID) and send it to third parties without clear notice. Real example: the FTC acted against the "Brightest Flashlight Free" app in 2013 for sending location and device ID to ad networks. Users and organisations need a way to spot risky apps before install and to stop sensitive data leaving a device.

## 3. Goals

1. Show how an app's requested permissions can be checked against what its type needs.
2. Show how sensitive text can be detected and masked or blocked before it leaves a device.
3. Join both checks under one MDM-style console with an audit trail.
4. Be demoable in under 5 minutes on one laptop.
5. Every team member can explain the module they own.

## 4. Non-goals

- No real device management, no real app installs, no Android code.
- No real personal data. Test data only.
- No machine learning. Rules only.
- No user accounts, login or database.
- No claim of being a real MDM or DLP product.

## 5. Users

| User | Need |
|---|---|
| Evaluator (professor) | See a working tool, understand the logic, link it to course tools (MDM, DLP) |
| Demo audience | Follow the flashlight-app story in minutes |
| Team members | Build and explain their own module |

## 6. Features and priority

| ID | Feature | Priority |
|---|---|---|
| F1 | Permission Risk Analyzer: pick app type, tick permissions, get score, level, reasons, action | P0 |
| F2 | MDM console "install app" flow that calls F1 and applies Allow / Review / Block | P0 |
| F3 | Audit log of every decision, shown in a table | P0 |
| F4 | DLP-style scanner: find phone numbers, emails, card-like and ID-like numbers | P1 |
| F5 | MDM console "send message" flow that calls F4 and applies Allow / Mask / Block | P1 |
| F6 | Simulated remote wipe | P2 |
| F7 | Dashboard counts (apps blocked, messages masked) | P2 |
| F8 | Export audit log as CSV | P2 |

## 7. User stories and acceptance criteria

- **F1:** As an admin I tick the permissions a flashlight app asks for and see a risk level with plain-English reasons.
  - Flashlight with only CAMERA gives Low and Allow.
  - Flashlight with CAMERA and ACCESS_FINE_LOCATION gives Medium and Review.
  - Flashlight with CAMERA, ACCESS_FINE_LOCATION and READ_CONTACTS gives High and Block.
  - A note says permissions alone do not prove data leakage.
- **F2:** As an admin I try to install an app on the simulated phone.
  - Allow installs it. Block refuses it. Review shows Approve and Reject buttons.
  - The phone's installed list updates.
- **F3:** Every install, send and wipe adds one row: time, event, detail, result.
- **F4/F5:** As an admin I type a message and press Send.
  - A message with only a phone number or email is masked, then sent.
  - A message with a valid test card number or a 12-digit ID-like number is blocked.
  - A message with none of these is sent unchanged.
  - The audit log never stores the raw sensitive value.
- **F6:** Pressing "Lost phone" empties installed apps and marks the device wiped.

## 8. Demo script (5 minutes)

1. Install a calculator with no permissions: Low, allowed.
2. Install a flashlight asking for location and contacts: High, blocked.
3. Send a message with a phone number: masked and sent.
4. Send a message with a test card number: blocked.
5. Press "Lost phone": device wiped.
6. Show the audit log with all events.

## 9. Success criteria

- All P0 features work on the demo laptop with no internet.
- The 6 analyzer test cases and the DLP test cases in the TRD pass.
- Each member explains their module without reading the code.
- Report and demo state the known limitations.

## 10. Constraints

- 4 days, 3 people, free tools only.
- Python and Streamlit unless the professor requires another language.
- Must run offline.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Not enough time for 3 modules | Build P0 first, follow the cut order in phases.md |
| AI-written code nobody can explain | Each member reads and explains their module; rules written by hand |
| Modules do not fit together | Freeze the function contracts on day 1 (see trd.md) |
| False alarms in the scanner | Luhn check for cards; list limits in the report |
| AI tool quota runs out | Spread work over 3 accounts; commit working code often |

## 12. Known limitations (state in report and demo)

- Permissions alone do not prove leakage. An app can be risky with few permissions or safe with many.
- Scores and weights are a team design choice, not an industry standard.
- Pattern matching misses obfuscated data and may flag harmless numbers.
- This is MDM-style and DLP-style only. Real products do much more.

## 13. Open questions

- What must be submitted besides the demo: report, hard copy, slides?
- Is Python allowed, or is a specific language required?
- Is the demo on our laptop or a college computer?
