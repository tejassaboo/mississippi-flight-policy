"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-mississippi-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    EWAIVER_APPROVED = "EWAIVER_APPROVED"
    WAIVER_NOT_ON_FILE = "WAIVER_NOT_ON_FILE"
    LOCAL_AIRPORT_REQUIRED = "LOCAL_AIRPORT_REQUIRED"
    OTHER_AIRPORT_MORE_ECONOMICAL = "OTHER_AIRPORT_MORE_ECONOMICAL"
    EARLIER_DAY_SAVES = "EARLIER_DAY_SAVES"
    FEWEST_STOPS = "FEWEST_STOPS"
    ARRIVES_TOO_LATE = "ARRIVES_TOO_LATE"
    FREE_TICKET_MUST_BE_USED = "FREE_TICKET_MUST_BE_USED"
    INTERNATIONAL_TRAVEL_APPROVED = "INTERNATIONAL_TRAVEL_APPROVED"
    DOMESTIC_TRAVEL = "DOMESTIC_TRAVEL"
    UNIVERSITY_WAIVER_PROCESS = "UNIVERSITY_WAIVER_PROCESS"
    OFFICER_OF_THE_STATE = "OFFICER_OF_THE_STATE"
    LEAVE_DAYS_NO_EXTRA_COST = "LEAVE_DAYS_NO_EXTRA_COST"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    WEEKEND_TRAVEL_HOME = "WEEKEND_TRAVEL_HOME"
    WEEKEND_TRIP_NOT_EARNED = "WEEKEND_TRIP_NOT_EARNED"
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    EXTENDED_TRAVEL_SAVINGS = "EXTENDED_TRAVEL_SAVINGS"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    CANDIDATE_TRIP_NOT_COVERED = "CANDIDATE_TRIP_NOT_COVERED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: State of Mississippi, DFA State Travel Policy Rules & Regulations (December 2024).
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    ALDER_SHOAL = "alder-shoal"
    ASTER_CRANE = "aster-crane"
    BAYOU_THIMBLE = "bayou-thimble"
    BRAMBLE_FJORD = "bramble-fjord"
    COBALT_MEADOW = "cobalt-meadow"
    CORAL_WHISTLE = "coral-whistle"
    CYPRESS_LANTERN = "cypress-lantern"
    DAPPLE_CAIRN = "dapple-cairn"
    EMBER_PADDOCK = "ember-paddock"
    FENNEL_WICK = "fennel-wick"
    GARNET_ROOKERY = "garnet-rookery"
    HERON_QUARTZ = "heron-quartz"
    HOLLOW_BRINE = "hollow-brine"
    JUNIPER_QUOIN = "juniper-quoin"
    LICHEN_SPINDLE = "lichen-spindle"
    LUPINE_GROTTO = "lupine-grotto"
    MAGNOLIA_SEXTANT = "magnolia-sextant"
    MAPLE_DUNE = "maple-dune"
    MARIGOLD_OAR = "marigold-oar"
    MARTEN_SILL = "marten-sill"
    NIMBUS_GARLAND = "nimbus-garland"
    OSPREY_REED = "osprey-reed"
    PECAN_DRIFT = "pecan-drift"
    PEWTER_FEN = "pewter-fen"
    QUARTZ_ORIEL = "quartz-oriel"
    QUILL_HARBOR = "quill-harbor"
    SABLE_TERN = "sable-tern"
    SLATE_HERON = "slate-heron"
    TAMARACK_FERRY = "tamarack-ferry"
    THISTLE_MARSH = "thistle-marsh"
    VELVET_BIGHT = "velvet-bight"
    WREN_BASALT = "wren-basalt"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    AGENCY_HEAD = "AGENCY_HEAD"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"
    EXECUTIVE_DIRECTOR = "EXECUTIVE_DIRECTOR"
    STATE_TRAVEL_OFFICE = "STATE_TRAVEL_OFFICE"
    DFA = "DFA"
    UNIVERSITY_TRAVEL_OFFICE = "UNIVERSITY_TRAVEL_OFFICE"
    TRAVEL_COORDINATOR = "TRAVEL_COORDINATOR"
    SUPERVISOR = "SUPERVISOR"
    CHIEF_FINANCIAL_OFFICER = "CHIEF_FINANCIAL_OFFICER"
    STATE_AUDITOR = "STATE_AUDITOR"


class Clause(Enum):
    """The handbook's sections, by heading."""

    INTRODUCTION = "INTRODUCTION"
    DEFINITIONS = "DEFINITIONS"
    ADMINISTRATION = "ADMINISTRATION"
    TRAVEL_REIMBURSEMENT = "TRAVEL_REIMBURSEMENT"
    TRAVEL_ADVANCES = "TRAVEL_ADVANCES"
    EWAIVER_REQUEST_FORM = "EWAIVER_REQUEST_FORM"
    TRAVEL_VOUCHER = "TRAVEL_VOUCHER"
    TRAVEL_ROUTING = "TRAVEL_ROUTING"
    COMBINING_PERSONAL_TRAVEL = "COMBINING_PERSONAL_TRAVEL"
    VEHICLE_TRAVEL = "VEHICLE_TRAVEL"
    DRIVING_VERSUS_FLYING = "DRIVING_VERSUS_FLYING"
    PUBLIC_CARRIER = "PUBLIC_CARRIER"
    AIRLINE_GENERAL = "AIRLINE_GENERAL"
    FREQUENT_FLYER_AWARDS = "FREQUENT_FLYER_AWARDS"
    AIRLINE_PENALTY_FARES = "AIRLINE_PENALTY_FARES"
    RESERVATION_CHANGES = "RESERVATION_CHANGES"
    TRAVEL_CARD = "TRAVEL_CARD"
    CONFERENCES = "CONFERENCES"
    CONFERENCE_AIRLINES = "CONFERENCE_AIRLINES"
    CONFERENCE_HOTELS = "CONFERENCE_HOTELS"
    INTERNATIONAL_TRAVEL = "INTERNATIONAL_TRAVEL"
    APPROVAL_FORMS = "APPROVAL_FORMS"
    LODGING = "LODGING"
    LODGING_WITH_NON_EMPLOYEE = "LODGING_WITH_NON_EMPLOYEE"
    MEAL_ALLOWANCES = "MEAL_ALLOWANCES"
    CONTRACT_TRAVEL_AGENCIES = "CONTRACT_TRAVEL_AGENCIES"
    OTHER_EXPENSES = "OTHER_EXPENSES"


class Passenger(Enum):
    STATE_EMPLOYEE = "STATE_EMPLOYEE"
    UNIVERSITY_EMPLOYEE = "UNIVERSITY_EMPLOYEE"
    BOARD_MEMBER = "BOARD_MEMBER"
    FAMILY_MEMBER = "FAMILY_MEMBER"
    INDEPENDENT_CONTRACTOR = "INDEPENDENT_CONTRACTOR"


class Purpose(Enum):
    CONFERENCE = "CONFERENCE"
    MEETING = "MEETING"
    TRAINING = "TRAINING"
    SITE_INSPECTION = "SITE_INSPECTION"
    AUDIT_FIELDWORK = "AUDIT_FIELDWORK"
    HEARING = "HEARING"
    VACATION = "VACATION"


class OtherDate(Enum):
    NONE = "NONE"
    LOWER_FARE = "LOWER_FARE"
    LEAVE_FIRST = "LEAVE_FIRST"


class SignOffSubject(Enum):
    ATTENDANCE = "ATTENDANCE"
    TRAVEL_AUTHORIZATION = "TRAVEL_AUTHORIZATION"
    EWAIVER_SIGNED = "EWAIVER_SIGNED"
    EWAIVER_APPROVED = "EWAIVER_APPROVED"
    ROUTING = "ROUTING"
    UNIVERSITY_WAIVER = "UNIVERSITY_WAIVER"
    TRAVEL_ADVANCE = "TRAVEL_ADVANCE"


class Covers(Enum):
    THE_TRIP = "THE_TRIP"
    BUSINESS_CLASS = "BUSINESS_CLASS"
    NONSTOP_FARE = "NONSTOP_FARE"
    LODGING = "LODGING"
    CASH_ADVANCE = "CASH_ADVANCE"


@dataclass
class SignOff(Output):
    role: Annotated[Approver, "Who signed: the signer's role"]
    name: Annotated[str, "Their name, or the office's name"]
    subject: Annotated[
        SignOffSubject,
        "What was signed: written approval to attend, DFA's authorization of the trip, an eWaiver form the agency's "
        "head has signed (still to be approved by OPTFM), an eWaiver OPTFM approved, a routing the agency's head "
        "specified, a waiver under a university's own procedure, or a cash advance",
    ]
    covers: Annotated[Covers, "What the sign-off is for: the trip itself, business class, a nonstop fare, lodging, or a cash advance"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their job title, or their relation to the employee they go with"]
    passenger: Annotated[Passenger, "What the person flying is to the state"]
    board_allowance_instead_of_salary: Annotated[bool, "For a board member: whether the state pays them a daily allowance for board service instead of a salary"]
    accompanies: Annotated[str, "The employee this person goes with, when the person flying is a family member; empty otherwise"]
    agency: Annotated[str, "The state agency, university or board the trip is for"]
    duty_station: Annotated[str, "The town of the traveller's official duty station"]
    local_airport: Annotated[Airport, "The airport that serves the traveller's duty station"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where it goes"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    must_land_by: Annotated[str, "The latest landing at the destination that still gets the traveller to the business: YYYY-MM-DD HH:MM, local time there"]
    other_origin: Annotated[str, "Another airport the traveller asks to leave from instead, as an IATA code; empty when none"]
    other_origin_added_cents: Annotated[int, "The travel coordinator's estimate, in cents, of the extra mileage, parking and staff time of leaving from that other airport; zero when none"]
    other_date: Annotated[str, "Another day to leave that the traveller names, YYYY-MM-DD; empty when none"]
    other_date_kind: Annotated[OtherDate, "Why that other day: a lower fare a day ahead of the business, or to spend leave first; NONE when no other day"]
    other_date_added_cents: Annotated[int, "Lodging and meals, in cents, the state would pay on top of the fare if the traveller leaves on that other day; zero when none"]
    leave_approved: Annotated[bool, "Whether leave for any days of the trip that are not business is approved"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    wants_nonstop: Annotated[bool, "Whether the traveller asks for a flight without a connection, even at a higher fare"]
    free_ticket_coupon: Annotated[str, "A free ticket coupon the traveller holds, what it came from, where it is good and until when; empty when none"]
    travel_advance_cents: Annotated[int, "A cash advance the traveller asks for, in cents; zero when none"]
    sign_offs: Annotated[list[SignOff], "Sign-offs already on file for this trip, each given before today"]
    awaiting: Annotated[str, "A sign-off asked for and not yet given, in plain words; empty when none"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
