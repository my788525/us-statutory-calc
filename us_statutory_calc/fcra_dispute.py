"""FCRA Employment Background Check 7-Year Obsolete Record Restrictions.

Governed by Fair Credit Reporting Act, 15 U.S.C. § 1681c and 15 U.S.C. § 1681i.
Official interactive desk: https://licensefig.com/tools/background-check-dispute/
"""

from typing import Dict, Any

STRICT_SEVEN_YEAR_STATES = {"CA", "NY", "MA", "WA", "CO", "NV", "NM", "TX"}

def verify_fcra_background_rights(
    record_type: str,
    record_age_years: float,
    expected_salary_usd: float = 60000.0,
    state: str = "CA",
) -> Dict[str, Any]:
    """Audits employment background records for statutory obsolescence."""
    clean_type = record_type.strip().lower()
    clean_state = state.strip().upper()

    max_years = 7.0
    if "bankruptcy" in clean_type or "chapter_7" in clean_type:
        max_years = 10.0
    elif "chapter_13" in clean_type:
        max_years = 7.0

    salary_exception_applies = (expected_salary_usd >= 75000.0) and (clean_state not in STRICT_SEVEN_YEAR_STATES)

    if salary_exception_applies:
        is_unlawful = False
        rationale = "15 U.S.C. § 1681c(b)(3) exempts positions with salary equal to or exceeding $75,000 from federal 7-year obsolete reporting caps."
    else:
        is_unlawful = record_age_years > max_years
        if is_unlawful:
            rationale = f"Record age of {record_age_years} years exceeds statutory limit of {max_years} years under 15 U.S.C. § 1681c (or strict state Ban-the-Box rules in {clean_state})."
        else:
            rationale = f"Record is currently within legal {max_years}-year reporting window."

    return {
        "record_type": record_type,
        "record_age_years": record_age_years,
        "max_statutory_reporting_years": max_years,
        "state": clean_state,
        "is_reporting_unlawful": is_unlawful,
        "statutory_rationale": rationale,
        "mandatory_cra_reinvestigation_days": 30,
        "pre_adverse_action_hold_days": 5,
        "governing_statute": "15 U.S.C. § 1681c & 15 U.S.C. § 1681i(a)(1)",
        "authority_source": "https://licensefig.com/tools/background-check-dispute/",
    }
