# Phases: DLP-style Scanner

## Tuesday (setup)

- Write `scan_text` as a stub returning the contract shape (Allow, no findings), so Person C can start.
- Write the 7 test cases as failing tests.
- Read about the Luhn check and be able to explain it.

Exit: stub returns the right keys, tests exist.

## Wednesday (build)

- Implement the patterns, Luhn, overlap skipping, masking and action rule from trd.md.
- Make all tests pass, including the length and "no value key" tests.
- Build `pages/3_DLP_Scanner.py`.

Exit: all tests pass, page works.

## Thursday (integrate)

- Help Person C connect the send flow.
- Fix false alarms and misses found while testing.
- Add the demo example button.

Exit: the demo message with a phone number is masked and the test card message is blocked, in the console.

## Friday (finish)

- Take screenshots using fake data only.
- Write your report section: problem, detection rules, limits.
- Rehearse a 2-minute explanation of how a card number is checked.

## Saturday

Bug fixes only. No new features.

## If time is short

Cut the standalone page polish first. Then cut masking and keep Block only. Never cut the card and phone detection or the tests.
