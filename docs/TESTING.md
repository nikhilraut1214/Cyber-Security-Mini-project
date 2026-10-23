# Testing Documentation: Mobile DLP Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Test Strategy, Automated Test Scenarios & Execution Guide  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Test Architecture & Framework

The project utilizes **pytest** as its primary test runner. The test suite is organized into unit tests for pure domain modules and headless integration tests for the Streamlit user interface:

- **Unit Testing:** Exercises `core/analyzer.py`, `core/dlp.py`, `core/rules.py`, `core/store.py`, and `core/ui.py` using standard Python assertions.
- **Headless UI Testing:** Utilizes Streamlit's official testing framework (`streamlit.testing.v1.AppTest`) to simulate browser interactions, form submissions, button clicks, and session state changes without running a graphical web browser.
- **Root Configuration:** `pytest.ini` configures `pythonpath = .` and `testpaths = tests`, ensuring test discovery works from the repository root.

---

## 2. Test Execution Commands

### Quick Execution
```bash
pytest -q
```
*Expected output:*
```text
.....................................................                    [100%]
53 passed in 2.06s
```

### Verbose Execution with Test Names
```bash
pytest -v
```

### Module-Specific Execution
```bash
pytest tests/test_analyzer.py
pytest tests/test_dlp.py
pytest tests/test_pages.py
pytest tests/test_store.py
pytest tests/test_ui.py
```

---

## 3. Test Scenarios Breakdown (53 Tests Total)

### 3.1 Permission Analyzer Tests (`tests/test_analyzer.py` - 8 Tests)
- `test_calculator_no_permissions_is_low_allow`: Confirms Calculator with zero permissions scores 0 (`Low`, `Allow`).
- `test_flashlight_camera_is_expected`: Confirms Flashlight requesting only `CAMERA` scores 0 (`Low`, `Allow`).
- `test_flashlight_location_needs_review`: Confirms Flashlight requesting `CAMERA` + `ACCESS_FINE_LOCATION` scores 3 (`Medium`, `Review`).
- `test_flashlight_location_and_contacts_is_blocked`: Confirms Flashlight requesting location and contacts scores 6 (`High`, `Block`).
- `test_maps_location_is_expected`: Confirms Maps app requesting `ACCESS_FINE_LOCATION` is expected (`Low`, `Allow`).
- `test_messaging_unexpected_call_log_needs_review`: Confirms Messaging requesting unexpected `READ_CALL_LOG` scores 3 (`Medium`, `Review`).
- `test_unknown_app_type_raises`: Validates that invalid app category names raise `ValueError`.
- `test_unknown_permission_raises`: Validates that invalid permission identifiers raise `ValueError`.

### 3.2 DLP Text Scanner Tests (`tests/test_dlp.py` - 14 Tests)
- `test_phone_is_masked`: Confirms standard 10-digit phone number is replaced with asterisks.
- `test_email_is_masked`: Confirms email address is replaced with asterisks.
- `test_fake_luhn_card_is_blocked`: Confirms candidate card passing Luhn validation triggers `Block`.
- `test_grouped_id_like_number_is_blocked`: Confirms 4-4-4 grouped 12-digit format triggers `Block`.
- `test_non_luhn_16_digit_number_is_not_card`: Confirms 16-digit number failing Luhn check is allowed.
- `test_plain_text_is_allowed`: Confirms benign text without patterns returns `Allow`.
- `test_empty_text_is_allowed`: Confirms empty string returns `Allow` with zero findings.
- `test_text_over_limit_is_rejected`: Confirms string > 5,000 characters raises `ValueError`.
- `test_findings_do_not_include_matched_values`: Asserts findings hold only `type`, `start`, and `end` offsets.
- `test_phone_with_country_prefix_is_masked`: Verifies `+91` prefixed phone detection.
- `test_phone_written_with_spaces_is_masked`: Verifies spaced phone number detection.
- `test_hyphenated_id_like_number_is_blocked`: Verifies hyphenated 12-digit format detection.
- `test_spaced_card_is_still_a_card_not_a_phone`: Confirms spaced credit cards are deconflicted as cards, not phones.
- `test_unspaced_12_digit_number_is_a_documented_miss`: Verifies documented boundary (unspaced 12 digits returns `Allow`).

### 3.3 Session Store Tests (`tests/test_store.py` - 17 Tests)
- `test_get_device_initializes_default`: Verifies lazy initialization of device state.
- `test_install_app_adds_app_and_log`: Verifies package insertion into manifest and audit trail logging.
- `test_wipe_clears_apps_and_marks_wiped`: Verifies device wipe purges apps and updates status flag.
- `test_reenrol_allows_device_to_be_active`: Verifies re-enrolment restores active status.
- `test_newest_log_row_is_first`: Confirms audit log prepends newest events at index 0.
- `test_csv_has_header_and_rows`: Verifies CSV string generation with proper column headers.
- `test_counts_include_blocked_installs_and_sends`: Asserts accuracy of dashboard count aggregations.
- `test_install_is_rejected_after_wipe`: Confirms package install throws `ValueError` on wiped endpoint.
- `test_sensitive_looking_app_name_is_rejected`: Confirms phone numbers in app names raise `ValueError`.
- `test_validate_app_name_accepts_simple_labels`: Validates standard alphanumeric package names.
- `test_validate_app_name_rejects_bad_labels` (6 parametrized tests): Rejects empty strings, whitespace, >60 chars, digits-only, `<script>` injection, and leading hyphens.
- `test_install_app_uses_same_name_rule_as_the_page`: Verifies uniform validation in page and store.

### 3.4 Headless Streamlit Page Tests (`tests/test_pages.py` - 10 Tests)
- `test_all_pages_load_without_errors`: Headless execution of `app.py`, `1_MDM_Console.py`, `2_Permission_Analyzer.py`, and `3_DLP_Scanner.py` confirming zero uncaught exceptions.
- `test_console_starts_with_risky_flashlight_filled_in`: Asserts default initial form values.
- `test_console_demo_button_restores_the_example`: Tests "Load demo example" button interaction.
- `test_risky_flashlight_is_blocked_and_not_installed`: Tests install click and block error assertion.
- `test_review_then_approve_installs_the_app`: Tests Review flow and subsequent approval button click.
- `test_hyphenated_app_name_is_accepted_on_the_page`: Tests UI form submission with hyphenated name.
- `test_sensitive_looking_app_name_is_rejected`: Tests UI form error when sensitive name entered.
- `test_audit_log_never_holds_raw_values`: Simulates DLP send flows and verifies raw numbers absent from log text.
- `test_analyzer_demo_button_fills_the_risky_example`: Tests standalone analyzer demo button click.
- `test_theme_switcher_toggles_mode_without_error`: Tests radio theme selector toggling to `Light` mode.

### 3.5 UI Presentation Tests (`tests/test_ui.py` - 4 Tests)
- `test_themes_definition_contains_required_keys`: Verifies presence of all required color tokens in both themes.
- `test_theme_state_default_and_setter`: Verifies getter and setter state management.
- `test_generate_css_returns_non_empty_css`: Confirms CSS generation contains CSS variables.
- `test_badge_html_generates_valid_span`: Asserts correct HTML span classes for status badges.

---

## 4. Instructions for Adding New Tests

When adding features or fixing bugs:
1. Place unit tests in the appropriate module file under `tests/`.
2. Do not import `streamlit` inside `test_analyzer.py` or `test_dlp.py` to maintain pure logic isolation.
3. For new UI pages or form elements, add headless test scenarios in `tests/test_pages.py` using `AppTest.from_file()`.
4. Run `pytest -q` to verify that all 53 baseline tests plus new tests pass before opening a pull request.
