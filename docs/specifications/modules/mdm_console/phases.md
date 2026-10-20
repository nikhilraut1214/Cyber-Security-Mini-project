# Phases: MDM Console

## Tuesday (setup and contracts)

- Create the folder, virtual environment, requirements.txt, `.streamlit/config.toml`.
- Create the full folder structure with empty files.
- Confirm A and B have put stubs in `core/analyzer.py` and `core/dlp.py`.
- Run "hello" Streamlit page.

Exit: `streamlit run app.py` opens, imports of both stubs work.

## Wednesday (build the shell)

- Write `store.py` with all functions and its 7 tests.
- Build the console page: device panel, install form, send box, log table, using the stubs.
- Build the home page with counts.

Exit: install and send flows run with stub results. Store tests pass.

## Thursday (integrate)

- Real modules arrive. Check nothing breaks.
- Add the Review flow with Approve and Reject.
- Check the log never shows raw values.
- Run the full demo script.

Exit: the 6-step demo script from the PRD runs end to end.

## Friday (finish)

- Build P2 items if time, in this order: CSV export, dashboard counts, then wipe/re-enrol. If wipe is omitted, remove the wipe step from the demo script and update the report.
- Take screenshots with fake data.
- Write your report section: architecture diagram, flows, limits.
- Rehearse the demo three times.

## Saturday

Bug fixes only. Copy the project to a pen drive and a backup. One last run on the presentation machine.

## If time is short

Follow Part E of rules.md. Never cut the install flow or the audit log.
