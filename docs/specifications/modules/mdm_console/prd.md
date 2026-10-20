# PRD: MDM Console (simulated)

- **Owner:** Person C
- **Part of:** Mobile Data Leakage Prevention Console (see the main prd.md)
- **Course tool it represents:** Mobile Device Management (MDM)
- **Role:** the hub. It calls the Permission Risk Analyzer and the DLP-style scanner, applies their decisions, and records everything.

## 1. Purpose

Show how an organisation controls what a phone may install and send. One simulated phone, one admin screen, and an audit log.

## 2. In scope

- A simulated device with an installed-apps list.
- Install flow: call the analyzer, then Allow, Review (Approve or Reject) or Block.
- Send flow: call the DLP scanner, then Allow, Mask or Block.
- Simulated remote wipe and re-enrol.
- Audit log of every decision, with counts on the home page.

## 3. Out of scope

- Real devices, real installs, real messages.
- Login, users, database, network.

## 4. Features

| ID | Feature | Priority |
|---|---|---|
| M1 | Device panel: name, status, installed apps | P0 |
| M2 | Install flow with Allow, Review and Block | P0 |
| M3 | Audit log table (home page and console) | P0 |
| M4 | Send flow with Allow, Mask and Block | P1 |
| M5 | Remote wipe and re-enrol | P2 |
| M6 | Dashboard counts (apps blocked, messages masked or blocked) | P2 |
| M7 | Export audit log as CSV | P2 |

## 5. Acceptance criteria

1. Installing a calculator with no permissions installs it. The log shows Allowed.
2. Installing a flashlight with CAMERA, ACCESS_FINE_LOCATION and READ_CONTACTS is blocked and not added to the device.
3. A Review result shows Approve and Reject. Approve installs, Reject does not, both are logged.
4. Sending a message with a phone number sends the masked text. A message with a test card number is blocked.
5. The audit log never holds a raw sensitive value, only finding types and counts.
6. After a wipe, the installed list is empty and install and send are disabled until re-enrol.
7. The console works with stub modules first and with the real modules later, with no code change.

## 6. Demo script (owned by this module)

1. Install a calculator: allowed.
2. Install a flashlight with location and contacts: blocked.
3. Send a message with a phone number: masked and sent.
4. Send a message with a test card number: blocked.
5. Press Lost phone: wiped.
6. Show the audit log.

## 7. Limits to state

- Everything is simulated.
- State resets when the page reloads.
- This is MDM-style. Real MDM manages many devices and policies.

## 8. Done when

The demo script runs end to end on the demo laptop with no internet.
