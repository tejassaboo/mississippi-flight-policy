"""The answer key's rules for the State of Mississippi, Department of Finance and Administration, State Travel
Policy Rules & Regulations (December 2024), as exact integer code. Byte-identical in src/plugin/rules.py and
verifier/rules.py; it imports only modules a verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an
answer open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each
unclear phrase at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a
new scenario cannot fall silently into untested logic.

The duration hook. Lines 868-869: "Preferred seating, b usiness, or first-class service may be authorized if at
least one of the flight segments exceeds 6 hours. A flight segment is defined as time in the air between
stopovers, changing aircraft, or change of airline." The test is per segment and strict ("exceeds"): rule
"segment". The eWaiver form's own wording (line 453) is "first-class or business-class airfare (six hours or
longer non-stop)", inclusive: rule "waiver-form". The two agree except on a longest segment of exactly 360
minutes, which the "segment" rule leaves out and the "waiver-form" rule lets in: that case is unclear. A
segment's scheduled minutes are its time in the air in this world (the only measure the tools give); every
scenario except the unclear one keeps its longest segment at least 25 minutes from 360, so a reader who
subtracts taxi time reaches the same answer.
"""

from contract import (
    Approver,
    Cabin,
    Clause,
    Covers,
    Decision,
    OtherDate,
    Passenger,
    Purpose,
    ReasonCode,
    SignOffSubject,
)

from .world import airport, clock_minutes, day_number, utc_minute, utc_offset

HANDBOOK = "State of Mississippi, DFA State Travel Policy Rules & Regulations, December 2024"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.INTRODUCTION: "100. Introduction",
    Clause.DEFINITIONS: "101. Definitions",
    Clause.ADMINISTRATION: "102. Administration & Responsibility",
    Clause.TRAVEL_REIMBURSEMENT: "103. Travel Reimbursement",
    Clause.TRAVEL_ADVANCES: "104. Travel Advances",
    Clause.EWAIVER_REQUEST_FORM: "105. eWaiver Request Form",
    Clause.TRAVEL_VOUCHER: "106. Travel Reimbursement Voucher",
    Clause.TRAVEL_ROUTING: "107. Travel Routing",
    Clause.COMBINING_PERSONAL_TRAVEL: "108. Combining Business Travel with Personal Travel",
    Clause.VEHICLE_TRAVEL: "109. Vehicle Travel",
    Clause.DRIVING_VERSUS_FLYING: "D. Calculating Reimbursement for Driving vs. Flying",
    Clause.PUBLIC_CARRIER: "110. Public Carrier (Airplane)",
    Clause.AIRLINE_GENERAL: "A. Airline Travel - General Information",
    Clause.FREQUENT_FLYER_AWARDS: "B. Frequent Flyer Program Awards",
    Clause.AIRLINE_PENALTY_FARES: "C. Airline Penalty Fares",
    Clause.RESERVATION_CHANGES: "D. Airline Reservation Changes",
    Clause.TRAVEL_CARD: "111. Travel Card Program Overview",
    Clause.CONFERENCES: "112. In-State/Out-Of-State/International Conferences",
    Clause.CONFERENCE_AIRLINES: "113. Conference Airlines",
    Clause.CONFERENCE_HOTELS: "114. Conference Hotels",
    Clause.INTERNATIONAL_TRAVEL: "116. General Information",
    Clause.APPROVAL_FORMS: "117. Approval Form Requirements",
    Clause.LODGING: "119. General Information",
    Clause.LODGING_WITH_NON_EMPLOYEE: "120. Lodging Shared With Someone Not a State Employee",
    Clause.MEAL_ALLOWANCES: "124. General Information",
    Clause.CONTRACT_TRAVEL_AGENCIES: "128. General Information",
    Clause.OTHER_EXPENSES: "130. Phone Charges, Postage, and Other Expenses",
}

# The handbook's duration thresholds (the per-handbook duration hook; tests/test_duration.py tests both
# sides of each). ">" is strict ("exceeds 6 hours"), ">=" inclusive ("six hours or longer").
DURATION_RULES = (
    {"name": "segment", "minutes": 360, "operator": ">", "lines": [868, 869],
     "quote": "Preferred seating, b usiness, or first-class service may be authorized if at least one of the flight "
              "segments exceeds 6 hours."},
    {"name": "waiver-form", "minutes": 360, "operator": ">=", "lines": [453, 453],
     "quote": "Requesting authority to pay first-class or business-class airfare (six hours or longer non-stop)"},
)
LIMITS = {rule["name"]: rule["minutes"] for rule in DURATION_RULES}

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Line 1131 and the notes at lines 1145-1146: travel outside the continental limits of the United States
# (Canada, Hawaii, Puerto Rico and Mexico are outside; Alaska is within) needs DFA's approval before departure,
# except for universities (line 1132).
OUTSIDE_US_STATES = {"HNL"}

SEGMENT_PHRASE = "if at least one of the flight segments exceeds 6 hours"
MEETING_PHRASE = "attendance at any convention, association, or meeting"

# Who a hold over unclear words may name. No role is named to settle the text; a reader may name the role the
# hold would wait on under the stricter reading.
LOWEST_CLAUSES = [Clause.TRAVEL_REIMBURSEMENT, Clause.PUBLIC_CARRIER, Clause.AIRLINE_GENERAL, Clause.TRAVEL_ROUTING]
AIR_CLAUSES = [Clause.PUBLIC_CARRIER, Clause.AIRLINE_GENERAL]
CABIN_CLAUSES = [Clause.PUBLIC_CARRIER, Clause.AIRLINE_GENERAL, Clause.EWAIVER_REQUEST_FORM]
UNCLEAR_REASONS = [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED]
ATTENDANCE_ROLES = [Approver.DEPARTMENT_HEAD, Approver.AGENCY_HEAD]


def over(rule, offer):
    """True or False: whether ``offer``'s outbound flights pass the handbook's ``rule`` (segment: one flight of more
    than 360 scheduled minutes; waiver-form: one flight of 360 minutes or more). Never unclear by itself: the
    unclear case is where the two rules disagree (see ``cabin_status``)."""
    if rule not in LIMITS:
        raise ValueError(f"unknown duration rule {rule!r}")
    if rule == "segment":
        return any(segment.scheduled_minutes > LIMITS[rule] for segment in offer.segments)
    return any(segment.scheduled_minutes >= LIMITS[rule] for segment in offer.segments)


def cabin_status(offer):
    """True when business may be authorized on every reading, False when on none, None when only the
    inclusive wording of line 453 lets it in."""
    strict, form = over("segment", offer), over("waiver-form", offer)
    if strict:
        return True
    return None if form else False


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def in_cabin(offers, cabin):
    return [offer for offer in offers if offer.cabin == cabin]


def on_file(trip):
    """Approvers a booking or refusal accepts (SYNC_NOTES 4' and 4(b)): NONE, and the role of every sign-off on
    file, whether the decision relies on it (readers split on a sign-off already given) or not."""
    return [Approver.NONE, *(record.role for record in trip.sign_offs)]


def signed(trip, subject, covers, role):
    return any(record.subject == subject and record.covers == covers and record.role == role
               for record in trip.sign_offs)


def leaves_from(offer):
    return offer.segments[0].origin, offer.segments[0].depart_local[:10]


def deadline_utc(trip):
    text = trip.must_land_by
    if len(text) != 16:
        raise ValueError("must_land_by is YYYY-MM-DD HH:MM")
    return day_number(text[:10]) * 1440 + clock_minutes(text[11:]) - utc_offset(trip.destination.code)


def logical(trip, offers):
    """Seated offers that land by the time the business needs (line 370: 'the lowest logical rate')."""
    limit = deadline_utc(trip)
    return [offer for offer in offers if offer.seats_available and utc_minute(offer.segments[-1].arrive_utc) <= limit]


def outside_continental(trip):
    return trip.destination.country != "US" or trip.destination.code in OUTSIDE_US_STATES


def lowest_economy(trip, offers):
    """The cheapest logical economy fare among ``offers``, with the reasons and notes it carries. Raises where
    line 864-866's fewest-stops choice would decide between tied fares, unless the case is about it."""
    economy = in_cabin(offers, Cabin.ECONOMY)
    usable = logical(trip, economy)
    lowest = cheapest(usable)
    if not lowest:
        raise ValueError("no logical economy offer")
    if any(offer.refundable for offer in lowest):
        raise ValueError("a refundable lowest fare is not modelled")
    reasons, notes = [ReasonCode.LOWEST_FARE], []
    seated = cheapest([offer for offer in economy if offer.seats_available])
    if seated and seated[0].fare_cents < lowest[0].fare_cents:
        reasons.append(ReasonCode.ARRIVES_TOO_LATE)
        notes.append("a cheaper seat lands after the business needs the traveller, so it is not logical")
    return lowest, reasons, notes


def scope(trip):
    """Reasons, clauses and notes for who flies and where: line 1131 (outside the continental limits needs DFA's
    approval; Alaska is within, lines 1145-1146), lines 375-377 (board members on a per diem are officers of the
    state) and lines 1026-1028 (the cardless account books non-employees on official state business)."""
    reasons, clauses, notes = [], [], []
    if outside_continental(trip):
        if trip.passenger == Passenger.UNIVERSITY_EMPLOYEE:
            clauses.append(Clause.INTERNATIONAL_TRAVEL)
            notes.append("line 1132: universities are excluded from DFA's prior approval of travel outside the "
                         "continental limits")
        elif signed(trip, SignOffSubject.TRAVEL_AUTHORIZATION, Covers.THE_TRIP, Approver.DFA):
            reasons.append(ReasonCode.INTERNATIONAL_TRAVEL_APPROVED)
            clauses += [Clause.INTERNATIONAL_TRAVEL, Clause.APPROVAL_FORMS]
            notes.append("line 1131: the destination is outside the continental limits, and DFA's approved Travel "
                         "Authorization Form is on file")
        else:
            raise ValueError("travel outside the continental limits without DFA approval is not modelled")
    elif trip.destination.code == "ANC":
        reasons.append(ReasonCode.DOMESTIC_TRAVEL)
        clauses += [Clause.INTERNATIONAL_TRAVEL, Clause.DEFINITIONS]
        notes.append("lines 1145-1146 and 249: Alaska is within the continental limits, so no DFA approval is needed")
    elif trip.destination.country != "US":
        raise ValueError("unreachable")
    if trip.passenger == Passenger.BOARD_MEMBER:
        if not trip.board_allowance_instead_of_salary:
            raise ValueError("a board member without the per diem in lieu of salary is not modelled")
        reasons.append(ReasonCode.OFFICER_OF_THE_STATE)
        clauses += [Clause.TRAVEL_REIMBURSEMENT, Clause.TRAVEL_CARD]
        notes.append("lines 375-377: a board member paid the per diem in lieu of salary is an officer of the state; "
                     "lines 1026-1028: the cardless account books non-entity travellers on official state business")
    return reasons, clauses, notes


def attendance(trip):
    """Line 1072-1073: prior written approval from the department head for attendance at any convention,
    association, or meeting, for expenses to be reimbursed. Returns (status, clauses): status 'ok', 'missing'
    (a conference or seminar without it) or 'unclear' (a working meeting without it: 'meeting' may or may not
    reach beyond conventions and associations)."""
    approved = any(record.subject == SignOffSubject.ATTENDANCE for record in trip.sign_offs)
    if trip.purpose_kind in (Purpose.CONFERENCE, Purpose.TRAINING, Purpose.MEETING) and approved:
        return "ok", [Clause.CONFERENCES]
    if approved:
        return "ok", []
    if trip.purpose_kind in (Purpose.CONFERENCE, Purpose.TRAINING):
        return "missing", []
    if trip.purpose_kind == Purpose.MEETING:
        return "unclear", []
    return "ok", []


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers of every search it pins: the decision, and every accepted
    offer id, cabin, reason, approver and section. ``hidden`` (the scenario's answer_key_inputs) is unused by
    this handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    if any(offer.return_segments for offer in offers):
        raise ValueError("round-trip fares are not modelled: every case buys a one-way ticket")
    if trip.passenger == Passenger.FAMILY_MEMBER:
        return family(trip)
    if trip.passenger == Passenger.INDEPENDENT_CONTRACTOR:
        raise ValueError("an independent contractor is not modelled")
    if trip.purpose_kind == Purpose.VACATION:
        return vacation(trip)
    if trip.free_ticket_coupon:
        return coupon(trip)
    status, extra_clauses = attendance(trip)
    decided = decide(trip, offers)
    if status == "ok":
        if decided["decision"] == Decision.BOOK:
            # The approval to attend is on file; a reader may cite the section that asks for it.
            decided["clauses"] = by_value([*decided["clauses"], *extra_clauses])
        return decided
    if decided["decision"] != Decision.BOOK:
        raise ValueError("an attendance hold over another hold is not modelled")
    held = [offer for offer in offers if offer.offer_id in decided["offer_ids"]]
    if status == "missing":
        return answer(Decision.FLAG_FOR_APPROVAL, held, [ReasonCode.APPROVAL_REQUIRED], ATTENDANCE_ROLES,
                      [Clause.CONFERENCES],
                      "Lines 1072-1073: attendance at a convention or seminar needs the department head's prior "
                      "written approval for the expenses to be reimbursed, and it is not yet given. Hold the fare the "
                      "handbook would buy: " + decided["explanation"])
    return answer(Decision.FLAG_FOR_APPROVAL, held, UNCLEAR_REASONS, [Approver.NOT_NAMED, *ATTENDANCE_ROLES],
                  [Clause.CONFERENCES],
                  "Lines 1072-1073 require the department head's prior written approval for 'attendance at any "
                  "convention, association, or meeting'. The section is about conferences, and this is a working "
                  "meeting with a partner agency: whether 'meeting' reaches it is unclear. With no approval on file, "
                  "hold the fare: " + decided["explanation"], phrase=MEETING_PHRASE)


def family(trip):
    if not trip.accompanies:
        raise ValueError("a family member with nobody accompanied is not modelled")
    return answer(Decision.REFUSE, [], [ReasonCode.COMPANION_NOT_COVERED, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED],
                  [Approver.NONE, *(record.role for record in trip.sign_offs)],
                  [Clause.INTRODUCTION, Clause.TRAVEL_REIMBURSEMENT, Clause.COMBINING_PERSONAL_TRAVEL,
                   Clause.LODGING_WITH_NON_EMPLOYEE, Clause.TRAVEL_CARD],
                  "Lines 202-203: the rules cover state officers and employees on official state business; line "
                  "1028: the cardless account books non-employees only when they travel on official state business; "
                  "lines 1216-1217: when a family member travels along, the employee claims the single room rate "
                  "only; line 648: the agency incurs no expense beyond the business trip. The state buys no ticket "
                  "for the employee's husband or wife.")


def vacation(trip):
    return answer(Decision.REFUSE, [], [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                  on_file(trip),
                  [Clause.COMBINING_PERSONAL_TRAVEL, Clause.TRAVEL_REIMBURSEMENT, Clause.INTRODUCTION],
                  "Lines 642-644: business and personal travel may be combined only when the primary purpose of the "
                  "trip is official state business; here the trip is a family vacation with an optional courtesy "
                  "call nobody asked for, and lines 648-649: the agency incurs no expense beyond the business it "
                  "would have had. The state buys no ticket.")


def coupon(trip):
    return answer(Decision.REFUSE, [], [ReasonCode.FREE_TICKET_MUST_BE_USED], on_file(trip),
                  [Clause.FREQUENT_FLYER_AWARDS, Clause.PUBLIC_CARRIER],
                  "Lines 884-888: a bonus earned on official state travel shall be used to offset later official "
                  "travel, and under no circumstances can the traveller keep it for personal use; free ticket coupons "
                  "are used to offset official state travel costs. The free coupon covers this trip and expires "
                  "before any other planned state trip, so it is used and the state buys no ticket.")


def decide(trip, offers):
    reasons, clauses, notes = scope(trip)
    if trip.requested_cabin == Cabin.BUSINESS:
        if trip.other_origin or trip.other_date or trip.wants_nonstop:
            raise ValueError("a business request with routing wishes is not modelled")
        return business(trip, offers, reasons, clauses, notes)
    if trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")
    wishes = [bool(trip.other_origin), bool(trip.other_date), trip.wants_nonstop]
    if sum(wishes) > 1:
        raise ValueError("more than one routing wish is not modelled")
    if trip.other_origin:
        return other_airport(trip, offers, reasons, clauses, notes)
    if trip.other_date:
        return other_day(trip, offers, reasons, clauses, notes)
    main = [offer for offer in offers if leaves_from(offer) == (trip.origin.code, trip.travel_date)]
    if len(main) != len(offers):
        raise ValueError("offers off the trip's route and date without a wish that names them")
    if trip.wants_nonstop:
        return nonstop(trip, main, reasons, clauses, notes)
    lowest, low_reasons, low_notes = lowest_economy(trip, main)
    if len({offer.stops for offer in lowest}) > 1:
        raise ValueError("tied lowest fares with different stops are not modelled outside a nonstop wish")
    why = ["Line 370: the lowest logical rate available", *low_notes, *notes]
    if any(cabin_status(offer) is not False for offer in in_cabin(main, Cabin.BUSINESS)):
        why.append("business is not asked for, so lines 868-872 do not come into it")
    return answer(Decision.BOOK, lowest, [*reasons, *low_reasons], on_file(trip), [*LOWEST_CLAUSES, *clauses],
                  "; ".join(why) + ".")


def business(trip, offers, reasons, clauses, notes):
    """A business request. Lines 868-872: business may be authorized if at least one flight segment exceeds 6
    hours, and is not reimbursable unless approved in advance by an eWaiver the agency head signs and OPTFM
    approves before the trip. Line 471: universities do not submit eWaivers and follow their own waiver
    procedure."""
    if trip.travel_advance_cents:
        raise ValueError("a cash advance on a business request is not modelled")
    main = [offer for offer in offers if leaves_from(offer) == (trip.origin.code, trip.travel_date)]
    offered = logical(trip, in_cabin(main, Cabin.BUSINESS))
    sure = [offer for offer in offered if cabin_status(offer) is True]
    maybe = [offer for offer in offered if cabin_status(offer) is None]
    wanted = cheapest(sure)
    if trip.passenger == Passenger.UNIVERSITY_EMPLOYEE:
        approved = signed(trip, SignOffSubject.UNIVERSITY_WAIVER, Covers.BUSINESS_CLASS, Approver.UNIVERSITY_TRAVEL_OFFICE)
        given = [ReasonCode.UNIVERSITY_WAIVER_PROCESS]
        source = ("line 471: universities are exempt from submitting eWaivers and follow the university's own "
                  "waiver procedure, under which business class on this trip is approved")
    else:
        approved = (signed(trip, SignOffSubject.EWAIVER_APPROVED, Covers.BUSINESS_CLASS, Approver.STATE_TRAVEL_OFFICE)
                    and signed(trip, SignOffSubject.EWAIVER_SIGNED, Covers.BUSINESS_CLASS, Approver.AGENCY_HEAD))
        given = [ReasonCode.EWAIVER_APPROVED]
        source = ("lines 871-872: the eWaiver signed by the agency head was approved by OPTFM before the trip")
    pending = (not approved and signed(trip, SignOffSubject.EWAIVER_SIGNED, Covers.BUSINESS_CLASS, Approver.AGENCY_HEAD)
               and bool(trip.awaiting))
    if maybe and (not wanted or any(offer.fare_cents < wanted[0].fare_cents for offer in maybe)):
        if not pending or wanted:
            raise ValueError("a 360-minute segment outside a pending eWaiver is not modelled")
        lowest, _, _ = lowest_economy(trip, main)
        held = [*cheapest(maybe), *lowest]
        return answer(Decision.FLAG_FOR_APPROVAL, held, UNCLEAR_REASONS,
                      [Approver.NOT_NAMED, Approver.STATE_TRAVEL_OFFICE], CABIN_CLAUSES,
                      "Lines 868-869: business may be authorized 'if at least one of the flight segments exceeds 6 "
                      "hours', and the longest segment is exactly 360 minutes, which does not exceed 6 hours; but the "
                      "eWaiver form's own reason (line 453) is business 'six hours or longer non-stop', which it meets. "
                      "On the first reading the answer is the lowest economy fare; on the second, the business fare "
                      "held for OPTFM's approval. Hold either.", phrase=SEGMENT_PHRASE)
    if approved:
        if not wanted:
            raise ValueError("an approved waiver with no qualifying business offer is not modelled")
        skipped = [offer for offer in offered if cabin_status(offer) is False and offer.fare_cents < wanted[0].fare_cents]
        why = [source, ("lines 868-869: a segment exceeds 6 hours, so business may be authorized: the cheapest "
               "business fare that qualifies (line 370)")]
        if skipped:
            why.append("a cheaper business fare flies no segment over 6 hours, so it cannot be authorized")
        return answer(Decision.BOOK, wanted, [*given, ReasonCode.LONG_FLIGHT_APPROVED, ReasonCode.INTERNATIONAL_LONG_FLIGHT,
                                              *reasons], on_file(trip),
                      [*CABIN_CLAUSES, *clauses], "; ".join([*why, *notes]) + ".")
    if not pending:
        raise ValueError("a business request with no eWaiver signed is not modelled")
    if wanted:
        return answer(Decision.FLAG_FOR_APPROVAL, wanted, [ReasonCode.APPROVAL_REQUIRED], [Approver.STATE_TRAVEL_OFFICE],
                      CABIN_CLAUSES,
                      "Lines 868-869: a segment exceeds 6 hours, so business may be authorized; lines 870-872: it is "
                      "not reimbursable unless approved in advance, and the agency head's eWaiver is still waiting for "
                      "OPTFM's approval. Hold the cheapest qualifying business fare for the State Travel Office.")
    lowest, _, low_notes = lowest_economy(trip, main)
    # The reason names why business is declined (the segment rule), so LOWEST_FARE is not accepted.
    return answer(Decision.BOOK, lowest, [ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET, ReasonCode.UPGRADE_NOT_ELIGIBLE],
                  on_file(trip), [*CABIN_CLAUSES, *clauses],
                  "; ".join([("Lines 868-869: no segment exceeds 6 hours (nor reaches six hours, line 453), so business "
                             "cannot be authorized on this trip whatever the eWaiver says; the traveller asked for "
                             "economy then: the lowest logical rate (line 370)"), *low_notes, *notes]) + ".")


def nonstop(trip, main, reasons, clauses, notes):
    """A nonstop wish 'if the state will pay for it'. Lines 864-866: choose the flight with the fewest stops;
    line 853: the least expensive routing shall be used; lines 840-843 and 859-862: a fare above the lowest, or
    routing other than the most economical, needs an eWaiver to OPTFM."""
    lowest, low_reasons, low_notes = lowest_economy(trip, main)
    direct = cheapest([offer for offer in logical(trip, in_cabin(main, Cabin.ECONOMY)) if offer.stops == 0])
    if not direct:
        raise ValueError("a nonstop wish with no nonstop is not modelled")
    if direct[0].fare_cents == lowest[0].fare_cents:
        return answer(Decision.BOOK, direct, [ReasonCode.FEWEST_STOPS, ReasonCode.LOWEST_FARE, *reasons], on_file(trip),
                      [*AIR_CLAUSES, *clauses],
                      "Lines 864-866: choose the flight with the fewest stops; the nonstop costs the same as the "
                      "cheapest connection, so it is the lowest logical rate too (line 370) and needs no eWaiver.")
    approved = signed(trip, SignOffSubject.EWAIVER_APPROVED, Covers.NONSTOP_FARE, Approver.STATE_TRAVEL_OFFICE)
    if approved:
        if not signed(trip, SignOffSubject.ROUTING, Covers.NONSTOP_FARE, Approver.AGENCY_HEAD):
            raise ValueError("a nonstop eWaiver without the agency head's routing is not modelled")
        return answer(Decision.BOOK, direct, [ReasonCode.EWAIVER_APPROVED, *reasons], on_file(trip),
                      [*AIR_CLAUSES, Clause.EWAIVER_REQUEST_FORM, *clauses],
                      "Lines 859-862: the agency head specified the nonstop routing and the eWaiver for paying above the "
                      "lowest fare was approved by OPTFM (lines 840-843): the cheapest nonstop.")
    other = [record for record in trip.sign_offs if record.subject == SignOffSubject.EWAIVER_APPROVED]
    why = [("Line 853: the least expensive routing shall be used; lines 840-843: a fare above the lowest needs an "
           "eWaiver submitted before booking, and none covers this fare")]
    if other:
        why.append("the eWaiver on file covers lodging, not the airfare")
    # The ground for declining the nonstop is the lowest-fare rule itself, so LOWEST_FARE stands beside the codes
    # that name the dearer nonstop and the missing waiver.
    return answer(Decision.BOOK, lowest, [ReasonCode.LOWEST_FARE, ReasonCode.WAIVER_NOT_ON_FILE,
                                          ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE, ReasonCode.COST_SAVINGS,
                                          *low_reasons, *reasons], on_file(trip),
                  [*AIR_CLAUSES, Clause.TRAVEL_ROUTING, Clause.EWAIVER_REQUEST_FORM, *clauses],
                  "; ".join([*why, *low_notes, *notes]) + ".")


def other_airport(trip, offers, reasons, clauses, notes):
    """Lines 845-851: travellers use their local airport, which is assumed most economical; the airport is chosen
    on the costs most economical to the State, all costs considered."""
    if trip.origin.code != trip.local_airport.code:
        raise ValueError("a trip that does not start at the local airport is not modelled")
    airport(trip.other_origin)
    local = [offer for offer in offers if leaves_from(offer) == (trip.origin.code, trip.travel_date)]
    away = [offer for offer in offers if leaves_from(offer) == (trip.other_origin, trip.travel_date)]
    if len(local) + len(away) != len(offers):
        raise ValueError("offers off both airports' searches")
    home, _, _ = lowest_economy(trip, local)
    there, _, _ = lowest_economy(trip, away)
    total = there[0].fare_cents + trip.other_origin_added_cents
    if total == home[0].fare_cents:
        raise ValueError("equal total costs are not modelled")
    if total < home[0].fare_cents:
        return answer(Decision.BOOK, there, [ReasonCode.OTHER_AIRPORT_MORE_ECONOMICAL, ReasonCode.COST_SAVINGS,
                                             ReasonCode.LOWEST_FARE, *reasons], on_file(trip), [*AIR_CLAUSES, *clauses],
                      "Lines 849-851: the airport is chosen on the travel costs most economical to the State, all costs "
                      "considered: the other airport's fare plus the added mileage, parking and staff time is below the "
                      "local airport's lowest fare, so the local-airport assumption (lines 845-846) gives way.")
    # The ground for declining the other airport is the local-airport rule and its total-cost test; the local fare
    # is not the lowest fare listed, so LOWEST_FARE is not accepted.
    return answer(Decision.BOOK, home, [ReasonCode.LOCAL_AIRPORT_REQUIRED, ReasonCode.COST_SAVINGS, *reasons],
                  on_file(trip), [*AIR_CLAUSES, *clauses],
                  "Lines 845-846: travellers use their local airport; lines 849-851: the other airport's fare plus the "
                  "added mileage, parking and staff time costs the State more than the local airport's lowest fare.")


def other_day(trip, offers, reasons, clauses, notes):
    day = [offer for offer in offers if leaves_from(offer) == (trip.origin.code, trip.travel_date)]
    early = [offer for offer in offers if leaves_from(offer) == (trip.origin.code, trip.other_date)]
    if len(day) + len(early) != len(offers) or day_number(trip.other_date) >= day_number(trip.travel_date):
        raise ValueError("an other day must be earlier, with offers on both days only")
    if trip.other_date_kind == OtherDate.LOWER_FARE:
        return lower_fare_day(trip, day, early, reasons, clauses, notes)
    if trip.other_date_kind == OtherDate.LEAVE_FIRST:
        return leave_first(trip, day, early, reasons, clauses, notes)
    raise ValueError("an other day without a kind is not modelled")


def lower_fare_day(trip, day, early, reasons, clauses, notes):
    """Lines 900-901: going a day early for a lower-priced penalty fare, the State pays the added lodging and meals
    'not to exceed the amount of savings in the airfare' (inclusive); lines 857-858: alternate dates should be
    considered when they lower fares. The traveller flies early only if it saves the State money overall."""
    if day_number(trip.travel_date) - day_number(trip.other_date) != 1:
        raise ValueError("only a day early is modelled")
    home, _, low_notes = lowest_economy(trip, day)
    before, _, _ = lowest_economy(trip, early)
    saving = home[0].fare_cents - before[0].fare_cents
    clauses = [Clause.AIRLINE_PENALTY_FARES, *AIR_CLAUSES, *clauses]
    if saving == trip.other_date_added_cents:
        raise ValueError("a saving equal to the added lodging and meals is not modelled")
    if saving > trip.other_date_added_cents:
        return answer(Decision.BOOK, before, [ReasonCode.EARLIER_DAY_SAVES, ReasonCode.COST_SAVINGS, ReasonCode.LOWEST_FARE,
                                              *reasons], on_file(trip), clauses,
                      "; ".join([("Lines 900-901: the day-early fare saves more than the added lodging and meals, which "
                                 "the State then pays in full; the total is lower, so fly the day before (lines "
                                 "857-858)"), *low_notes, *notes]) + ".")
    _, home_reasons, _ = lowest_economy(trip, day)
    return answer(Decision.BOOK, home, [ReasonCode.COST_SAVINGS, *home_reasons, *reasons], on_file(trip), clauses,
                  "; ".join([("Lines 900-901: the day-early fare saves less than the added lodging and meals, so it does "
                             "not save the State money overall (the State would pay the extra only up to the saving): "
                             "fly on the day of the business at its lowest logical fare"), *low_notes, *notes]) + ".")


def leave_first(trip, day, early, reasons, clauses, notes):
    """Lines 642-656: business and personal leave may be combined when the primary purpose is state business, the
    leave is approved, and the agency incurs no expenses beyond the business trip's."""
    if not trip.leave_approved or trip.other_date_added_cents:
        raise ValueError("leave days that are unapproved or cost the state lodging are not modelled")
    home, _, _ = lowest_economy(trip, day)
    before, _, _ = lowest_economy(trip, early)
    clauses = [Clause.COMBINING_PERSONAL_TRAVEL, *clauses]
    if before[0].fare_cents <= home[0].fare_cents:
        return answer(Decision.BOOK, before, [ReasonCode.LEAVE_DAYS_NO_EXTRA_COST, ReasonCode.LOWEST_FARE, *reasons],
                      on_file(trip), [*clauses, *AIR_CLAUSES],
                      "Lines 642-651: the trip's primary purpose is state business, the leave is approved, and the "
                      "earlier fare costs no more than the business day's lowest fare, so the agency incurs no extra "
                      "expense: book the earlier day the traveller asked for.")
    # The ground for declining the earlier day is the no-extra-expense condition of line 648, not the lowest fare.
    return answer(Decision.BOOK, home, [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.COST_SAVINGS, *reasons],
                  on_file(trip), [*clauses, *AIR_CLAUSES],
                  "Lines 647-648: the agency may incur no expenses beyond the business trip's, and the earlier fare is "
                  "dearer than the business day's lowest fare: book the business day, as the traveller asked otherwise.")
