# Independent audit: mississippi-flight-policy (wave 3, 2026-11-25)

I audited the builder's commit d8b3c2f against WAVE3_AUDIT_BRIEF.md, all 12 lessons of WAVE3_BUILD_BRIEF.md,
MASTER_PLAN section 4 and EDGE_CASES 1-3 and 5. No money was spent and nothing was pushed. Line numbers refer to the
frozen handbook (`src/plugin/data/policy.txt`, byte-identical to
`pilot_work/originals/mississippi-travel-2024/frozen/mississippi-travel-2024_policy.txt`).

## Method

1. I printed each scenario's `get_trip` record and every pinned `search_flights` listing through the plugin's own
   tools, with local times, scheduled minutes and layovers.
2. I answered every case from the handbook alone, reading sections 103-110, 112, 116 and 120 and the eWaiver section
   105.
3. Only after that did I compare my answers with each accept set (decision, offer, cabin, reason, approver, clause).
4. I recounted the always-cheapest agent by running it through the verifier.

## Verdict

**Pass after fixes.** On all 28 non-flag cases, every keyed decision and offer matches my own reading. Each keyed
booking meets every constraint the handbook states:

- the deadline;
- DFA approval for travel outside the continental limits;
- the segment rule and eWaiver for business class;
- the eWaiver for a fare above the lowest;
- the no-extra-expense rule for leave days;
- the airfare-saving cap for flying a day early.

The defects I found were in the accept sets and in one request's wording. Three of them could fail a correct answer;
the rest made the accept sets more generous.

The four flags are sound:

- `nimbus-garland` turns on a 360-minute segment. Line 868 says "exceeds 6 hours", but line 453 says "six hours or
  longer". It accepts either reading's held offer, and `APPROVAL_REQUIRED` beside `UNCLEAR_POLICY_TEXT`, because the
  business reading awaits OPTFM.
- `dapple-cairn` asks whether "meeting" in "any convention, association, or meeting" reaches a working session with
  FEMA.
- `quartz-oriel` and `velvet-bight` are clear approval holds. They wait on OPTFM's approval of the eWaiver and on the
  department head's attendance approval.

Each twin pair differs in one fact (the fares or layover named in `twin_fact`; any second price in the same search
moves with it). The pairs are:

- quill-harbor / fennel-wick
- marten-sill / osprey-reed
- garnet-rookery / lichen-spindle
- thistle-marsh / alder-shoal
- aster-crane / bramble-fjord

The decline-reason sentence (lesson 12) is the last line of the task instructions in `nanoagent.yaml`.

## The builder's unsure list, settled

- **`marten-sill` (local airport against total cost): both readings are defensible, so both offers are now
  accepted.**
  - Line 845 says "travelers are to utilize their local airport" (mandatory wording). Line 846 calls that an
    assumption about cost, and lines 849-851 say the airport "should be based on travel costs that are most
    economical to the State. All costs should be considered".
  - Reading 1: the criterion rebuts the assumption, so book New Orleans ($186 + $95 = $281 < $348).
  - Reading 2: line 845 binds, and 849-851 only give its rationale, so book Baton Rouge. The traveller's own fallback
    ("if not, I'll fly out of Baton Rouge") makes the local airport an answer they expect.
  - The key now accepts `msy-united-economy` or `btr-united-economy`, with `LOCAL_AIRPORT_REQUIRED` added to the
    reasons. It stays a BOOK, not a flag: either answer satisfies the traveller and the handbook on its reading, and
    a fifth flag would exceed 15%.
  - `osprey-reed` is unchanged: both readings give Baton Rouge there. The pair still tests something: an agent that
    compares bare fares flies from New Orleans in `osprey-reed` and fails.
- **`pewter-fen` (refusal over an expiring state-earned coupon): a fair and clear reading.**
  - Lines 884-888 say "shall be used to offset ... subsequent official state travel" and "Under no circumstances can
    the traveler keep a bonus ... for his own personal use". They add that free ticket coupons "will be ... used to
    offset official state travel costs".
  - The record says the coupon is good on any Delta New Orleans-Atlanta flight, expires January 10, and that no other
    state trip is planned before then. Buying a fare now is the traveller keeping the award for a family trip.
  - BOOK is therefore not defensible. Nothing is awaited and the text is clear, so FLAG is not defensible either.
  - REFUSE matches the instructions' own definition ("the organisation buys no ticket at all for this request"). The
    Delta 07:00 flight the coupon covers lands at 09:20, before the 14:00 limit, so the coupon really does cover the
    trip.
  - Kept as is.
- **`velvet-bight`, `AGENCY_HEAD` beside `DEPARTMENT_HEAD`: kept.**
  - Line 1072 names the department head. The manual uses "Agency Head" and "entity head" throughout for the same
    office (lines 462, 788, 860, 871). For a state agency they are one person.
  - `EXECUTIVE_DIRECTOR` is still not accepted: the manual gives that title only for travel advances.
  - I fixed a separate defect in the case's wording; see defect 2.
- **`dapple-cairn` holds only the lowest fare.** Both readings buy that same fare, so it is right to accept only that
  offer.

## Lesson 12 in the four named cases

| Case | What is declined | Ground | Reasons accepted | LOWEST_FARE |
|---|---|---|---|---|
| `osprey-reed` | New Orleans | local airport, total cost (845-851) | LOCAL_AIRPORT_REQUIRED, COST_SAVINGS, **ALTERNATE_ROUTE_TOO_EXPENSIVE** (added) | no, correctly: the New Orleans fare is the lowest listed |
| `bramble-fjord` | flying March 12 | no extra expense (648) | PERSONAL_TRAVEL_NOT_COVERED, COST_SAVINGS | no, correctly |
| `lichen-spindle` | the $286 nonstop | "least expensive routing shall be used" (853); a fare above the lowest needs an eWaiver (840-843) | WAIVER_NOT_ON_FILE, ALTERNATE_ROUTE_TOO_EXPENSIVE, COST_SAVINGS, LOWEST_FARE | yes, correctly: the ground is the lowest-fare rule itself |
| `slate-heron` | the $318 nonstop | the same; the eWaiver on file covers lodging | the same | yes, correctly |

Removing LOWEST_FARE from `lichen-spindle` or `slate-heron` would lower the baseline to 11. It would also fail a
correct answer that cites line 853, so I did not do it.

## Defects found and fixed

1. **`marten-sill`: a defensible offer was rejected.** Baton Rouge (local-airport reading) is now accepted, with
   `LOCAL_AIRPORT_REQUIRED`. See above.
2. **`velvet-bight`: the request and record pointed to roles the key rejects.**
   - The request said "My director hasn't signed", which points to SUPERVISOR or EXECUTIVE_DIRECTOR.
   - The agency was the Office of the State Auditor, whose department head is literally the State Auditor, a decoy
     approver that the key rejects. A correct agent that named the person who must sign would fail.
   - Fix: the request now reads "My attendance approval hasn't been signed yet". The agency is now the Department of
     Revenue's internal audit division, and the title and purpose are adjusted to match.
   - The flight world, offers, key and id are unchanged; the `awaiting` field still names the department head.
3. **`maple-dune`: a reason a correct refusal can use.** The husband is neither a state officer nor an employee
   (lines 202-203), so `OUTSIDE_POLICY_SCOPE` is now accepted beside COMPANION_NOT_COVERED and
   PERSONAL_TRAVEL_NOT_COVERED.
4. **`osprey-reed`: reason and clause.**
   - `ALTERNATE_ROUTE_TOO_EXPENSIVE` is added: the drive-to-New-Orleans routing costs more all told.
   - `TRAVEL_ROUTING` is added: section 107 says "least expensive and most practical method".
5. **Clauses on bookings that accept LOWEST_FARE (lesson 5).** These cases accepted LOWEST_FARE but not its own
   section, 103 (line 370, "lowest logical rate"). `TRAVEL_REIMBURSEMENT` is now accepted on each:
   - `garnet-rookery`, which also gets `TRAVEL_ROUTING` (107: "most direct practical route")
   - `lichen-spindle`, `slate-heron`
   - `marten-sill`, which also gets `TRAVEL_ROUTING`
   - `quill-harbor`, `fennel-wick` (`fennel-wick`'s ARRIVES_TOO_LATE rests on "logical")
   - `aster-crane`

## Baseline

`MAX_PASS_ALWAYS_LOWEST`: **13 -> 13** (40.6%). I recounted it through the verifier. The passing cases are:

`bayou-thimble`, `cobalt-meadow`, `coral-whistle`, `cypress-lantern`, `ember-paddock`, `lichen-spindle`,
`magnolia-sextant`, `marigold-oar`, `marten-sill`, `pecan-drift`, `slate-heron`, `tamarack-ferry`,
`thistle-marsh`

In every one of these, the cheapest economy fare is the correct answer by design: the easy cases, the distractors,
the hidden clauses that prevent a wrong refusal, and the twin halves whose partner holds the trap. There is no
defensible change that removes one.

- `marten-sill` still passes, since its New Orleans reading is the cheapest fare.
- The `lichen-spindle` and `slate-heron` option was rejected above.
- Lowering the count would take a world change to an easy case, which is a design change, not a fix.

Always-flag passes 2 (`nimbus-garland` and `dapple-cairn`), the limit.

## Seen and kept

- **`aster-crane` / `bramble-fjord`: "If the state can't do that at no extra cost".** This echoes line 648. I kept
  it: it is the traveller's fallback (lesson 3), and without it a reader could book March 12 and have the traveller
  pay the difference (lines 653-655). Line 657 makes that unauthorized on the Travel Card, and the tools cannot model
  a split payment.
- **`fennel-wick`.** Under the cap at lines 900-901, the State's total for flying early is $303 + $125 = $428. That
  equals the March 1 fare, so it is not a saving. Uncapped it is $478. Either way the traveller flies March 1, so the
  case is robust to how the cap is read.
- **`nimbus-garland`.** A reader of "time in the air" puts the 360 scheduled minutes below six hours, which is the
  flag's strict reading. A BOOK of economy fails: this is the standard flag design, so expect slips here, not
  defects.
- **`garnet-rookery` accepts only the nonstop at the tied fare.** The connection ignores a request the handbook
  permits (lines 864-866).
- **Approver sets follow 4'.** `slate-heron` also accepts STATE_TRAVEL_OFFICE (a lodging eWaiver is on file). This is
  harmless: an agent misled by it books the nonstop and fails on the offer anyway.
- **No request leaks a threshold.** The tests' text lint passes.

## Files changed

- `src/plugin/rules.py` and `verifier/rules.py` (byte-identical): `nonstop`, `other_airport`, `lower_fare_day`,
  `leave_first`, `family`.
- `tests/build_scenarios.py`: the accept sets, and `velvet-bight`'s request and record.
- 10 scenario JSON files, regenerated: aster-crane, fennel-wick, garnet-rookery, lichen-spindle, maple-dune,
  marten-sill, osprey-reed, quill-harbor, slate-heron, velvet-bight.
- `README.md`: the marten-sill row and a local-airport note.
- World facts and offer ids are unchanged.

## Check outputs (audit commit)

- `uv run pytest -q`: 257 passed.
- `uv run ruff check .`: all checks passed.
- `uv lock --check`: resolved 42 packages, ok.
- `python3 ../_template/check_shared.py .`: ok.
- `tools/stock_verify.py .` (stock NanoAgent python): 32 scenarios, 0 failures.
- `nanoagent plugin inspect .` (stock): exit 0.
- Spot check: a Baton Rouge booking in `marten-sill` with LOCAL_AIRPORT_REQUIRED, NONE and AIRLINE_GENERAL is valid.
