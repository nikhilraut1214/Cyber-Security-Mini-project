# Mobile Data Leakage Prevention Console

A Python/Streamlit course-project simulation of an MDM-style console and DLP-style text scanner.

## Important scope and safety
- This repository folder contains project specifications/context documents; it is not the application source code.
- The app is a simulation only. It does not manage real phones, install apps, or transmit messages.
- Use synthetic demo data only. Never enter or store real personal, payment-card, or identity data.
- Permission scores are illustrative team-defined rules, not proof of data leakage.

## Read the documents
1. `prd.md` — goals, scope, acceptance criteria and demo.
2. `trd.md` — folder structure, frozen function contracts and tests.
3. `rules.md` — implementation and safety rules.
4. `design.md` — screen layouts and wording.
5. `phases.md` — implementation sequence and cut order.
6. `memory.md` — decisions, ownership and current progress.
7. `modules/` — module-specific contracts and plans.

## Intended implementation setup
After the application files described in `trd.md` have been created, install dependencies with `pip install -r requirements.txt`, run tests with `pytest`, and start the app with `streamlit run app.py`. The app can run offline after dependencies are installed.

## Shared contracts
Do not change `analyze_app`, `scan_text`, or `store.py` contracts without agreement from all three team members and updates to all affected tests and documents.
