# Mississippi State Travel Policy Flight Booking

**Source of the handbook:** https://www.dfa.ms.gov/sites/default/files/Office%20of%20Purchasing%2C%20Travel%20and%20Fleet%20Home/Resources%20Manuals%20Guidelines/Travel%20Manual%202024.pdf. The agent reads it verbatim (bundled at `src/plugin/data/policy.txt`); flights, fares and trips are synthetic.

**No affiliation with the State of Mississippi.** The handbook is the Mississippi Department of Finance and
Administration's *State Travel Policy Rules & Regulations* (December 2024), a public state manual, bundled verbatim
for research. Every traveller, office and trip in the scenarios is invented.

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the state's real travel
manual: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and manual section. A deterministic Python verifier,
with no LLM, rebuilds the offers and the manual's answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files.

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 12,334 words, 1,543 lines, 81,172 bytes, sha256 `6f361eff...0e464757`,
equal to `pilot_work/originals/mississippi-travel-2024/frozen/SHA256SUMS`) is never paraphrased, and the task text
restates no rule. Under stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The
`harness.policy` switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to the
system prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins are
meant to run with `query: instructions+input`, so a selector sees the traveller's request.

**Size.** At 1.33 tokens a word the manual alone is about 16,400 tokens; calibrated on the paid Thornton and NJC runs
(about 0.2 tokens a character plus 1,800) the first `full` call is about 18,000 input tokens. A 3-call run
(`get_trip`, `search_flights`, `submit`) is about 56,000 input tokens before the final message and about 75,000 with
it; the six cases that search a second airport or day make 4 calls (about 75,000 before the final message). Under
`full` this crosses the hosted cap of 65,536 total tokens: run it with the ladder's raised cap and report the hosted
cap per arm.

**Airports.** The shared world has no Mississippi airport (no JAN, GPT, PIB, GTR or TUP). Travellers are posted at
duty stations whose local airport is in the world: Picayune, Poplarville and Stennis Space Center (New Orleans,
MSY) and Woodville, Centreville and Gloster (Baton Rouge, BTR). `tests/BUILD_NOTES.md` records the template request.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date, and on the other airport or day the trip
  record names when it names one (every case buys one one-way ticket), then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list plus
  thirteen codes of this manual and ten decoy codes from other handbooks' rules. Fares are in cents of US dollars.
- **Success:** every field is one the answer key accepts; the cabin is graded as the chosen offer's own. Score =
  fields right / 6.
- **Approver.** A booking or refusal accepts `NONE` and the role of every sign-off on file (SYNC_NOTES 4'); a hold
  awaiting a sign-off accepts only the awaited roles.
- **Reasons on a declined request.** When the booking is not what the traveller asked for, the reason names the
  manual's ground: `osprey-reed` (other airport dearer all told) and `bramble-fjord` (leave days cost more) do not
  accept `LOWEST_FARE`; `lichen-spindle` and `slate-heron` (nonstop declined) accept it beside
  `WAIVER_NOT_ON_FILE`, since the ground is the lowest-fare rule itself (lines 840-843, 853).
- **Local airport.** `marten-sill` accepts both airports: New Orleans on the total-cost criterion (lines 849-851),
  or Baton Rouge for a reader who takes "travelers are to utilize their local airport" (line 845) as binding.
  `osprey-reed` is Baton Rouge on both readings.
- **No hidden facts:** no scenario has `answer_key_inputs`.

| Scenario | Category | Expected decision (offer; cabin) | Frozen lines |
|---|---|---|---|
| `bayou-thimble` | easy | BOOK (first-economy; ECONOMY) | 369-370, 557-558 |
| `coral-whistle` | easy | BOOK (atlanta-economy; ECONOMY) | 369-370, 1131-1133 |
| `cypress-lantern` | easy | BOOK (morning-economy; ECONOMY) | 369-370, 557-558, 1072-1074 |
| `heron-quartz` | easy | BOOK (british-business; BUSINESS) | 369-370, 462-466, 868-872, 1131-1133 |
| `magnolia-sextant` | easy | BOOK (atlanta-economy; ECONOMY) | 369-370, 868-872, 1131-1133 |
| `pecan-drift` | easy | BOOK (dallas-economy; ECONOMY) | 369-370, 853 |
| `alder-shoal` | boundary_twin | BOOK (first-economy; ECONOMY) | 368-369, 369-370 |
| `fennel-wick` | boundary_twin | BOOK (first-economy; ECONOMY) | 369-370, 900-901 |
| `garnet-rookery` | boundary_twin | BOOK (united-economy; ECONOMY) | 369-370, 853, 864-866 |
| `lichen-spindle` | boundary_twin | BOOK (dallas-economy; ECONOMY) | 840-843, 853, 857-862, 864-866 |
| `marten-sill` | boundary_twin | BOOK (msy-united-economy or btr-united-economy; ECONOMY) | 369-370, 845-847, 849-851 |
| `osprey-reed` | boundary_twin | BOOK (btr-united-economy; ECONOMY) | 369-370, 845-847, 849-851 |
| `quill-harbor` | boundary_twin | BOOK (afternoon-economy; ECONOMY) | 369-370, 857-862, 900-901 |
| `thistle-marsh` | boundary_twin | BOOK (dallas-economy; ECONOMY) | 368-369, 369-370 |
| `aster-crane` | multi_rule | BOOK (leave-day-southwest; ECONOMY) | 369-370, 642-651 |
| `bramble-fjord` | multi_rule | BOOK (business-day-southwest; ECONOMY) | 369-370, 642-651 |
| `juniper-quoin` | multi_rule | BOOK (southwest-economy; ECONOMY) | 369-370, 462-466, 840-843, 857-862 |
| `sable-tern` | multi_rule | BOOK (american-economy; ECONOMY) | 369-370, 453, 868-872, 1131-1133 |
| `wren-basalt` | multi_rule | BOOK (american-business; BUSINESS) | 462-466, 868-872, 1131-1133 |
| `lupine-grotto` | hidden_clause | BOOK (airfrance-business; BUSINESS) | 471-474, 868-872, 1131-1133 |
| `marigold-oar` | hidden_clause | BOOK (charlotte-economy; ECONOMY) | 369-370, 375-377, 1026-1030 |
| `tamarack-ferry` | hidden_clause | BOOK (minneapolis-economy; ECONOMY) | 249, 369-370, 1145-1146 |
| `cobalt-meadow` | distractor | BOOK (first-economy; ECONOMY) | 369-370, 557-558 |
| `ember-paddock` | distractor | BOOK (minneapolis-economy; ECONOMY) | 369-370, 853 |
| `slate-heron` | distractor | BOOK (dallas-economy; ECONOMY) | 840-843, 853 |
| `hollow-brine` | refusal | REFUSE (none; NONE) | 202-203, 642-651 |
| `maple-dune` | refusal | REFUSE (none; NONE) | 202-203, 642-651, 1026-1030, 1216-1217 |
| `pewter-fen` | refusal | REFUSE (none; NONE) | 884-888 |
| `dapple-cairn` | flag | FLAG_FOR_APPROVAL (first-economy; ECONOMY) | 369-370, 1072-1074 |
| `nimbus-garland` | flag | FLAG_FOR_APPROVAL (american-business, american-economy; BUSINESS, ECONOMY) | 453, 868-872 |
| `quartz-oriel` | flag | FLAG_FOR_APPROVAL (american-business; BUSINESS) | 442, 462-466, 868-872 |
| `velvet-bight` | flag | FLAG_FOR_APPROVAL (philadelphia-economy; ECONOMY) | 369-370, 1072-1074 |

Mix (EDGE_CASES.md 5.2): 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause, 3 distractor, 3 refusal, 4 flags
(12.5%). Decisions: 25 BOOK, 3 REFUSE, 4 FLAG_FOR_APPROVAL. Degenerate agents: always-flag passes 2, always-cheapest
passes 13.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller, duty station and local airport, route, date, landing deadline, other airport or day asked for, purpose, cabin and nonstop wishes, coupon, advance, sign-offs on file and awaited | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date: the pinned scenario offers plus seeded background offers on those searches only; a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-mississippi-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this manual's scenario ids, approvers, sections, reason codes
  and trip record.
- `src/plugin/`: `world.py`, `scenarios.py`, `guide.py`, `answer.py`, `tools.py` (shared), `rules.py` (this
  manual's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of the shared modules and `rules.py`, plus `booking.py` and `tools.py`.
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this manual's settings.
- `tests/build_scenarios.py`: writes the scenario files (an authoring aid, not a test).
- `tests/BUILD_NOTES.md`: design choices, the blind read and the acceptance outputs.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 ../_template/check_shared.py .
# from a NanoAgent checkout (read-only use):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/mississippi-flight-policy.tar.gz
# from this folder, with that checkout's Python:
/path/to/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
