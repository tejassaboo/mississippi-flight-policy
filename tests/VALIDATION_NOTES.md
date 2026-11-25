# Validation notes: mississippi-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/mississippi-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius fp8), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head 9e68450. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

27/32 valid (84.4%), mean field score 0.917, **easy 6/6**. By category: boundary 8/8, distractor 3/3, easy 6/6,
flag 2/4, hidden 3/3, multi 2/5, refusal 3/3. $0.00199 billed per run, 4.0 calls per run, 20,836 prompt tokens per
call; no run would exceed the hosted 65,536 cap.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| sable-tern | multi_rule | FLAG American business VR74-R7WG, APPROVAL_REQUIRED, STATE_TRAVEL_OFFICE; key BOOK American economy 399Y-KMJ3 | model slip | The request makes the segment test the question: "If business can be authorized on this trip, hold ...; if it can't be authorized on this trip at all, book me economy." The model never looked at a segment: "So business class is not yet approved - it's awaiting approval. So we should FLAG_FOR_APPROVAL". Both routings fly via LAX with longest segments of 330 and 335 minutes, so nothing "exceeds 6 hours" (lines 868-869) or is "six hours or longer non-stop" (line 453). The twin quartz-oriel shows the model can run this test when it does read the rule. |
| wren-basalt | multi_rule | BOOK Delta business NPBE-FA88 ($3,180), EWAIVER_APPROVED; key American business QUN5-D92L ($3,420) | model slip | "The lowest business class is Delta NPBE-FA88 ... So BOOK". It never read the segment condition. Delta flies 230 + 335 minutes via LAX; American's DFW-HNL segment is 470 minutes. Lines 868-869 authorise business only "if at least one of the flight segments exceeds 6 hours", and line 870 makes it non-reimbursable otherwise. The approved eWaiver names business class, not a flight, so it does not lift the condition. The cheapest fare that can be authorised is American. |
| quartz-oriel | flag | BOOK Delta economy, LONG_FLIGHT_CONDITION_NOT_MET; key FLAG American business for STATE_TRAVEL_OFFICE | model slip | It quoted lines 868-872 correctly, then checked only the first offer: "MSY-LAX is 230 min (~3.8h), LAX-HNL is 335 min (~5.6h). Neither segment exceeds 6 hours ... So business class cannot be authorized on this trip at all". The same search lists American via DFW with a 470-minute DFW-HNL segment, so business can be authorised on this trip and the eWaiver is still awaited (`awaiting`). The key is right, and the hold is not a reading of unclear text. |
| dapple-cairn | flag | BOOK lowest Delta, LOWEST_FARE, NONE, AIRLINE_GENERAL; key FLAG the same fare, APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT, clause CONFERENCES | model slip | It went straight to the fare: "No sign-offs needed. Decision BOOK." It never opened lines 1072-1074 ("prior written approval from the department head for employee attendance at any convention, association, or meeting"). `sign_offs` is empty, and the purpose is a "Working meeting with FEMA Region 4 staff". Every other MEETING record in the plugin carries the department head's ATTENDANCE sign-off (cypress-lantern, coral-whistle, fennel-wick, quill-harbor ...), so the record is consistent; only site visits and audit fieldwork (bayou-thimble, pecan-drift) carry none. A missing sign-off not seen. |
| bramble-fjord | multi_rule | right offer (March 14 Southwest), approver and clause; reason LEAVE_DAYS_NO_EXTRA_COST; key COST_SAVINGS or PERSONAL_TRAVEL_NOT_COVERED | model slip (code points the wrong way) | It named the ground (lines 642-651, "the state would incur extra cost") and then picked the twin's code by its name, doubting it as it did so: "the code name 'LEAVE_DAYS_NO_EXTRA_COST' reads as a positive statement that leave days are at no extra cost ... But it's the closest match." That code is the BOOK-side code of the twin aster-crane, where the leave day costs nothing extra; here the leave day costs $53 more, so the code states the opposite of the fact. Same treatment as Anixter onyx-grove (COMBINED_TRIP_NO_ADDED_COST on an added-cost case) and LSU catalpa-ferry. PERSONAL_TRAVEL_NOT_COVERED and COST_SAVINGS were both on the list it weighed. |

## Pattern

The three Honolulu twins (sable-tern, wren-basalt, quartz-oriel) all failed on the same test: whether some business
fare in the search has a segment over 6 hours. Twice the model never applied lines 868-869, and once it applied them
to the first routing only. In each case the deciding segment lengths are in the search results it received, and the
key follows the line. The keys are fair and stay as they are. If these three fail again the same way, the lead may
consider whether three cases on one trap is too much weight on one line; that is a coverage call, not a key change.

## Fixes

None. No record, request or accept set changed. Not loosened: bramble-fjord (the code states the opposite of the
case), and the four decision failures.

## Q2

The always-cheapest agent passes **13/32 (40.6%)** (`MAX_PASS_ALWAYS_LOWEST = 13`), unchanged and at the ~40% ceiling.

## Re-score at this head

27/32, easy 6/6 (no change; nothing was fixed).

## Re-run

Required: none (no record or request changed, and no easy case failed). Optional, for variance: sable-tern,
wren-basalt and quartz-oriel (the shared segment trap).

## Checks

`uv run pytest -q` (257 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`, `tools/stock_verify.py` (32
scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
