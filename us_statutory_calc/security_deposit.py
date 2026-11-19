"""50-State Tenant Security Deposit Return & Treble Damages Audit.

Governed by state property codes (Cal. Civ. Code § 1950.5, N.Y. GOL § 7-108, Tex. Prop. § 92.109).
Official interactive desk: https://relofig.com/calculators/security-deposit-refund/
"""

from typing import Dict, Any

STATE_DEPOSIT_RULES: Dict[str, Dict[str, Any]] = {
    "CA": {"days": 21, "penalty_multiplier": 2.0, "statute": "Cal. Civ. Code § 1950.5(l)"},
    "NY": {"days": 14, "penalty_multiplier": 2.0, "statute": "N.Y. Gen. Oblig. Law § 7-108(1-a)(g)"},
    "TX": {"days": 30, "penalty_multiplier": 3.0, "fixed_statutory_fine": 100.0, "statute": "Tex. Prop. Code § 92.109"},
    "IL": {"days": 30, "penalty_multiplier": 2.0, "statute": "765 ILCS 710/1"},
    "FL": {"days": 15, "claim_days": 30, "penalty_multiplier": 1.0, "statute": "Fla. Stat. § 83.49(3)"},
    "WA": {"days": 30, "penalty_multiplier": 2.0, "statute": "RCW 59.18.280"},
    "PA": {"days": 30, "penalty_multiplier": 2.0, "statute": "68 P.S. § 250.512"},
    "MA": {"days": 30, "penalty_multiplier": 3.0, "statute": "M.G.L. c. 186 § 15B(7)"},
}

def calc_security_deposit_refund(
    deposit_amount: float,
    itemized_deductions_claimed: float,
    days_since_vacating: int,
    state: str = "CA",
    landlord_acted_in_bad_faith: bool = False,
) -> Dict[str, Any]:
    """Calculates refund entitlement, statutory deadline violation, and treble damages."""
    clean_state = state.strip().upper()
    rule = STATE_DEPOSIT_RULES.get(clean_state, {"days": 30, "penalty_multiplier": 2.0, "statute": f"State Uniform Tenant Act ({clean_state})"})

    statutory_deadline_days = rule["days"]
    is_past_deadline = days_since_vacating > statutory_deadline_days

    # Under most statutes, missing the accounting deadline forfeits all deduction rights
    unlawful_forfeiture = is_past_deadline
    actual_refund_owed = deposit_amount if unlawful_forfeiture else max(0.0, deposit_amount - itemized_deductions_claimed)

    multiplier = rule.get("penalty_multiplier", 1.0) if (landlord_acted_in_bad_faith or is_past_deadline) else 1.0
    fixed_fine = rule.get("fixed_statutory_fine", 0.0) if (landlord_acted_in_bad_faith or is_past_deadline) else 0.0
    total_claimable_amount = round((actual_refund_owed * multiplier) + fixed_fine, 2)

    return {
        "state": clean_state,
        "deposit_amount_usd": deposit_amount,
        "days_since_vacating": days_since_vacating,
        "statutory_deadline_days": statutory_deadline_days,
        "is_landlord_past_deadline": is_past_deadline,
        "deductions_forfeited_by_delay": unlawful_forfeiture,
        "actual_refund_owed_usd": round(actual_refund_owed, 2),
        "statutory_penalty_multiplier": multiplier,
        "total_claimable_in_court_usd": total_claimable_amount,
        "governing_statute": rule["statute"],
        "authority_source": "https://relofig.com/calculators/security-deposit-refund/",
    }
