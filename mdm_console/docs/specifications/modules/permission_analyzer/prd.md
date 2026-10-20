# PRD: Permission Risk Analyzer

- **Owner:** Person A
- **Part of:** Mobile Data Leakage Prevention Console (see the main prd.md)
- **Course tool it represents:** an MDM-style app policy check
- **Used by:** the install flow in the MDM console

## 1. Purpose

Check the permissions an app asks for against what that type of app really needs, and give a risk level with an action. Example: a flashlight asking for location and contacts is high risk.

## 2. In scope

- Pick an app type, tick requested permissions, get a result.
- Score, level, plain-English reasons, and an action: Allow, Review or Block.
- A standalone page so this module can be demoed alone.

## 3. Out of scope

- Reading real app files or real phones.
- Network calls, machine learning, app store lookups.
- Judging whether an app actually leaks data.

## 4. Features

| ID | Feature | Priority |
|---|---|---|
| PA1 | `analyze_app` function with scoring and action | P0 |
| PA2 | Reasons list in plain English | P0 |
| PA3 | Standalone Streamlit page | P0 |
| PA4 | "Load demo example" button (flashlight with location and contacts) | P1 |

## 5. Acceptance criteria

1. All 6 analyzer test cases pass (listed in trd.md).
2. Unknown app type or unknown permission raises a clear `ValueError`.
3. The page always shows: "Permissions alone do not prove data leakage."
4. The MDM console can call `analyze_app` with no changes to its code.
5. Person A can explain every weight and every expected-permission choice.

## 6. Limits to state in the report

- Weights and thresholds are a team design choice, not a standard.
- An app can be risky with few permissions or safe with many.
- Only 7 permissions and 6 app types are covered.

## 7. Done when

Tests pass, the page works offline, and rules.py matches rules.md.
