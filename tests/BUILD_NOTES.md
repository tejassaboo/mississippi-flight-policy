# Build notes: mississippi-flight-policy (wave 3, 2026-11-24)

Built from `_template` with `instantiate.py` (slug `mississippi-travel-2024`, `--task-id book-mississippi-flight`,
`--currency USD`, `--background 0`, `--scenarios 32`). Frozen handbook:
`pilot_work/originals/mississippi-travel-2024/frozen/mississippi-travel-2024_policy.txt`, 12,334 words (over 10,000,
so 32 scenarios), 1,543 lines, sha256 `6f361eff...0e464757`. Decisions were taken without asking (the lead was
away); each is recorded here.

## 1. What the handbook supports

Mandatory or checkable flight clauses (frozen line numbers):

| Lines | Clause | Operator / force | Used by |
|---|---|---|---|
| 368-370 | minimum cost; "shall utilize the lowest logical rate available" | mandatory | every booking |
| 557-558 | least expensive and most practical method | should | easy cases |
| 840-843 | a fare above the lowest needs an eWaiver submitted to OPTFM before booking | mandatory | juniper-quoin, lichen-spindle, slate-heron |
| 845-851 | use the local airport (assumed most economical); the airport is chosen on the costs most economical to the State, all costs considered | mandatory + criterion | marten-sill, osprey-reed |
| 853 | "The least expensive routing shall be used." | mandatory | lichen-spindle, slate-heron, pecan-drift |
| 857-862 | alternate dates should be considered; other routing needs the agency head and an eWaiver | should / mandatory | juniper-quoin, quill-harbor |
| 864-866 | "Choose the flight with the fewest stops" | imperative | garnet-rookery (tie only) |
| 868-872 | business/first/preferred seat may be authorized if a segment "exceeds 6 hours"; not reimbursable unless an eWaiver signed by the agency head is approved by OPTFM before the trip | strict, per segment | heron-quartz, sable-tern, wren-basalt, quartz-oriel, nimbus-garland |
| 453 | the eWaiver form's reason: business "(six hours or longer non-stop)" | inclusive | nimbus-garland (the conflict) |
| 471-474 | universities do not submit eWaivers; they follow their own waiver procedure | scope | lupine-grotto |
| 642-656 | business and personal leave combined only when the primary purpose is state business, leave is approved and the agency incurs no extra expense | mandatory ("all of the following") | aster-crane, bramble-fjord, hollow-brine |
| 884-888 | state-earned bonuses offset later state travel; never kept for personal use; free coupons used for official travel | shall / "under no circumstances" | pewter-fen |
| 900-901 | a day early for a lower penalty fare: added lodging and meals paid "not to exceed the amount of savings in the airfare" | inclusive cap | quill-harbor, fennel-wick |
| 1072-1074 | department head's prior written approval for "attendance at any convention, association, or meeting" | mandatory for reimbursement | velvet-bight, dapple-cairn, every conference booking |
| 1131-1133, 1145-1146, 249 | DFA approves travel outside the continental limits (Canada, Hawaii, Puerto Rico, Mexico outside; Alaska within; universities excluded) | mandatory | magnolia-sextant, coral-whistle, heron-quartz, sable-tern, wren-basalt, tamarack-ferry, lupine-grotto |
| 375-377, 1026-1030 | board members on a per diem in lieu of salary are officers of the state; the cardless account books non-entity travellers on official business | scope | marigold-oar |
| 202-203, 1216-1217 | the rules cover state officers and employees; a family member along: single room rate only | scope | maple-dune |

Not used as rules (no checkable flight outcome): the Trip Optimizer (under moratorium, motor vehicles), the
driving-vs-flying cap (786-824, a reimbursement cap for drivers; used as a distractor), the two-fare cost comparison
for non-agency bookings (834-838, paperwork; distractor), penalty and change fees, baggage, flight insurance. The
manual has no rule on several employees on one flight and none on overnight stops, so the `multi_traveller` and
overnight overlays are not required (plugin_spec `OVERLAY_MINIMUMS`). It never mentions premium economy, so no
scenario asks for it. Every case buys one one-way ticket; the trip record has no return date.

## 2. Unclear points and how they are handled

- **"exceeds 6 hours" (lines 868-869) against "six hours or longer non-stop" (line 453).** Two duration rules,
  `segment` (> 360) and `waiver-form` (>= 360). They differ only on a longest segment of exactly 360 minutes: flag
  `nimbus-garland` (Los Angeles-Honolulu at 360 minutes, the agency head's eWaiver awaiting OPTFM). Its hold accepts
  either reading's offer (American business held for OPTFM, or the lowest economy fare), `UNCLEAR_POLICY_TEXT` or
  `APPROVAL_REQUIRED`, approver `NOT_NAMED` or `STATE_TRAVEL_OFFICE`. Twins: `sable-tern` (330/335 minutes: book
  economy) and `wren-basalt` (470 minutes, eWaiver approved: book business).
- **"time in the air" (line 869) against scheduled minutes.** The world gives only scheduled minutes, which include
  taxi time. Every other scenario keeps its longest segment at least 25 minutes from 360 (330, 335, 355 on the
  non-qualifying side; 440, 470, 525, 535, 555, 560, 590 on the qualifying side), so a reader who subtracts taxi time
  reaches the same answer. At exactly 360 scheduled minutes, a time-in-the-air reader is on the "does not qualify"
  side, which is one of the flag's two readings.
- **"attendance at any convention, association, or meeting" (lines 1072-1073).** The section is headed Conferences;
  whether "meeting" reaches a working session with a partner agency is unclear. Flag `dapple-cairn` (working meeting
  with FEMA, no approval on file): hold the lowest fare; reasons `UNCLEAR_POLICY_TEXT` or `APPROVAL_REQUIRED`;
  approver `NOT_NAMED`, `DEPARTMENT_HEAD` or `AGENCY_HEAD`. Twins `cypress-lantern` (a meeting with the approval on
  file: book) and `bayou-thimble` (a factory inspection, no approval: book). To keep the phrase in one scenario, every
  other meeting, hearing, training or conference trip carries the department head's written approval, and the trips
  without it are inspections and audit fieldwork.
- **Approval required** (`velvet-bight`, a conference, the attendance approval asked for and not signed): hold the
  lowest fare for `DEPARTMENT_HEAD` or `AGENCY_HEAD` (the manual says "department head"; readers equate the two).
  (`quartz-oriel`, a 470-minute segment, eWaiver awaiting OPTFM): hold American business for `STATE_TRAVEL_OFFICE`.
  Both are approval holds, never "no compliant offer".
- **Local airport (lines 845-851).** "travelers are to utilize their local airport" is followed by "Use of the local
  airport is assumed to result in travel costs that are most economical" and "The criteria for determining which
  airport ... should be based on travel costs that are most economical to the State. All costs should be
  considered". I read the assumption as rebuttable by the stated criterion: `marten-sill` books New Orleans when its
  fare plus the coordinator's estimate of added mileage, parking and staff time ($281) is well under Baton Rouge's
  $348; `osprey-reed` keeps Baton Rouge when it is not ($384). Margins are $67 and $36, never equal. Listed under
  "unsure" below.
- **Fewest stops (lines 864-866) against least expensive routing (line 853).** Not flagged: avoided. The nonstop is
  booked only when it is also the lowest fare (`garnet-rookery`); a dearer nonstop needs an eWaiver (lines 840-843),
  which is mandatory, so `lichen-spindle` and `slate-heron` book the connection. The rules raise on any tie between
  different stop counts outside a nonstop wish.
- **eWaiver submitted vs approved (lines 840-843 say "submit ... prior to booking", lines 442 and 465 speak of
  approval).** Avoided for fares: every fare eWaiver in a scenario is either approved or absent. For business the
  text is clear ("approved by OPTFM prior to the trip").
- **International approval timing ("prior to departure").** Avoided: every case outside the continental limits has
  DFA's approval on file, except the university case (excluded) and Alaska (within).

## 3. Choices made without asking

1. **Airports.** No Mississippi airport is in the shared world. Travellers sit at duty stations whose local airport
   exists: Picayune, Poplarville, Stennis Space Center (MSY) and Woodville, Centreville, Gloster (BTR). See section 7.
2. **Deadline.** Every trip record has `must_land_by` (lesson 4); "logical" (line 370) excludes seated offers that
   land after it. `alder-shoal`, `quill-harbor` and `fennel-wick` turn on it, with margins of 20 minutes or more.
3. **Approver sets (SYNC_NOTES 4').** A booking or refusal accepts `NONE` and the role of every sign-off on file
   (relied on or not); a hold awaiting a sign-off accepts only the awaited roles; an unclear hold adds `NOT_NAMED`.
4. **Reasons on declined requests (lesson 12).** `osprey-reed` (local airport kept) accepts `LOCAL_AIRPORT_REQUIRED`
   or `COST_SAVINGS`, not `LOWEST_FARE` (the New Orleans fare is lower). `bramble-fjord` (leave day dearer) accepts
   `PERSONAL_TRAVEL_NOT_COVERED` or `COST_SAVINGS`. `sable-tern` (business not authorized) accepts
   `LONG_FLIGHT_CONDITION_NOT_MET` or `UPGRADE_NOT_ELIGIBLE`. `lichen-spindle` and `slate-heron` (dearer nonstop
   without an airfare eWaiver) accept `LOWEST_FARE` beside `WAIVER_NOT_ON_FILE`, `ALTERNATE_ROUTE_TOO_EXPENSIVE` and
   `COST_SAVINGS`, because the ground is the lowest-fare rule itself (lines 840-843, 853). `fennel-wick` (day early
   not cheaper overall) and `alder-shoal` (cheapest lands late) accept `LOWEST_FARE` with `COST_SAVINGS` /
   `ARRIVES_TOO_LATE`: the request is conditional on cost or time and the ground is the lowest logical fare.
5. **Permitted requests win ties.** `garnet-rookery` accepts only the nonstop at the tied fare; `aster-crane` only the
   leave-day flight at the tied fare (the business-day flight at the same price ignores a permitted request).
6. **Clauses.** Lowest-fare bookings accept `TRAVEL_REIMBURSEMENT` (line 370), `PUBLIC_CARRIER` and
   `AIRLINE_GENERAL` (section 110.A), `TRAVEL_ROUTING` (lines 557-558). A booking with the attendance approval on file
   also accepts `CONFERENCES`. Section headings carry their numbers in the text ("110. Public Carrier (Airplane)");
   the clause codes are digit-free.
7. **Decoy reason codes** (grepped; none has a subject in the text): WEEKEND_TRAVEL_HOME, WEEKEND_TRIP_NOT_EARNED,
   NEXT_OF_KIN_TRAVEL, FLY_AMERICA_US_CARRIER_REQUIRED, OPEN_SKIES_AGREEMENT, CREATIVE_TICKETING,
   EXTENDED_TRAVEL_SAVINGS, CHANCELLOR_WRITTEN_AUTHORIZATION, DOUBLE_BOOKING_PROHIBITED, CANDIDATE_TRIP_NOT_COVERED.
   Left out: SAME_CLASS_AS_CUSTOMER ("customers" occurs at line 905), PRIVATE_AIRCRAFT_NOT_APPROVED (private
   airplanes at line 664), DENIED_BOARDING_NOT_ALLOWED (an Overbooked Flights section exists). Approver decoys:
   SUPERVISOR, CHIEF_FINANCIAL_OFFICER, STATE_AUDITOR.
8. **Background offers** are 0 except `bayou-thimble` and `pecan-drift` (2 each), plain cheapest-economy cases where
   background fares (floored far above) cannot change the answer.
9. **Board member** (`marigold-oar`): the record says the member is paid a daily allowance instead of a salary, so
   lines 375-377 ("officers of the state") apply on every reading.

## 4. Mix and overlays

6 easy, 8 boundary_twin, 5 multi_rule, 3 hidden_clause, 3 distractor, 3 refusal, 4 flag (12.5%). Decisions: 25 BOOK
(3 business, 22 economy), 3 REFUSE, 4 FLAG (2 unclear, 2 approval). Boundary pairs: day-early saving against added
lodging and meals (quill-harbor / fennel-wick), other airport's total cost (marten-sill / osprey-reed), nonstop fare
tied or $45 above (garnet-rookery / lichen-spindle), connection landing before or after the deadline (thistle-marsh /
alder-shoal); fact twins aster-crane / bramble-fjord (leave-day fare). Overlays: multi_leg 15, outside_air_section
16, dearer_option 8, date_arithmetic 6 (month_end 2: February 28 to March 1, 2027), personal_travel 3,
upgrade_not_taken 2. Degenerate agents: always-flag passes 2 (the two unclear flags), always-cheapest passes 13 of
32 (MAX_PASS_ALWAYS_LOWEST = 13, its real count).

## 5. Independent blind read (non-flag scenarios)

Re-derived from the frozen text and the tool outputs only (trip record plus every `search_flights` listing the case
pins, dumped per scenario), not from rules.py, then compared with `expected`.

| Scenario | My reading from text + offers | Agrees |
|---|---|---|
| cypress-lantern | 06:10 $172 sold out; DL 09:00 $189 is the lowest logical rate (370) | yes |
| bayou-thimble | AA 06:00 $236 lands 07:15; refundable $318 dearer | yes |
| magnolia-sextant | Amsterdam needs DFA approval (1131), on file; economy asked; DL via ATL $798 | yes |
| heron-quartz | 555 and 440 min segments > 360; eWaiver signed and OPTFM-approved (868-872); cheapest business BA $5,980 | yes |
| coral-whistle | Puerto Rico outside (1131), DFA on file; DL via ATL $388 | yes |
| pecan-drift | no nonstop wish; least expensive routing (853): AA via DFW $259 | yes |
| quill-harbor | logical Mar 1 low $428 (UA $139 lands 15:10 > 12:00); Feb 28 $163 saves $265 > $175 extra (900-901): Feb 28 | yes |
| fennel-wick | Feb 28 $303 saves $125 < $175: fly Mar 1, AA 06:00 $428 | yes |
| marten-sill | MSY $186 + $95 = $281 < BTR $348; 849-851 most economical: MSY UA | yes |
| osprey-reed | MSY $289 + $95 = $384 > $348: local airport BTR UA $348 | yes |
| garnet-rookery | UA nonstop $241 = AA connection $241: fewest stops (864-866), UA | yes |
| lichen-spindle | nonstop $286 > $241, no airfare eWaiver (840-843, 853): AA via DFW | yes |
| thistle-marsh | AA via DFW $214 lands 10:50 < 11:30 | yes |
| alder-shoal | AA lands 12:20, DL 09:30 lands 11:50, both late: DL 06:00 $268 | yes |
| juniper-quoin | agency head routing + OPTFM eWaiver for the nonstop (859-862, 840-843): cheapest nonstop WN $322 | yes |
| sable-tern | longest segments 330/335 < 360: business cannot be authorized; economy AA $642 | yes |
| aster-crane | Mar 12 $236 = Mar 14 low $236, leave approved, own hotel (642-651): Mar 12 WN | yes |
| bramble-fjord | Mar 12 $289 > $236: extra expense; Mar 14 WN $236 | yes |
| wren-basalt | approved; DL business $3,180 has no segment > 360; AA via DFW (470) business $3,420 | yes |
| tamarack-ferry | Alaska within the continental limits (1145-1146, 249): no DFA approval; DL via MSP $498 | yes |
| lupine-grotto | university: own waiver (471-474), no DFA approval (1132); 590/535 > 360; AF business $4,860 | yes |
| marigold-oar | board member on per diem in lieu of salary = officer of the state (375-377); AA via CLT $287 | yes |
| cobalt-meadow | the unrestricted-fare cap is for drivers (786-792); AA 06:45 $257 | yes |
| ember-paddock | the advance rules (389-395) do not touch the ticket; DL via MSP $288 | yes |
| slate-heron | the OPTFM eWaiver covers lodging (1099-1103), not airfare; AA via DFW $246 | yes |
| hollow-brine | primary purpose personal (642-644): refuse | yes |
| maple-dune | husband is not an officer or employee on state business (202-203, 1028, 1216-1217): refuse | yes |
| pewter-fen | state-earned coupon must offset this trip (884-888), expires before any other trip: refuse | yes |

28 of 28 non-flag scenarios agree.

## 6. Hosted-cap estimate

Full-handbook prompt: 81,172 bytes; about 16,400 tokens at 1.33 a word, about 18,000 on the Thornton/NJC
calibration (0.2 a character plus 1,800) per `full` call. A 3-call run is about 56,000 input tokens before the final
message and about 75,000 with it; the 6 cases that search a second airport or day make 4 calls (about 75,000 before
the final message). Under `full` the run crosses the hosted 65,536 total-token cap (like Anixter's 4-call cases):
run with the ladder's raised cap and report the hosted cap per arm (MASTER_PLAN Q3).

## 7. Template change requests

- **Mississippi airports.** Add JAN (Jackson-Medgar Wiley Evers, 32.3112, -90.0759, -360), GPT (Gulfport-Biloxi,
  30.4073, -89.0701, -360), and optionally PIB, GTR, TUP, MEI, plus MEM, BHM and MOB (the manual names New Orleans,
  Memphis, Mobile and Birmingham at line 820). No new hubs, so no existing route's offers move; run
  `tools/world_diff.py`. With JAN in the world, most scenarios here could start at Jackson (DFA's own city); that
  changes their pinned worlds and needs a re-audit, so it is left for later.
- Observation, no change requested: the skeleton's `search-flights` task text says "one-way"; kept, since every case
  here is one-way.

## 8. Unsure

- `marten-sill`: the local-airport clause read as rebuttable by its own total-cost criterion (lines 849-851). A
  strict reader of "travelers are to utilize their local airport" would book Baton Rouge. If a paid run shows that
  split, convert it to a flag (it would then be the fifth flag, over 15% of 32, so swap it with a non-flag) or drop
  the other-airport pair.
- `pewter-fen`: REFUSE because the coupon covers this trip and expires before any other state trip. A reader might
  book and tell the traveller to use the coupon later; the record rules that out, but the coupon-as-refusal framing
  is new.
- `velvet-bight` approver: the manual says "department head"; `AGENCY_HEAD` is accepted beside it. `EXECUTIVE_DIRECTOR`
  (who approves advances) is not.
- `dapple-cairn` keeps the lowest fare as the only held offer; reading B books that same fare, so no second offer.

## 9. Acceptance outputs

```
$ uv run pytest -q
257 passed in 3.08s
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 12ms
$ python3 ../_template/check_shared.py .
: ok
$ nanoagent plugin inspect .
ok (exit 0)
$ nanoagent plugin pack . /private/tmp/claude-501/-Users-tejassaboo-Code-Rice-COMP580/8e2b1c45-e5c0-4068-ac61-31be3ef811f5/scratchpad/mississippi-flight-policy.tar.gz
packed . into /private/tmp/claude-501/-Users-tejassaboo-Code-Rice-COMP580/8e2b1c45-e5c0-4068-ac61-31be3ef811f5/scratchpad/mississippi-flight-policy.tar.gz (191493 bytes)
$ python ../_template/tools/stock_verify.py .
alder-shoal          right=True score=1.00 identical=True wrong-decision-rejected=True
aster-crane          right=True score=1.00 identical=True wrong-decision-rejected=True
bayou-thimble        right=True score=1.00 identical=True wrong-decision-rejected=True
bramble-fjord        right=True score=1.00 identical=True wrong-decision-rejected=True
cobalt-meadow        right=True score=1.00 identical=True wrong-decision-rejected=True
coral-whistle        right=True score=1.00 identical=True wrong-decision-rejected=True
cypress-lantern      right=True score=1.00 identical=True wrong-decision-rejected=True
dapple-cairn         right=True score=1.00 identical=True wrong-decision-rejected=True
ember-paddock        right=True score=1.00 identical=True wrong-decision-rejected=True
fennel-wick          right=True score=1.00 identical=True wrong-decision-rejected=True
garnet-rookery       right=True score=1.00 identical=True wrong-decision-rejected=True
heron-quartz         right=True score=1.00 identical=True wrong-decision-rejected=True
hollow-brine         right=True score=1.00 identical=True wrong-decision-rejected=True
juniper-quoin        right=True score=1.00 identical=True wrong-decision-rejected=True
lichen-spindle       right=True score=1.00 identical=True wrong-decision-rejected=True
lupine-grotto        right=True score=1.00 identical=True wrong-decision-rejected=True
magnolia-sextant     right=True score=1.00 identical=True wrong-decision-rejected=True
maple-dune           right=True score=1.00 identical=True wrong-decision-rejected=True
marigold-oar         right=True score=1.00 identical=True wrong-decision-rejected=True
marten-sill          right=True score=1.00 identical=True wrong-decision-rejected=True
nimbus-garland       right=True score=1.00 identical=True wrong-decision-rejected=True
osprey-reed          right=True score=1.00 identical=True wrong-decision-rejected=True
pecan-drift          right=True score=1.00 identical=True wrong-decision-rejected=True
pewter-fen           right=True score=1.00 identical=True wrong-decision-rejected=True
quartz-oriel         right=True score=1.00 identical=True wrong-decision-rejected=True
quill-harbor         right=True score=1.00 identical=True wrong-decision-rejected=True
sable-tern           right=True score=1.00 identical=True wrong-decision-rejected=True
slate-heron          right=True score=1.00 identical=True wrong-decision-rejected=True
tamarack-ferry       right=True score=1.00 identical=True wrong-decision-rejected=True
thistle-marsh        right=True score=1.00 identical=True wrong-decision-rejected=True
velvet-bight         right=True score=1.00 identical=True wrong-decision-rejected=True
wren-basalt          right=True score=1.00 identical=True wrong-decision-rejected=True
32 scenarios, 0 failures
```
