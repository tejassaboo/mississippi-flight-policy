"""Writes the Mississippi scenario JSON files (an authoring aid, not a test; the JSON files are the truth).

    uv run python tests/build_scenarios.py

Expected answers are hand-written here; tests/test_scenarios.py checks them against rules.solve.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

POLICY = (ROOT / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = ROOT / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def aside(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses the answers rest on -----
LOWEST = keep(369, 370, "Travelers shall request air, train, bus, hotel, and vehicle rental reservations as far in "
              "advance as possible and shall utilize the lowest logical rate available.",
              "the default: the lowest logical rate available")
MINIMUM = keep(368, 369, "Travel for business should be conducted at a minimum cost to achieve the success of the "
               "mission.", "business travel at a minimum cost that still achieves the mission")
METHOD = keep(557, 558, "The least expensive and most practical method of transportation should be used.",
              "the least expensive and most practical method")
ABOVE_LOWEST = keep(840, 843, None, "a fare above the lowest on the comparison needs an eWaiver before booking")
LEAST_ROUTING = keep(853, 853, "The least expensive routing shall be used.", "the least expensive routing")
OTHER_ROUTING = keep(857, 862, None, "alternate dates should be considered; other routing needs the agency head and "
                     "an eWaiver to OPTFM")
STOPS = keep(864, 866, None, "'direct' is not nonstop; choose the flight with the fewest stops")
CABIN = keep(868, 872, None, "business only if a segment exceeds 6 hours, approved in advance by an eWaiver the "
             "agency head signs and OPTFM approves")
FORM = keep(453, 453, None, "the eWaiver reason for business: six hours or longer non-stop")
WAIVER_SIGN = keep(462, 466, None, "the eWaiver is signed by the entity head and approved by the State Travel Office")
WAIVER_PRIOR = keep(442, 442, None, "the eWaiver is submitted for approval before reservations")
UNIVERSITY = keep(471, 474, None, "universities do not submit eWaivers and follow their own waiver procedures")
LOCAL = keep(845, 847, None, "travellers use their local airport, assumed most economical")
ECONOMICAL = keep(849, 851, None, "the airport is chosen on the costs most economical to the State, all costs "
                  "considered")
DAY_EARLY = keep(900, 901, None, "going a day early for a lower penalty fare: added lodging and meals paid up to "
                 "the airfare saving")
COMBINE = keep(642, 651, None, "business and personal leave combined only when the primary purpose is state "
               "business, leave is approved and the agency incurs no extra expense")
OUTSIDE = keep(1131, 1133, "All travel outside the continental limits of the United States (Canada, Hawaii, Puerto "
               "Rico, and Mexico are outside) must be approved by the Department of Finance and Administration "
               "(excluding Universities) prior to departure.", "DFA approves travel outside the continental limits")
ALASKA = keep(1145, 1146, None, "Alaska is within the continental limits")
INTL_DEF = keep(249, 249, None, "international travel: areas other than the 48 contiguous states and Alaska")
CONFERENCE = keep(1072, 1074, None, "the department head's prior written approval for attendance at any convention, "
                  "association, or meeting")
AWARD = keep(884, 888, None, "bonuses from state travel offset later state travel; free ticket coupons are used for it")
BOARD = keep(375, 377, None, "board members on a per diem in lieu of salary are officers of the state")
CARDLESS = keep(1026, 1030, None, "the cardless account books non-entity travellers on official state business")
COVERED = keep(202, 203, "All rules and regulations contained herein apply to all state officers and employees.",
               "the rules cover state officers and employees")
FAMILY = keep(1216, 1217, None, "a family member along: the employee claims the single room rate only")

# ----- nearby clauses that must not change the answer -----
DRIVE = aside(786, 792, "shall not exceed the cost of the lowest unrestricted airfare",
              "a cap on driving expenses, not the fare to buy when flying")
UNRESTRICTED = aside(309, 312, "Unrestricted airfares allow for refunds and changes in travel dates without penalties.",
                     "a definition, not a fare the traveller must buy")
ADVANCE = aside(389, 395, "An advance will not be issued earlier than 20 days before the travel start date.",
                "the advance's timing and approval, not the ticket's")
HOTEL_WAIVER = aside(1099, 1103, "An eWaiver request form is required for any lodging reimbursement greater than the "
                     "conference rate or when an employee stays somewhere other than the conference hotel",
                     "a lodging eWaiver, which says nothing about the airfare")
COMPARISON = aside(834, 838, "the state agency must maintain in its files a cost comparison showing a minimum of two "
                   "(2) fares", "paperwork for bookings outside the contract agencies; it does not pick the fare")
STATUS = aside(968, 971, "Check the status of your flight directly with the airline at least 24 hours prior to "
               "departure (48 hours for international flights).", "a tip with hours, not a cabin rule")
CHANGES = aside(920, 921, "If the change is for personal reasons, the State will not reimburse any fees imposed by the "
                "airline or the travel agency.", "fees for later changes, not the purchase")
OPTIMIZER = aside(562, 567, "where the travel will exceed one hundred (100) miles per day",
                  "a motor-vehicle rule under moratorium, not a flight rule")
CURRENCY = aside(1171, 1173, "When converting foreign currency to dollars for the purpose of reimbursement",
                 "a voucher rule for foreign currency, not a fare rule")

# ----- builders -----


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "passenger": "STATE_EMPLOYEE",
        "board_allowance_instead_of_salary": False, "accompanies": "", "agency": "", "duty_station": "Picayune, MS",
        "local_airport": "MSY", "origin": "MSY", "destination": "", "travel_date": "", "must_land_by": "",
        "other_origin": "", "other_origin_added_cents": 0, "other_date": "", "other_date_kind": "NONE",
        "other_date_added_cents": 0, "leave_approved": False, "booking_date": "", "purpose": "",
        "purpose_kind": "MEETING", "requested_cabin": "ECONOMY", "wants_nonstop": False, "free_ticket_coupon": "",
        "travel_advance_cents": 0, "sign_offs": [], "awaiting": "",
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    return base


def sign(role, name, subject, covers="THE_TRIP"):
    return {"role": role, "name": name, "subject": subject, "covers": covers}


def attend(name):
    return sign("DEPARTMENT_HEAD", name, "ATTENDANCE")


def dfa():
    return sign("DFA", "Department of Finance and Administration", "TRAVEL_AUTHORIZATION")


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": slots, "cabins": cabins, "reason_codes": sorted(reasons),
            "approvers": sorted(approvers), "clauses": sorted(clauses), "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers, background=0, name="main"):
    # Background offers only where no background routing could change the answer (handbook.json
    # background_offers is 0, so a search the scenario does not pin lists nothing).
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": background, "flights": flights, "offers": offers}


S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=()):
    S.append({
        "id": id, "category": category, "overlays": list(overlays), "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": list(searches)}, "expected": exp, "must_keep": list(must_keep),
        "distractors": list(distractors), "design_notes": notes,
    })


LOW_CLAUSES = ["AIRLINE_GENERAL", "PUBLIC_CARRIER", "TRAVEL_REIMBURSEMENT", "TRAVEL_ROUTING"]
AIR = ["AIRLINE_GENERAL", "PUBLIC_CARRIER"]
CABIN_CLAUSES = ["AIRLINE_GENERAL", "EWAIVER_REQUEST_FORM", "PUBLIC_CARRIER"]
INTL = ["APPROVAL_FORMS", "INTERNATIONAL_TRAVEL"]
LONG_OK = ["EWAIVER_APPROVED", "INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"]
NOT_MET = ["LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"]
DECLINED_NONSTOP = ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "COST_SAVINGS", "LOWEST_FARE", "WAIVER_NOT_ON_FILE"]

# ===== easy (6) =====

scenario(
    "cypress-lantern", "easy", [],
    "I need to fly New Orleans to Atlanta on December 14th for the air-permit coordination meeting at the EPA "
    "regional office. Economy, cheapest please.",
    trip(traveller_name="Denise Faulkner", traveller_title="Environmental Engineer III",
         agency="Department of Environmental Quality, Picayune field office", destination="ATL",
         travel_date="2026-12-14", must_land_by="2026-12-14 17:00", booking_date="2026-11-30",
         purpose="Air-permit coordination meeting at the EPA regional office in Atlanta",
         sign_offs=[attend("Executive Director, Department of Environmental Quality")]),
    [search("MSY", "ATL", "2026-12-14", {
        "early": {"carrier": "DL", "depart": "06:10"},
        "morning": {"carrier": "DL", "depart": "09:00"},
        "afternoon": {"carrier": "DL", "depart": "13:30"},
        "charlotte": {"carrier": "AA", "via": ["CLT"], "depart": "07:30", "layovers": [65]},
    }, [
        offer("early-economy", "early", "ECONOMY", 17200, seats=False),
        offer("morning-economy", "morning", "ECONOMY", 18900),
        offer("afternoon-economy", "afternoon", "ECONOMY", 22600),
        offer("charlotte-economy", "charlotte", "ECONOMY", 24100),
    ])],
    expected("BOOK", ["morning-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["DEPARTMENT_HEAD", "NONE"],
             [*LOW_CLAUSES, "CONFERENCES"]),
    [LOWEST, METHOD, CONFERENCE],
    "A short domestic trip: the lowest logical rate (line 370). The cheaper 06:10 fare is sold out. The department "
    "head's written approval of the meeting is on file (lines 1072-1073), so the approver is that role or NONE.")

scenario(
    "bayou-thimble", "easy", [],
    "Baton Rouge to Dallas on January 12th for the factory inspection of the new hatchery aeration equipment. Cheapest "
    "economy is fine.",
    trip(traveller_name="Marcus Thibodeaux", traveller_title="Fisheries Biologist II", duty_station="Woodville, MS",
         local_airport="BTR", origin="BTR", agency="Department of Wildlife, Fisheries and Parks, Woodville hatchery",
         destination="DFW", travel_date="2027-01-12", must_land_by="2027-01-12 14:00", booking_date="2026-12-28",
         purpose="Factory acceptance inspection of hatchery aeration equipment in Dallas",
         purpose_kind="SITE_INSPECTION"),
    [search("BTR", "DFW", "2027-01-12", {
        "first": {"carrier": "AA", "depart": "06:00"},
        "houston": {"carrier": "UA", "via": ["IAH"], "depart": "07:05", "layovers": [70]},
        "mid": {"carrier": "AA", "depart": "10:15"},
        "late": {"carrier": "AA", "depart": "15:40"},
    }, [
        offer("first-economy", "first", "ECONOMY", 23600),
        offer("houston-economy", "houston", "ECONOMY", 26200),
        offer("mid-economy", "mid", "ECONOMY", 25100),
        offer("late-economy", "late", "ECONOMY", 31800, refundable=True),
    ], background=2)],
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["NONE"], LOW_CLAUSES),
    [LOWEST, METHOD],
    "The lowest logical rate (line 370): the 06:00 American nonstop lands well before the inspection. The refundable "
    "fare is dearer. A factory inspection is not a convention, association or meeting, and no sign-off is on file.")

scenario(
    "magnolia-sextant", "easy", ["multi_leg", "upgrade_not_taken", "outside_air_section"],
    "New Orleans to Amsterdam on February 2nd for the port investor meetings. Economy is fine, the cheapest one please.",
    trip(traveller_name="Lauren Okafor", traveller_title="International Trade Manager",
         agency="Mississippi Development Authority, Gulf ports desk", destination="AMS", travel_date="2027-02-02",
         must_land_by="2027-02-03 18:00", booking_date="2027-01-05",
         purpose="Investor meetings in Amsterdam on the state's port expansion",
         sign_offs=[attend("Executive Director, Mississippi Development Authority"), dfa()]),
    [search("MSY", "AMS", "2027-02-02", {
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "16:05", "minutes": [95, 525], "layovers": [75]},
        "klm": {"carrier": "KL", "depart": "17:30", "minutes": [560]},
    }, [
        offer("atlanta-economy", "atlanta", "ECONOMY", 79800),
        offer("atlanta-business", "atlanta", "BUSINESS", 588000),
        offer("klm-economy", "klm", "ECONOMY", 84500),
        offer("klm-business", "klm", "BUSINESS", 612000),
    ])],
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], ["INTERNATIONAL_TRAVEL_APPROVED", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "DFA", "NONE"], [*LOW_CLAUSES, *INTL, "CONFERENCES"]),
    [LOWEST, OUTSIDE, CABIN],
    "Travel outside the continental limits, with DFA's approved Travel Authorization Form on file (line 1131). Both "
    "itineraries have a segment over 6 hours, but business is neither asked for nor approved by an eWaiver (lines "
    "868-872): the lowest logical rate, the Atlanta connection (line 370).",
    distractors=[STATUS, CURRENCY])

scenario(
    "heron-quartz", "easy", ["dearer_option", "outside_air_section"],
    "Please book me business class from New Orleans to London on March 8th for the coastal resilience conference. Our "
    "executive director signed my eWaiver for business class and the State Travel Office approved it.",
    trip(traveller_name="Dr. Simone Batiste", traveller_title="Chief Scientist, Coastal Restoration",
         agency="Department of Marine Resources, Picayune science office", destination="LHR", travel_date="2027-03-08",
         must_land_by="2027-03-09 18:00", booking_date="2027-02-08",
         purpose="Presenting at the international coastal resilience conference in London",
         purpose_kind="CONFERENCE", requested_cabin="BUSINESS",
         sign_offs=[attend("Executive Director, Department of Marine Resources"), dfa(),
                    sign("AGENCY_HEAD", "Executive Director, Department of Marine Resources", "EWAIVER_SIGNED",
                         "BUSINESS_CLASS"),
                    sign("STATE_TRAVEL_OFFICE", "State Travel Office (OPTFM)", "EWAIVER_APPROVED", "BUSINESS_CLASS")]),
    [search("MSY", "LHR", "2027-03-08", {
        "philadelphia": {"carrier": "AA", "via": ["PHL"], "depart": "13:20", "minutes": [165, 440], "layovers": [90]},
        "british": {"carrier": "BA", "depart": "18:10", "minutes": [555]},
    }, [
        offer("philadelphia-economy", "philadelphia", "ECONOMY", 79000),
        offer("philadelphia-business", "philadelphia", "BUSINESS", 642000),
        offer("british-economy", "british", "ECONOMY", 84500),
        offer("british-business", "british", "BUSINESS", 598000),
    ])],
    expected("BOOK", ["british-business"], ["BUSINESS"], [*LONG_OK, "INTERNATIONAL_TRAVEL_APPROVED"],
             ["AGENCY_HEAD", "DEPARTMENT_HEAD", "DFA", "NONE", "STATE_TRAVEL_OFFICE"],
             [*CABIN_CLAUSES, *INTL, "CONFERENCES"]),
    [CABIN, WAIVER_SIGN, OUTSIDE, LOWEST],
    "Both itineraries have a segment over 6 hours (555; 440), so business may be authorized, and the agency head's "
    "eWaiver was approved by OPTFM before the trip (lines 868-872): the cheapest business fare, British Airways. "
    "DFA's travel authorization is on file for London (line 1131).")

scenario(
    "coral-whistle", "easy", ["multi_leg", "outside_air_section"],
    "New Orleans to San Juan on January 19th for the hurricane recovery peer exchange. Cheapest economy, please.",
    trip(traveller_name="Andre Whitfield", traveller_title="Recovery Programs Bureau Chief",
         agency="Mississippi Emergency Management Agency, south region office", destination="SJU",
         travel_date="2027-01-19", must_land_by="2027-01-19 20:00", booking_date="2026-12-21",
         purpose="Hurricane recovery peer exchange with Puerto Rico's emergency management bureau",
         sign_offs=[attend("Executive Director, MEMA"), dfa()]),
    [search("MSY", "SJU", "2027-01-19", {
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "07:00", "layovers": [80]},
        "miami": {"carrier": "AA", "via": ["MIA"], "depart": "08:15", "layovers": [95]},
        "miami-late": {"carrier": "AA", "via": ["MIA"], "depart": "12:40", "layovers": [70]},
    }, [
        offer("atlanta-economy", "atlanta", "ECONOMY", 38800),
        offer("miami-economy", "miami", "ECONOMY", 41200),
        offer("miami-late-economy", "miami-late", "ECONOMY", 39900),
    ])],
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], ["INTERNATIONAL_TRAVEL_APPROVED", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "DFA", "NONE"], [*LOW_CLAUSES, *INTL, "CONFERENCES"]),
    [LOWEST, OUTSIDE],
    "Puerto Rico is outside the continental limits (line 1131), and DFA's approval is on file: the lowest logical rate "
    "(line 370), the Delta connection through Atlanta.")

scenario(
    "pecan-drift", "easy", ["multi_leg"],
    "Baton Rouge to Denver on February 16th for the grant audit fieldwork. I'm happy to connect if it's cheaper.",
    trip(traveller_name="Kristen Lowery", traveller_title="Internal Auditor II", duty_station="Centreville, MS",
         local_airport="BTR", origin="BTR", agency="Office of the State Auditor, southwest district",
         destination="DEN", travel_date="2027-02-16", must_land_by="2027-02-16 18:00", booking_date="2027-01-25",
         purpose="Audit fieldwork at a federal grant office in Denver", purpose_kind="AUDIT_FIELDWORK"),
    [search("BTR", "DEN", "2027-02-16", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "06:20", "layovers": [75]},
        "houston": {"carrier": "UA", "via": ["IAH"], "depart": "07:40", "layovers": [65]},
        "united": {"carrier": "UA", "depart": "10:05"},
        "southwest": {"carrier": "WN", "depart": "12:30"},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 25900),
        offer("houston-economy", "houston", "ECONOMY", 27400),
        offer("united-economy", "united", "ECONOMY", 33500),
        offer("southwest-economy", "southwest", "ECONOMY", 31900),
    ], background=2)],
    expected("BOOK", ["dallas-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["NONE"], LOW_CLAUSES),
    [LOWEST, LEAST_ROUTING],
    "No nonstop wish: the least expensive routing (line 853) and lowest logical rate (line 370), the Dallas "
    "connection. Audit fieldwork is not a convention, association or meeting.")

# ===== boundary twins (8) =====

DCA_REQUEST = ("I need to be in Washington for a 1 pm grant review meeting at USDOT on March 1st. If flying up the day "
               "before saves the state money overall, I'm glad to do that; otherwise I'll fly that morning. Economy is "
               "fine.")


def dca_trip():
    return trip(traveller_name="Gregory Pham", traveller_title="Highway Safety Grants Manager",
                agency="Department of Transportation, Office of Highway Safety (Picayune)", destination="DCA",
                travel_date="2027-03-01", must_land_by="2027-03-01 12:00", other_date="2027-02-28",
                other_date_kind="LOWER_FARE", other_date_added_cents=17500, booking_date="2027-02-01",
                purpose="Federal highway safety grant review meeting at USDOT headquarters, 1 pm on March 1",
                sign_offs=[attend("Executive Director, Department of Transportation")])


def dca_searches(before_cents):
    return [
        search("MSY", "DCA", "2027-03-01", {
            "first": {"carrier": "AA", "depart": "06:00", "minutes": [140]},
            "second": {"carrier": "AA", "depart": "07:45", "minutes": [140]},
            "houston": {"carrier": "UA", "via": ["IAH"], "depart": "08:30", "minutes": [80, 170], "layovers": [90]},
        }, [
            offer("first-economy", "first", "ECONOMY", 42800),
            offer("second-economy", "second", "ECONOMY", 45600),
            offer("houston-economy", "houston", "ECONOMY", 13900),
        ], name="day-of"),
        search("MSY", "DCA", "2027-02-28", {
            "afternoon": {"carrier": "AA", "depart": "14:30", "minutes": [140]},
            "evening": {"carrier": "AA", "depart": "18:10", "minutes": [140]},
        }, [
            offer("afternoon-economy", "afternoon", "ECONOMY", before_cents),
            offer("evening-economy", "evening", "ECONOMY", 35500),
        ], name="day-before"),
    ]


scenario(
    "quill-harbor", "boundary_twin", ["date_arithmetic", "month_end"], DCA_REQUEST, dca_trip(), dca_searches(16300),
    expected("BOOK", ["afternoon-economy"], ["ECONOMY"], ["COST_SAVINGS", "EARLIER_DAY_SAVES", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "NONE"], ["AIRLINE_GENERAL", "AIRLINE_PENALTY_FARES", "CONFERENCES", "PUBLIC_CARRIER"]),
    [DAY_EARLY, OTHER_ROUTING, LOWEST],
    "The lowest logical fare on March 1 is $428 (the $139 Houston connection lands at 15:10, after the noon deadline). "
    "February 28 (the day before March 1; 2027 is no leap year) costs $163: a $265 saving, more than the $175 of added "
    "lodging and meals, which lines 900-901 then pay in full. The State saves $90, so fly the day before.",
    twin_of="fennel-wick", twin_fact="day-before fare 16300 or 30300 cents")

scenario(
    "fennel-wick", "boundary_twin", ["date_arithmetic", "month_end", "dearer_option"], DCA_REQUEST, dca_trip(),
    dca_searches(30300),
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["ARRIVES_TOO_LATE", "COST_SAVINGS", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "NONE"], ["AIRLINE_GENERAL", "AIRLINE_PENALTY_FARES", "CONFERENCES", "PUBLIC_CARRIER"]),
    [DAY_EARLY, LOWEST],
    "The day-before fare saves $125 against the lowest logical March 1 fare ($428; the $139 connection lands after the "
    "deadline), less than the $175 of added lodging and meals: the State would pay the extra only up to the saving "
    "(lines 900-901), so flying early does not save it money. Fly the morning of March 1.",
    twin_of="quill-harbor", twin_fact="day-before fare 30300 or 16300 cents")

ORD_REQUEST = ("I'd like to drive down to New Orleans and fly to Chicago from there on January 20th, if that's "
               "acceptable; if not, I'll fly out of Baton Rouge.")


def ord_trip():
    return trip(traveller_name="Wesley Carraway", traveller_title="Bridge Inspection Engineer",
                duty_station="Woodville, MS", local_airport="BTR", origin="BTR",
                agency="Department of Transportation, District 7 bridge unit", destination="ORD",
                travel_date="2027-01-20", must_land_by="2027-01-20 16:00", other_origin="MSY",
                other_origin_added_cents=9500, booking_date="2026-12-30",
                purpose="Acceptance testing of bridge-inspection equipment at the manufacturer near Chicago",
                purpose_kind="SITE_INSPECTION")


def ord_searches(united, american):
    return [
        search("BTR", "ORD", "2027-01-20", {
            "united": {"carrier": "UA", "depart": "06:30"},
            "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "07:10", "layovers": [70]},
        }, [
            offer("btr-united-economy", "united", "ECONOMY", 34800),
            offer("btr-dallas-economy", "dallas", "ECONOMY", 36200),
        ], name="local"),
        search("MSY", "ORD", "2027-01-20", {
            "united": {"carrier": "UA", "depart": "08:00"},
            "american": {"carrier": "AA", "depart": "10:30"},
        }, [
            offer("msy-united-economy", "united", "ECONOMY", united),
            offer("msy-american-economy", "american", "ECONOMY", american),
        ], name="other"),
    ]


scenario(
    "marten-sill", "boundary_twin", [], ORD_REQUEST, ord_trip(), ord_searches(18600, 21400),
    expected("BOOK", ["msy-united-economy"], ["ECONOMY"], ["COST_SAVINGS", "LOWEST_FARE", "OTHER_AIRPORT_MORE_ECONOMICAL"],
             ["NONE"], AIR),
    [LOCAL, ECONOMICAL, LOWEST],
    "Woodville's local airport is Baton Rouge ($348). New Orleans costs $186 plus the coordinator's $95 of added "
    "mileage, parking and staff time: $281, less than $348. Lines 849-851 choose the airport on the costs most "
    "economical to the State, all costs considered, so the local-airport assumption (lines 845-846) gives way.",
    twin_of="osprey-reed", twin_fact="New Orleans fare 18600 or 28900 cents")

scenario(
    "osprey-reed", "boundary_twin", ["dearer_option"], ORD_REQUEST, ord_trip(), ord_searches(28900, 30500),
    expected("BOOK", ["btr-united-economy"], ["ECONOMY"], ["COST_SAVINGS", "LOCAL_AIRPORT_REQUIRED"], ["NONE"], AIR),
    [LOCAL, ECONOMICAL, LOWEST],
    "New Orleans costs $289 plus $95 of added mileage, parking and staff time: $384, more than Baton Rouge's $348. "
    "The local airport (lines 845-846), at its lowest logical fare. LOWEST_FARE is not accepted: the New Orleans fare "
    "is lower, and the ground for declining it is the local-airport and total-cost test.",
    twin_of="marten-sill", twin_fact="New Orleans fare 28900 or 18600 cents")

DEN_REQUEST = "I'd love a nonstop to Denver on January 27th if the state will pay for it; if not, book me the cheaper flight."


def den_trip():
    return trip(traveller_name="Tamika Rowe", traveller_title="Hydrologist II",
                agency="Department of Environmental Quality, Office of Land and Water (Picayune)", destination="DEN",
                travel_date="2027-01-27", must_land_by="2027-01-27 15:00", booking_date="2027-01-04",
                purpose="Hydrology modelling training course in Denver", purpose_kind="TRAINING", wants_nonstop=True,
                sign_offs=[attend("Executive Director, Department of Environmental Quality")])


def den_search(united, southwest):
    return [search("MSY", "DEN", "2027-01-27", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "06:05", "layovers": [70]},
        "united": {"carrier": "UA", "depart": "08:40"},
        "southwest": {"carrier": "WN", "depart": "12:15"},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 24100),
        offer("united-economy", "united", "ECONOMY", united),
        offer("southwest-economy", "southwest", "ECONOMY", southwest),
    ])]


scenario(
    "garnet-rookery", "boundary_twin", ["multi_leg"], DEN_REQUEST, den_trip(), den_search(24100, 26800),
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["FEWEST_STOPS", "LOWEST_FARE"], ["DEPARTMENT_HEAD", "NONE"],
             [*AIR, "CONFERENCES"]),
    [STOPS, LOWEST, LEAST_ROUTING],
    "The United nonstop costs the same $241 as the Dallas connection: it is the lowest fare too, so no eWaiver is needed "
    "(lines 840-843), and lines 864-866 say to choose the flight with the fewest stops: the nonstop the traveller asked "
    "for. The connection at the same fare ignores a request the handbook permits.",
    twin_of="lichen-spindle", twin_fact="nonstop fare 24100 or 28600 cents")

scenario(
    "lichen-spindle", "boundary_twin", ["multi_leg"], DEN_REQUEST, den_trip(), den_search(28600, 29900),
    expected("BOOK", ["dallas-economy"], ["ECONOMY"], DECLINED_NONSTOP, ["DEPARTMENT_HEAD", "NONE"],
             [*AIR, "CONFERENCES", "EWAIVER_REQUEST_FORM", "TRAVEL_ROUTING"]),
    [LEAST_ROUTING, ABOVE_LOWEST, OTHER_ROUTING, STOPS],
    "The cheapest nonstop is $286, $45 above the $241 Dallas connection. The least expensive routing shall be used "
    "(line 853), and a fare above the lowest needs an eWaiver before booking (lines 840-843), which is not on file: "
    "the connection. Lines 864-866 choose fewest stops, but not over the mandatory lowest-fare and eWaiver rules.",
    twin_of="garnet-rookery", twin_fact="nonstop fare 28600 or 24100 cents")

ATL_REQUEST = ("I'm testifying at a federal hearing in Atlanta on March 3rd and have to land by 11:30 that morning. "
               "Book the cheapest flight that gets me there in time.")


def atl_trip():
    return trip(traveller_name="Olivia Brandon", traveller_title="Public Utilities Staff Attorney",
                duty_station="Gloster, MS", local_airport="BTR", origin="BTR",
                agency="Public Utilities Staff, southwest office", destination="ATL", travel_date="2027-03-03",
                must_land_by="2027-03-03 11:30", booking_date="2027-02-10",
                purpose="Testifying at a federal regulatory hearing in Atlanta", purpose_kind="HEARING",
                sign_offs=[attend("Executive Director, Public Utilities Staff")])


def atl_search(layover):
    return [search("BTR", "ATL", "2027-03-03", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "05:30", "minutes": [85, 115], "layovers": [layover]},
        "first": {"carrier": "DL", "depart": "06:00", "minutes": [80]},
        "later": {"carrier": "DL", "depart": "09:30", "minutes": [80]},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 21400),
        offer("first-economy", "first", "ECONOMY", 26800),
        offer("later-economy", "later", "ECONOMY", 23900),
    ])]


scenario(
    "thistle-marsh", "boundary_twin", ["multi_leg"], ATL_REQUEST, atl_trip(), atl_search(60),
    expected("BOOK", ["dallas-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["DEPARTMENT_HEAD", "NONE"], LOW_CLAUSES),
    [LOWEST, MINIMUM],
    "The Dallas connection (60-minute layover) lands at 10:50 local, before 11:30: the lowest logical rate (line 370). "
    "The 09:30 Delta nonstop lands at 11:50, too late.",
    twin_of="alder-shoal", twin_fact="Dallas layover 60 or 150 minutes")

scenario(
    "alder-shoal", "boundary_twin", ["multi_leg", "dearer_option"], ATL_REQUEST, atl_trip(), atl_search(150),
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["ARRIVES_TOO_LATE", "LOWEST_FARE"], ["DEPARTMENT_HEAD", "NONE"],
             LOW_CLAUSES),
    [LOWEST, MINIMUM],
    "With a 150-minute layover the $214 Dallas connection lands at 12:20, and the $239 09:30 nonstop at 11:50: both "
    "after 11:30, so neither is logical (line 370; lines 368-369, at a minimum cost that achieves the mission). The "
    "06:00 Delta nonstop at $268 lands at 08:20.",
    twin_of="thistle-marsh", twin_fact="Dallas layover 150 or 60 minutes")

# ===== multi_rule (5) =====

scenario(
    "juniper-quoin", "multi_rule", ["dearer_option"],
    "Our agency head wants me on a nonstop to Phoenix on February 23rd so I make the afternoon briefing; the eWaiver for "
    "the nonstop fare is approved. Please book it.",
    trip(traveller_name="Carla Mendez", traveller_title="Water Supply Division Director",
         agency="Department of Environmental Quality, Office of Land and Water (Picayune)", destination="PHX",
         travel_date="2027-02-23", must_land_by="2027-02-23 15:00", booking_date="2027-02-01",
         purpose="Afternoon briefing with the Arizona water authority on shared aquifer modelling", wants_nonstop=True,
         sign_offs=[attend("Deputy Director, Office of Land and Water"),
                    sign("AGENCY_HEAD", "Executive Director, Department of Environmental Quality", "ROUTING",
                         "NONSTOP_FARE"),
                    sign("STATE_TRAVEL_OFFICE", "State Travel Office (OPTFM)", "EWAIVER_APPROVED", "NONSTOP_FARE")]),
    [search("MSY", "PHX", "2027-02-23", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "06:00", "layovers": [75]},
        "southwest": {"carrier": "WN", "depart": "07:20"},
        "american": {"carrier": "AA", "depart": "09:10"},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 23800),
        offer("southwest-economy", "southwest", "ECONOMY", 32200),
        offer("american-economy", "american", "ECONOMY", 33900),
    ])],
    expected("BOOK", ["southwest-economy"], ["ECONOMY"], ["EWAIVER_APPROVED"],
             ["AGENCY_HEAD", "DEPARTMENT_HEAD", "NONE", "STATE_TRAVEL_OFFICE"],
             [*AIR, "CONFERENCES", "EWAIVER_REQUEST_FORM"]),
    [OTHER_ROUTING, ABOVE_LOWEST, WAIVER_SIGN, LOWEST],
    "Lines 859-862: routing other than the most economical may be specified by the agency head with an eWaiver to OPTFM; "
    "lines 840-843: a fare above the lowest needs the eWaiver before booking. Both are on file: the cheapest nonstop, "
    "Southwest at $322 (line 370 still picks the lowest of the allowed nonstops).")

HNL_REQUEST = ("Honolulu for the conference on April {day}. It's a long trip, so I'd like business class. Our executive "
               "director signed the eWaiver and it's with the State Travel Office now. If business can be authorized on "
               "this trip, hold the business seat until the waiver is approved; if it can't be authorized on this trip "
               "at all, book me economy.")


def hnl_trip(name, title, date, booked):
    return trip(traveller_name=name, traveller_title=title,
                agency="Mississippi Emergency Management Agency, south region office", destination="HNL",
                travel_date=date, must_land_by=f"{date} 20:00", booking_date=booked,
                purpose="Presenting at the Pacific emergency management conference in Honolulu",
                purpose_kind="CONFERENCE", requested_cabin="BUSINESS",
                sign_offs=[attend("Executive Director, MEMA"), dfa(),
                           sign("AGENCY_HEAD", "Executive Director, MEMA", "EWAIVER_SIGNED", "BUSINESS_CLASS")],
                awaiting="The eWaiver for business class, signed by the executive director, is with the State Travel "
                         "Office for approval.")


scenario(
    "sable-tern", "multi_rule", ["multi_leg", "upgrade_not_taken", "outside_air_section"],
    HNL_REQUEST.format(day="12th"), hnl_trip("Darnell Haynes", "Mitigation Bureau Director", "2027-04-12", "2027-03-15"),
    [search("MSY", "HNL", "2027-04-12", {
        "american": {"carrier": "AA", "via": ["LAX"], "depart": "07:00", "minutes": [225, 330], "layovers": [80]},
        "delta": {"carrier": "DL", "via": ["LAX"], "depart": "08:30", "minutes": [230, 335], "layovers": [70]},
    }, [
        offer("american-economy", "american", "ECONOMY", 64200),
        offer("american-business", "american", "BUSINESS", 298000),
        offer("delta-economy", "delta", "ECONOMY", 66800),
        offer("delta-business", "delta", "BUSINESS", 315000),
    ])],
    expected("BOOK", ["american-economy"], ["ECONOMY"], NOT_MET, ["AGENCY_HEAD", "DEPARTMENT_HEAD", "DFA", "NONE"],
             [*CABIN_CLAUSES, *INTL, "CONFERENCES"]),
    [CABIN, FORM, OUTSIDE, LOWEST],
    "The longest segment is 330 (American) or 335 (Delta) minutes: none exceeds 6 hours (lines 868-869), nor reaches "
    "six hours (line 453), so business cannot be authorized on this trip whatever OPTFM decides. The traveller asked "
    "for economy then: the lowest logical rate, American. DFA's approval for Hawaii is on file (line 1131).")

scenario(
    "bramble-fjord", "multi_rule", ["personal_travel", "date_arithmetic", "outside_air_section"],
    "I'd like to fly down to Orlando two days early, on March 12th, and take two days of annual leave before the "
    "conference; I'll pay my own hotel for those nights. If the state can't do that at no extra cost, just book me "
    "on the 14th.",
    trip(traveller_name="Hannah Greer", traveller_title="Library Services Consultant",
         agency="Mississippi Library Commission, Picayune regional office", destination="MCO",
         travel_date="2027-03-14", must_land_by="2027-03-14 22:00", other_date="2027-03-12",
         other_date_kind="LEAVE_FIRST", leave_approved=True, booking_date="2027-02-15",
         purpose="State library association conference in Orlando, opening session at 8:00 on March 15",
         purpose_kind="CONFERENCE", sign_offs=[attend("Executive Director, Mississippi Library Commission")]),
    [search("MSY", "MCO", "2027-03-14", {
        "southwest": {"carrier": "WN", "depart": "09:10"},
        "jetblue": {"carrier": "B6", "depart": "13:45"},
    }, [
        offer("business-day-southwest", "southwest", "ECONOMY", 23600),
        offer("business-day-jetblue", "jetblue", "ECONOMY", 25100),
    ], name="business-day"),
     search("MSY", "MCO", "2027-03-12", {
         "southwest": {"carrier": "WN", "depart": "08:30"},
         "jetblue": {"carrier": "B6", "depart": "15:20"},
     }, [
         offer("leave-day-southwest", "southwest", "ECONOMY", 28900),
         offer("leave-day-jetblue", "jetblue", "ECONOMY", 31400),
     ], name="leave-day")],
    expected("BOOK", ["business-day-southwest"], ["ECONOMY"], ["COST_SAVINGS", "PERSONAL_TRAVEL_NOT_COVERED"],
             ["DEPARTMENT_HEAD", "NONE"], [*AIR, "COMBINING_PERSONAL_TRAVEL", "CONFERENCES"]),
    [COMBINE, LOWEST],
    "Lines 642-651: leave may be combined when the agency incurs no expenses beyond the business trip's. The March 12 "
    "fare ($289) is above the March 14 lowest ($236), so the earlier day would cost the State more: book March 14, as "
    "the traveller asked otherwise. LOWEST_FARE is not accepted: the ground for declining is the no-extra-expense "
    "condition.",
    twin_of="aster-crane", twin_fact="March 12 fare 28900 or 23600 cents")

scenario(
    "aster-crane", "multi_rule", ["personal_travel", "date_arithmetic", "outside_air_section"],
    "I'd like to fly down to Orlando two days early, on March 12th, and take two days of annual leave before the "
    "conference; I'll pay my own hotel for those nights. If the state can't do that at no extra cost, just book me "
    "on the 14th.",
    trip(traveller_name="Hannah Greer", traveller_title="Library Services Consultant",
         agency="Mississippi Library Commission, Picayune regional office", destination="MCO",
         travel_date="2027-03-14", must_land_by="2027-03-14 22:00", other_date="2027-03-12",
         other_date_kind="LEAVE_FIRST", leave_approved=True, booking_date="2027-02-15",
         purpose="State library association conference in Orlando, opening session at 8:00 on March 15",
         purpose_kind="CONFERENCE", sign_offs=[attend("Executive Director, Mississippi Library Commission")]),
    [search("MSY", "MCO", "2027-03-14", {
        "southwest": {"carrier": "WN", "depart": "09:10"},
        "jetblue": {"carrier": "B6", "depart": "13:45"},
    }, [
        offer("business-day-southwest", "southwest", "ECONOMY", 23600),
        offer("business-day-jetblue", "jetblue", "ECONOMY", 25100),
    ], name="business-day"),
     search("MSY", "MCO", "2027-03-12", {
         "southwest": {"carrier": "WN", "depart": "08:30"},
         "jetblue": {"carrier": "B6", "depart": "15:20"},
     }, [
         offer("leave-day-southwest", "southwest", "ECONOMY", 23600),
         offer("leave-day-jetblue", "jetblue", "ECONOMY", 26200),
     ], name="leave-day")],
    expected("BOOK", ["leave-day-southwest"], ["ECONOMY"], ["LEAVE_DAYS_NO_EXTRA_COST", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "NONE"], [*AIR, "COMBINING_PERSONAL_TRAVEL", "CONFERENCES"]),
    [COMBINE, LOWEST],
    "Lines 642-651: the primary purpose is the conference, the leave is approved, the traveller pays the leave nights, "
    "and the March 12 fare ($236) is no more than the March 14 lowest ($236): the agency incurs no extra expense, so "
    "book March 12 as asked. The March 14 fare at the same price ignores a permitted request.",
    twin_of="bramble-fjord", twin_fact="March 12 fare 23600 or 28900 cents")

scenario(
    "wren-basalt", "multi_rule", ["multi_leg", "dearer_option", "outside_air_section"],
    "Business class to Honolulu on May 3rd for the conference, please. Our executive director signed the eWaiver for "
    "business class and the State Travel Office approved it.",
    trip(traveller_name="Renee Castille", traveller_title="Preparedness Bureau Director",
         agency="Mississippi Emergency Management Agency, south region office", destination="HNL",
         travel_date="2027-05-03", must_land_by="2027-05-03 20:00", booking_date="2027-04-05",
         purpose="Presenting at the Pacific emergency management conference in Honolulu", purpose_kind="CONFERENCE",
         requested_cabin="BUSINESS",
         sign_offs=[attend("Executive Director, MEMA"), dfa(),
                    sign("AGENCY_HEAD", "Executive Director, MEMA", "EWAIVER_SIGNED", "BUSINESS_CLASS"),
                    sign("STATE_TRAVEL_OFFICE", "State Travel Office (OPTFM)", "EWAIVER_APPROVED", "BUSINESS_CLASS")]),
    [search("MSY", "HNL", "2027-05-03", {
        "delta": {"carrier": "DL", "via": ["LAX"], "depart": "07:30", "minutes": [230, 335], "layovers": [70]},
        "american": {"carrier": "AA", "via": ["DFW"], "depart": "08:00", "minutes": [110, 470], "layovers": [85]},
    }, [
        offer("delta-economy", "delta", "ECONOMY", 67200),
        offer("delta-business", "delta", "BUSINESS", 318000),
        offer("american-economy", "american", "ECONOMY", 69800),
        offer("american-business", "american", "BUSINESS", 342000),
    ])],
    expected("BOOK", ["american-business"], ["BUSINESS"], [*LONG_OK, "INTERNATIONAL_TRAVEL_APPROVED"],
             ["AGENCY_HEAD", "DEPARTMENT_HEAD", "DFA", "NONE", "STATE_TRAVEL_OFFICE"],
             [*CABIN_CLAUSES, *INTL, "CONFERENCES"]),
    [CABIN, WAIVER_SIGN, OUTSIDE],
    "The eWaiver is approved, but business may be authorized only 'if at least one of the flight segments exceeds 6 "
    "hours' (lines 868-869). The cheaper Delta business fare flies 230 and 335 minutes: no segment qualifies. American's "
    "Dallas-Honolulu segment is 470 minutes: book American business, the cheapest that can be authorized.")

# ===== hidden clause (3) =====

scenario(
    "tamarack-ferry", "hidden_clause", ["multi_leg", "outside_air_section"],
    "Please book me New Orleans to Anchorage on February 22nd for the oil spill response drill. Cheapest economy.",
    trip(traveller_name="Brent Ladner", traveller_title="Emergency Response Coordinator",
         agency="Department of Environmental Quality, Emergency Services (Picayune)", destination="ANC",
         travel_date="2027-02-22", must_land_by="2027-02-22 23:00", booking_date="2027-01-25",
         purpose="Oil spill response drill hosted by Alaska's environmental agency", purpose_kind="TRAINING",
         sign_offs=[attend("Executive Director, Department of Environmental Quality")]),
    [search("MSY", "ANC", "2027-02-22", {
        "minneapolis": {"carrier": "DL", "via": ["MSP"], "depart": "06:40", "layovers": [80]},
        "seattle": {"carrier": "AS", "via": ["SEA"], "depart": "07:15", "layovers": [75]},
    }, [
        offer("minneapolis-economy", "minneapolis", "ECONOMY", 49800),
        offer("seattle-economy", "seattle", "ECONOMY", 52400),
    ])],
    expected("BOOK", ["minneapolis-economy"], ["ECONOMY"], ["DOMESTIC_TRAVEL", "LOWEST_FARE"],
             ["DEPARTMENT_HEAD", "NONE"], [*LOW_CLAUSES, "CONFERENCES", "DEFINITIONS", "INTERNATIONAL_TRAVEL"]),
    [ALASKA, INTL_DEF, LOWEST],
    "Alaska is far and outside the 48 contiguous states, but the notes at lines 1145-1146 and the definition at line "
    "249 count it within the continental limits: no DFA approval is needed. The lowest logical rate, via Minneapolis.")

scenario(
    "lupine-grotto", "hidden_clause", ["dearer_option", "outside_air_section"],
    "Please book business class from New Orleans to Paris on May 10th for the ocean sciences conference. The "
    "university's travel office approved my waiver for business class under the university's own procedure.",
    trip(traveller_name="Dr. Ethan Moreau", traveller_title="Associate Professor of Marine Science",
         passenger="UNIVERSITY_EMPLOYEE", duty_station="Stennis Space Center, MS",
         agency="University of Southern Mississippi, School of Ocean Science (Stennis)", destination="CDG",
         travel_date="2027-05-10", must_land_by="2027-05-11 18:00", booking_date="2027-04-12",
         purpose="Presenting a paper at the international ocean sciences conference in Paris",
         purpose_kind="CONFERENCE", requested_cabin="BUSINESS",
         sign_offs=[attend("Director, School of Ocean Science"),
                    sign("UNIVERSITY_TRAVEL_OFFICE", "University Travel Office", "UNIVERSITY_WAIVER", "BUSINESS_CLASS")]),
    [search("MSY", "CDG", "2027-05-10", {
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "15:30", "minutes": [95, 535], "layovers": [80]},
        "airfrance": {"carrier": "AF", "depart": "17:45", "minutes": [590]},
    }, [
        offer("atlanta-economy", "atlanta", "ECONOMY", 87600),
        offer("atlanta-business", "atlanta", "BUSINESS", 512000),
        offer("airfrance-economy", "airfrance", "ECONOMY", 91200),
        offer("airfrance-business", "airfrance", "BUSINESS", 486000),
    ])],
    expected("BOOK", ["airfrance-business"], ["BUSINESS"],
             ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UNIVERSITY_WAIVER_PROCESS"],
             ["DEPARTMENT_HEAD", "NONE", "UNIVERSITY_TRAVEL_OFFICE"],
             [*CABIN_CLAUSES, "CONFERENCES", "INTERNATIONAL_TRAVEL"]),
    [UNIVERSITY, CABIN, OUTSIDE],
    "Both itineraries have a segment over 6 hours (590; 535), so business may be authorized (lines 868-869). The "
    "OPTFM eWaiver of lines 870-872 does not apply: universities are exempt from submitting eWaivers and follow their "
    "own waiver procedure (lines 471-474), and the university's approval is on file. Universities are also excluded "
    "from DFA's prior approval of travel outside the continental limits (line 1132). The cheapest business fare: Air "
    "France.")

scenario(
    "marigold-oar", "hidden_clause", ["multi_leg", "outside_air_section"],
    "I'm on the State Board of Health and need to get to the national board conference near Dulles on March 22nd. "
    "Cheapest economy, please.",
    trip(traveller_name="Dr. Raymond Pickens", traveller_title="Member, State Board of Health",
         passenger="BOARD_MEMBER", board_allowance_instead_of_salary=True, duty_station="Poplarville, MS",
         agency="Mississippi State Board of Health", destination="IAD", travel_date="2027-03-22",
         must_land_by="2027-03-22 19:00", booking_date="2027-02-26",
         purpose="National association of state boards of health annual conference near Washington Dulles",
         purpose_kind="CONFERENCE", sign_offs=[attend("State Health Officer, Mississippi State Department of Health")]),
    [search("MSY", "IAD", "2027-03-22", {
        "houston": {"carrier": "UA", "via": ["IAH"], "depart": "06:30", "layovers": [75]},
        "charlotte": {"carrier": "AA", "via": ["CLT"], "depart": "07:00", "layovers": [65]},
        "united": {"carrier": "UA", "depart": "08:15"},
    }, [
        offer("houston-economy", "houston", "ECONOMY", 30500),
        offer("charlotte-economy", "charlotte", "ECONOMY", 28700),
        offer("united-economy", "united", "ECONOMY", 31200),
    ])],
    expected("BOOK", ["charlotte-economy"], ["ECONOMY"], ["LOWEST_FARE", "OFFICER_OF_THE_STATE"],
             ["DEPARTMENT_HEAD", "NONE"], [*LOW_CLAUSES, "CONFERENCES", "TRAVEL_CARD"]),
    [BOARD, CARDLESS, LOWEST],
    "A board member is not an employee, but lines 375-377 make a board member paid the per diem in lieu of salary an "
    "officer of the state, and lines 1026-1028 let the cardless account book non-entity travellers on official state "
    "business. The lowest logical rate: the Charlotte connection.")

# ===== distractor (3) =====

scenario(
    "cobalt-meadow", "distractor", [],
    "I thought about driving to Charlotte for the inspection on January 26th, but it's a long way, so I'll fly. Book me "
    "the cheapest flight.",
    trip(traveller_name="Jerome Hollis", traveller_title="Elections Equipment Examiner", duty_station="Woodville, MS",
         local_airport="BTR", origin="BTR", agency="Secretary of State, Elections Division field office",
         destination="CLT", travel_date="2027-01-26", must_land_by="2027-01-26 17:00", booking_date="2027-01-04",
         purpose="Inspection of a vendor's voting equipment plant near Charlotte", purpose_kind="SITE_INSPECTION"),
    [search("BTR", "CLT", "2027-01-26", {
        "first": {"carrier": "AA", "depart": "06:45"},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "08:10", "layovers": [70]},
        "afternoon": {"carrier": "AA", "depart": "13:00"},
    }, [
        offer("first-economy", "first", "ECONOMY", 25700),
        offer("atlanta-economy", "atlanta", "ECONOMY", 27900),
        offer("afternoon-economy", "afternoon", "ECONOMY", 43100, refundable=True),
    ])],
    expected("BOOK", ["first-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["NONE"], LOW_CLAUSES),
    [LOWEST, METHOD],
    "The lowest logical rate (line 370). The 'lowest unrestricted airfare' of lines 786-792 caps what a driver is "
    "reimbursed; it is not the fare to buy when flying, and the refundable fare is dearer.",
    distractors=[DRIVE, UNRESTRICTED])

scenario(
    "ember-paddock", "distractor", ["multi_leg", "date_arithmetic"],
    "Please book me to Seattle on February 17th for the wildfire GIS course, cheapest economy. I'll also need a $600 "
    "travel advance for the hotel.",
    trip(traveller_name="Allison Tran", traveller_title="Forestry GIS Analyst",
         agency="Mississippi Forestry Commission, Picayune district", destination="SEA", travel_date="2027-02-17",
         must_land_by="2027-02-17 20:00", booking_date="2027-01-22", travel_advance_cents=60000,
         purpose="Wildfire GIS training course in Seattle", purpose_kind="TRAINING",
         sign_offs=[attend("State Forester, Mississippi Forestry Commission")]),
    [search("MSY", "SEA", "2027-02-17", {
        "minneapolis": {"carrier": "DL", "via": ["MSP"], "depart": "06:30", "layovers": [70]},
        "denver": {"carrier": "UA", "via": ["DEN"], "depart": "07:15", "layovers": [80]},
        "alaska": {"carrier": "AS", "depart": "09:00"},
    }, [
        offer("minneapolis-economy", "minneapolis", "ECONOMY", 28800),
        offer("denver-economy", "denver", "ECONOMY", 30100),
        offer("alaska-economy", "alaska", "ECONOMY", 31200),
    ])],
    expected("BOOK", ["minneapolis-economy"], ["ECONOMY"], ["LOWEST_FARE"], ["DEPARTMENT_HEAD", "NONE"],
             [*LOW_CLAUSES, "CONFERENCES"]),
    [LOWEST, LEAST_ROUTING],
    "The lowest logical rate (line 370). The advance is 26 days before travel and needs the executive director's "
    "approval (lines 389-395), but those rules govern the cash advance, not the ticket: book now.",
    distractors=[ADVANCE, COMPARISON])

scenario(
    "slate-heron", "distractor", ["multi_leg"],
    "The State Travel Office already approved my eWaiver, so please put me on the nonstop to Las Vegas on April 5th if "
    "that's covered; otherwise the cheaper flight is fine.",
    trip(traveller_name="Patrick Dunaway", traveller_title="Traffic Operations Engineer",
         agency="Department of Transportation, Traffic Engineering (Picayune)", destination="LAS",
         travel_date="2027-04-05", must_land_by="2027-04-05 18:00", booking_date="2027-03-08",
         purpose="Western states transportation operations conference in Las Vegas", purpose_kind="CONFERENCE",
         wants_nonstop=True,
         sign_offs=[attend("Executive Director, Department of Transportation"),
                    sign("STATE_TRAVEL_OFFICE", "State Travel Office (OPTFM)", "EWAIVER_APPROVED", "LODGING")]),
    [search("MSY", "LAS", "2027-04-05", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "06:30", "layovers": [75]},
        "saltlake": {"carrier": "DL", "via": ["SLC"], "depart": "07:45", "layovers": [65]},
        "southwest": {"carrier": "WN", "depart": "10:20"},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 24600),
        offer("saltlake-economy", "saltlake", "ECONOMY", 26200),
        offer("southwest-economy", "southwest", "ECONOMY", 31800),
    ])],
    expected("BOOK", ["dallas-economy"], ["ECONOMY"], DECLINED_NONSTOP,
             ["DEPARTMENT_HEAD", "NONE", "STATE_TRAVEL_OFFICE"],
             [*AIR, "CONFERENCES", "EWAIVER_REQUEST_FORM", "TRAVEL_ROUTING"]),
    [LEAST_ROUTING, ABOVE_LOWEST],
    "The eWaiver on file is for staying outside the conference hotel (lines 1099-1103); a fare above the lowest needs "
    "its own eWaiver (lines 840-843) and the least expensive routing shall be used (line 853): the Dallas connection.",
    distractors=[HOTEL_WAIVER])

# ===== refusal (3) =====

scenario(
    "hollow-brine", "refusal", ["personal_travel", "outside_air_section"],
    "I'm taking two weeks of annual leave for a family vacation in Honolulu over spring break. While I'm there I'll drop "
    "by the Hawaii emergency management office to say hello, so can the state buy my ticket?",
    trip(traveller_name="Corey Saucier", traveller_title="Planning Section Chief",
         agency="Mississippi Emergency Management Agency, south region office", destination="HNL",
         travel_date="2027-03-20", must_land_by="2027-03-20 23:00", leave_approved=True, booking_date="2027-02-22",
         purpose="Family vacation in Honolulu over spring break, with an optional courtesy visit to the Hawaii emergency "
                 "management office that nobody at the agency asked for", purpose_kind="VACATION"),
    [search("MSY", "HNL", "2027-03-20", {
        "american": {"carrier": "AA", "via": ["LAX"], "depart": "07:00", "layovers": [80]},
        "delta": {"carrier": "DL", "via": ["LAX"], "depart": "08:30", "layovers": [70]},
    }, [
        offer("american-economy", "american", "ECONOMY", 61500),
        offer("delta-economy", "delta", "ECONOMY", 63800),
    ])],
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["COMBINING_PERSONAL_TRAVEL", "INTRODUCTION", "TRAVEL_REIMBURSEMENT"]),
    [COMBINE, COVERED],
    "Lines 642-644: business and personal leave may be combined only when the primary purpose of the trip is official "
    "state business. The trip is a family vacation; the courtesy call is optional and unrequested. The state buys no "
    "ticket (and DFA's approval for Hawaii never comes into it).")

scenario(
    "maple-dune", "refusal", ["outside_air_section"],
    "Please book a ticket for my husband Robert to come with me to the public health conference in San Diego on April "
    "26th; he'll share my room.",
    trip(traveller_name="Robert Ellison", traveller_title="Husband of Dr. Karen Ellison, State Epidemiologist's office",
         passenger="FAMILY_MEMBER", accompanies="Dr. Karen Ellison",
         agency="Mississippi State Department of Health, Picayune district office", destination="SAN",
         travel_date="2027-04-26", must_land_by="2027-04-26 20:00", booking_date="2027-03-29",
         purpose="Accompanying his wife to a public health conference in San Diego", purpose_kind="CONFERENCE",
         sign_offs=[attend("State Health Officer, Mississippi State Department of Health")]),
    [search("MSY", "SAN", "2027-04-26", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "06:50", "layovers": [70]},
        "alaska": {"carrier": "AS", "depart": "09:40"},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 29900),
        offer("alaska-economy", "alaska", "ECONOMY", 32800),
    ])],
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_COVERED", "PERSONAL_TRAVEL_NOT_COVERED"],
             ["DEPARTMENT_HEAD", "NONE"],
             ["COMBINING_PERSONAL_TRAVEL", "INTRODUCTION", "LODGING_WITH_NON_EMPLOYEE", "TRAVEL_CARD",
              "TRAVEL_REIMBURSEMENT"]),
    [COVERED, FAMILY, CARDLESS, COMBINE],
    "The rules cover state officers and employees on official business (lines 202-203); the cardless account books "
    "non-employees only on official state business (lines 1026-1028); a family member along means the single room "
    "rate only (lines 1216-1217); and the agency incurs no expense beyond the business trip (line 648). No ticket for "
    "the husband.")

scenario(
    "pewter-fen", "refusal", ["date_arithmetic"],
    "Please buy me a regular ticket to Atlanta on January 6th for the CDC partnership meeting. I do have a free Delta "
    "coupon from the miles I earned on state trips, but I'd like to save it for a family trip.",
    trip(traveller_name="Natalie Burkes", traveller_title="Immunization Program Manager",
         agency="Mississippi State Department of Health, Picayune district office", destination="ATL",
         travel_date="2027-01-06", must_land_by="2027-01-06 14:00", booking_date="2026-12-16",
         purpose="Quarterly coordination meeting with the CDC's state partnership office in Atlanta",
         free_ticket_coupon="A Delta free one-way economy ticket coupon from SkyMiles earned on state-paid trips; good "
                            "on any Delta flight New Orleans-Atlanta; expires 2027-01-10; no other state trip is "
                            "planned before then",
         sign_offs=[attend("State Health Officer, Mississippi State Department of Health")]),
    [search("MSY", "ATL", "2027-01-06", {
        "charlotte": {"carrier": "AA", "via": ["CLT"], "depart": "06:15", "layovers": [60]},
        "delta": {"carrier": "DL", "depart": "07:00"},
    }, [
        offer("charlotte-economy", "charlotte", "ECONOMY", 22800),
        offer("delta-economy", "delta", "ECONOMY", 20500),
    ])],
    expected("REFUSE", [], ["NONE"], ["FREE_TICKET_MUST_BE_USED"], ["DEPARTMENT_HEAD", "NONE"],
             ["FREQUENT_FLYER_AWARDS", "PUBLIC_CARRIER"]),
    [AWARD],
    "Lines 884-888: a bonus earned on state travel shall offset later official travel, the traveller can under no "
    "circumstances keep it for personal use, and free ticket coupons are used to offset official travel costs. The "
    "coupon covers this flight and expires (January 10) before any other state trip, so it is used and the state "
    "buys no ticket.")

# ===== flag (4) =====

scenario(
    "nimbus-garland", "flag", ["multi_leg", "unclear_phrase", "outside_air_section"],
    HNL_REQUEST.format(day="19th"), hnl_trip("Alicia Pruitt", "Hazard Mitigation Officer", "2027-04-19", "2027-03-22"),
    [search("MSY", "HNL", "2027-04-19", {
        "american": {"carrier": "AA", "via": ["LAX"], "depart": "07:00", "minutes": [225, 360], "layovers": [80]},
        "delta": {"carrier": "DL", "via": ["LAX"], "depart": "08:30", "minutes": [230, 355], "layovers": [70]},
    }, [
        offer("american-economy", "american", "ECONOMY", 65500),
        offer("american-business", "american", "BUSINESS", 306000),
        offer("delta-economy", "delta", "ECONOMY", 68900),
        offer("delta-business", "delta", "BUSINESS", 324000),
    ])],
    expected("FLAG_FOR_APPROVAL", ["american-business", "american-economy"], ["BUSINESS", "ECONOMY"],
             ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"], ["NOT_NAMED", "STATE_TRAVEL_OFFICE"], CABIN_CLAUSES,
             phrase="if at least one of the flight segments exceeds 6 hours"),
    [CABIN, FORM],
    "American's Los Angeles-Honolulu segment is exactly 360 minutes. Lines 868-869 authorize business only if a "
    "segment 'exceeds 6 hours' (strict: 360 does not), while the eWaiver form's reason (line 453) is business 'six "
    "hours or longer non-stop' (inclusive: 360 does). The first reading books the lowest economy fare; the second holds "
    "American business for OPTFM's approval. Hold either offer.",
    flag_twins=["sable-tern", "wren-basalt"],
    ambiguity={"phrase": "if at least one of the flight segments exceeds 6 hours",
               "readings": [("'exceeds 6 hours' is strict: a 360-minute segment does not qualify, so business cannot be "
                            "authorized: book the lowest economy fare"),
                            ("the eWaiver form's 'six hours or longer non-stop' (line 453) lets a 360-minute segment in: "
                            "hold the business fare until OPTFM approves the eWaiver")]})

scenario(
    "quartz-oriel", "flag", ["multi_leg", "approval_required", "dearer_option", "outside_air_section"],
    HNL_REQUEST.format(day="26th"), hnl_trip("Victor Lusk", "Logistics Bureau Director", "2027-04-26", "2027-03-29"),
    [search("MSY", "HNL", "2027-04-26", {
        "delta": {"carrier": "DL", "via": ["LAX"], "depart": "07:30", "minutes": [230, 335], "layovers": [70]},
        "american": {"carrier": "AA", "via": ["DFW"], "depart": "08:00", "minutes": [110, 470], "layovers": [85]},
    }, [
        offer("delta-economy", "delta", "ECONOMY", 67200),
        offer("delta-business", "delta", "BUSINESS", 318000),
        offer("american-economy", "american", "ECONOMY", 69800),
        offer("american-business", "american", "BUSINESS", 342000),
    ])],
    expected("FLAG_FOR_APPROVAL", ["american-business"], ["BUSINESS"], ["APPROVAL_REQUIRED"], ["STATE_TRAVEL_OFFICE"],
             CABIN_CLAUSES),
    [CABIN, WAIVER_SIGN, WAIVER_PRIOR],
    "American's Dallas-Honolulu segment is 470 minutes, so business may be authorized (lines 868-869), but it is not "
    "reimbursable unless the eWaiver is approved by OPTFM before the trip (lines 870-872), and that approval is still "
    "awaited. Hold American business, the cheapest fare that can be authorized (Delta's cheaper business flies no "
    "segment over 6 hours), for the State Travel Office. Approval required, not 'no compliant offer'.",
    flag_twins=["sable-tern", "wren-basalt"],
    ambiguity="none: the eWaiver's approval is required and still awaited; the text is clear")

scenario(
    "velvet-bight", "flag", ["approval_required", "outside_air_section"],
    "Please book me to Boston on May 17th for the national state auditors' conference. My director hasn't signed my "
    "attendance approval yet, but I want to lock in the fare.",
    trip(traveller_name="Leon Whitaker", traveller_title="Senior Performance Auditor",
         agency="Office of the State Auditor, south district (Picayune)", destination="BOS", travel_date="2027-05-17",
         must_land_by="2027-05-17 20:00", booking_date="2027-04-19",
         purpose="National conference of state auditors in Boston", purpose_kind="CONFERENCE",
         awaiting="Written approval to attend the conference, asked of the department head and not yet signed."),
    [search("MSY", "BOS", "2027-05-17", {
        "philadelphia": {"carrier": "AA", "via": ["PHL"], "depart": "06:10", "layovers": [70]},
        "jetblue": {"carrier": "B6", "depart": "07:30"},
        "delta": {"carrier": "DL", "depart": "11:00"},
    }, [
        offer("philadelphia-economy", "philadelphia", "ECONOMY", 31900),
        offer("jetblue-economy", "jetblue", "ECONOMY", 33800),
        offer("delta-economy", "delta", "ECONOMY", 35200),
    ])],
    expected("FLAG_FOR_APPROVAL", ["philadelphia-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED"],
             ["AGENCY_HEAD", "DEPARTMENT_HEAD"], ["CONFERENCES"]),
    [CONFERENCE, LOWEST],
    "Lines 1072-1073: expenses of attending any convention are reimbursed only with the department head's prior "
    "written approval, which is asked for and not yet given. Hold the lowest logical fare (line 370), the Philadelphia "
    "connection, for the department head.",
    flag_twins=["marigold-oar", "hollow-brine"],
    ambiguity="none: the department head's written approval is required and missing; the text is clear")

scenario(
    "dapple-cairn", "flag", ["unclear_phrase", "outside_air_section"],
    "I need to fly to Atlanta on February 9th for a working session with FEMA Region 4 staff to reconcile our open "
    "grant files. Cheapest economy, please.",
    trip(traveller_name="Monique Batson", traveller_title="Grants Reconciliation Specialist",
         agency="Mississippi Emergency Management Agency, south region office", destination="ATL",
         travel_date="2027-02-09", must_land_by="2027-02-09 13:00", booking_date="2027-01-19",
         purpose="Working meeting with FEMA Region 4 staff in Atlanta to reconcile open grant files"),
    [search("MSY", "ATL", "2027-02-09", {
        "first": {"carrier": "DL", "depart": "06:45"},
        "charlotte": {"carrier": "AA", "via": ["CLT"], "depart": "07:10", "layovers": [60]},
        "later": {"carrier": "DL", "depart": "10:20"},
    }, [
        offer("first-economy", "first", "ECONOMY", 19800),
        offer("charlotte-economy", "charlotte", "ECONOMY", 22900),
        offer("later-economy", "later", "ECONOMY", 21600),
    ])],
    expected("FLAG_FOR_APPROVAL", ["first-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"],
             ["AGENCY_HEAD", "DEPARTMENT_HEAD", "NOT_NAMED"], ["CONFERENCES"],
             phrase="attendance at any convention, association, or meeting"),
    [CONFERENCE, LOWEST],
    "Lines 1072-1073 require the department head's prior written approval for 'attendance at any convention, "
    "association, or meeting'. The section is headed Conferences, and this is a working session with a federal partner: "
    "whether 'meeting' reaches it is unclear, and no approval is on file. On one reading book the lowest fare; on the "
    "other, hold it for the department head. Hold the lowest logical fare.",
    flag_twins=["cypress-lantern", "bayou-thimble"],
    ambiguity={"phrase": "attendance at any convention, association, or meeting",
               "readings": [("'meeting' means meetings of the conference kind (conventions, associations): a working "
                            "session with a federal partner needs no written approval: book the lowest fare"),
                            ("'any ... meeting' covers every meeting attended: without the department head's prior "
                            "written approval, hold the fare")]})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios to {OUT}")


if __name__ == "__main__":
    main()
