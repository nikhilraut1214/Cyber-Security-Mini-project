# Changelog: Mobile Data Leakage Prevention Console

All notable changes, architectural milestones, and fixes to this project are documented here.
This project adheres to clear milestone tracking and semantic documentation.

---

## [v1.1.0] - 2026-10-23: Architecture Governance & Documentation Consolidation

### Added
- **`memory.md`:** Persistent architectural context, decision records (D1–D7), and system limitations at repository root.
- **`rule.md`:** Mandatory operational constraints and quality standards for AI agents at repository root.
- **Canonical Technical Documentation (`docs/`):**
  - `docs/PROJECT_OVERVIEW.md`: Detailed problem statement, FTC Brightest Flashlight context, and academic scope.
  - `docs/ARCHITECTURE.md`: Technical architecture, data flow, Streamlit session lifecycle, and theme system.
  - `docs/FEATURES.md`: Functional documentation for all 4 application modules.
  - `docs/INSTALLATION.md`: Verified installation procedures, environment setup, and offline verification.
  - `docs/USER_GUIDE.md`: End-user guide, 5-minute evaluation demonstration script, and badge reference.
  - `docs/TECHNICAL_DOCUMENTATION.md`: Mathematical scoring heuristics, regex patterns, Luhn check, and state mutators.
  - `docs/SECURITY_AND_PRIVACY.md`: Privacy architecture, non-retention audit logging, and simulation boundaries.
  - `docs/TESTING.md`: Complete description of the 53 automated test cases and AppTest headless testing.
  - `docs/LIMITATIONS.md`: Exhaustive review of verified heuristic limitations and edge cases.
- **`REPOSITORY_AUDIT.md`:** Formal repository audit documenting folder consolidation and cleanup analysis.

### Removed
- Removed 25 redundant, fragmented, and outdated draft specification files previously nested under `docs/specifications/` and `docs/specifications/modules/`.

---

## [v1.0.0] - 2026-10-23: SOC Technical Minimal UI Optimization

### Added
- **`core/ui.py`:** Centralized design system engine providing:
  - Dark (SOC Analyst) and Light display themes with exact HEX color palettes.
  - Seamless, non-flickering sidebar theme toggle persisted across multi-page navigation.
  - Text-based security pill badges (`[ALLOW]`, `[REVIEW]`, `[BLOCK]`, `[MASK]`, `[WIPED]`, `[ACTIVE]`).
  - Standardized simulation environment compliance banner.
- **`tests/test_ui.py`:** Unit tests verifying theme token completeness, state getters/setters, CSS generation, and badge generation.
- **UI Tests in `tests/test_pages.py`:** Added automated headless verification for theme switching via `AppTest`.

### Changed
- **`app.py`:** Redesigned into an enterprise operational dashboard with real 4-KPI metrics, device ledger, and heuristic rules reference.
- **`pages/1_MDM_Console.py`:** Implemented split-screen MDM workspace with pending administrative review queue and outbound transmission checker.
- **`pages/2_Permission_Analyzer.py`:** Implemented split layout with package configuration, dynamic category baseline reference, and policy verdict card.
- **`pages/3_DLP_Scanner.py`:** Implemented payload inspection workbench with regex pattern coverage card and zero-retention detected entity offset table.
- **`.streamlit/config.toml`:** Updated base theme to neutral Slate/Sky palette (`#38BDF8`, `#0B0F17`) to eliminate orange color flash.
- **Terminology Refinement:** Replaced misleading labels (`Managed Endpoints` $\rightarrow$ `Simulated Device`, `DLP Interceptions` $\rightarrow$ `DLP Blocked/Masked Events`, `AIR-GAPPED` $\rightarrow$ `LOCAL SIMULATION`).
- Verified WCAG 2.1 Level AA compliance ($\ge 4.5:1$ contrast ratio) across all text tokens.

---

## [v0.2.0] - 2026-10-20: Multi-Page Integration & Test Suite Expansion

### Added
- Multi-page Streamlit application structure: `app.py`, `pages/1_MDM_Console.py`, `pages/2_Permission_Analyzer.py`, `pages/3_DLP_Scanner.py`.
- Automated headless UI testing using Streamlit `AppTest` in `tests/test_pages.py`.
- CSV export for session audit logs.
- Simulated remote wipe and device re-enrolment workflow.

### Fixed
- Fixed benchmark demo buttons ("Load demo example") to reliably populate session state.
- Standardized application name validation via `store.validate_app_name` across pages and backend.
- Expanded DLP regex to detect hyphenated 12-digit IDs (`XXXX-XXXX-XXXX`) and phone numbers with `+91` prefix.
- Added `pytest.ini` with `pythonpath = .` to enable root `pytest` execution without import errors.
- Test suite expanded from 27 to 48 passing tests.

---

## [v0.1.0] - 2026-10-20: Core Heuristics & Engine Contracts

### Added
- Core heuristic engines:
  - `core/analyzer.py`: Permission risk scoring engine with least-privilege category evaluation.
  - `core/dlp.py`: Outbound text scanner detecting cards (Luhn-validated), 12-digit IDs, phone numbers, and emails.
  - `core/rules.py`: Centralized permission weight dictionary and category expected sets.
  - `core/store.py`: In-memory device state management and privacy-safe audit logging.
- Unit test suites: `tests/test_analyzer.py`, `tests/test_dlp.py`, `tests/test_store.py` (27 initial tests).
