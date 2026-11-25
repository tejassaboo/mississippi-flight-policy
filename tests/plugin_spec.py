"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "mississippi-travel-2024" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. It has no rule on several
# employees on one flight and none on overnight stops, so neither overlay is required.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "waiver", "ewaiver", "university", "board", "officer", "spouse", "husband", "wife", "family", "vacation",
    "leave", "personal", "coupon", "award", "miles", "free", "local", "airport", "nonstop", "direct", "stops",
    "connection", "routing", "segment", "conference", "meeting", "convention", "attendance", "alaska", "hawaii",
    "international", "domestic", "continental", "dfa", "optfm", "agency", "head", "director", "advance", "driving",
    "unrestricted", "penalty", "lowest", "logical", "late", "deadline", "day", "early", "saving", "savings",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Passenger, contract.Purpose, contract.OtherDate, contract.SignOffSubject, contract.Covers]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section).
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 13

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False).
DURATION_CASES = [
    ("segment", [361], [], True),  # strict: "exceeds 6 hours"
    ("segment", [360], [], False),
    ("segment", [110, 470], [85], True),  # the long segment of a connection counts
    ("segment", [230, 335], [70], False),  # segments are never added together
    ("segment", [225, 360], [80], False),
    ("waiver-form", [360], [], True),  # inclusive: "six hours or longer non-stop"
    ("waiver-form", [359], [], False),
    ("waiver-form", [225, 360], [80], True),
    ("waiver-form", [230, 335], [70], False),
]
