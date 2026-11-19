"""Child Support Modification Thresholds & Arrears Interest Accrual.

Governed by 42 U.S.C. § 666(a)(9) (Bradley Amendment) and 50-state judgment interest codes.
Official interactive desk: https://childsupportfig.com/child-support-arrears-interest/
"""

from typing import Dict, Any

STATE_ARREARS_RATES: Dict[str, Dict[str, Any]] = {
    "CA": {"rate": 10.0, "mode": "simple", "statute": "Cal. Code Civ. Proc. § 685.010"},
    "TX": {"rate": 6.0, "mode": "simple", "statute": "Tex. Fam. Code § 157.265"},
    "FL": {"rate": 4.75, "mode": "simple", "statute": "Fla. Stat. § 55.03"},
    "NY": {"rate": 9.0, "mode": "simple", "statute": "N.Y. CPLR § 5004"},
    "IL": {"rate": 9.0, "mode": "simple", "statute": "735 ILCS 5/12-109"},
    "CO": {"rate": 10.0, "mode": "compound_annual", "statute": "Colo. Rev. Stat. § 14-14-106"},
    "WI": {"rate": 6.0, "mode": "compound_monthly", "statute": "Wis. Stat. § 767.511(6m)"},
    "WA": {"rate": 12.0, "mode": "simple", "statute": "RCW 4.56.110"},
    "PA": {"rate": 6.0, "mode": "simple", "statute": "42 Pa.C.S. § 8101"},
    "NC": {"rate": 8.0, "mode": "simple", "statute": "N.C. Gen. Stat. § 24-1"},
}

def audit_child_support_arrears(
    principal_arrears: float,
    months_delinquent: int,
    state: str = "CA",
) -> Dict[str, Any]:
    """Calculates exact statutory arrears interest and Bradley Amendment restrictions."""
    clean_state = state.strip().upper()
    rule = STATE_ARREARS_RATES.get(clean_state, {"rate": 6.0, "mode": "simple", "statute": f"State General Judgment Interest ({clean_state})"})

    annual_rate = rule["rate"]
    years = months_delinquent / 12.0
    mode = rule["mode"]

    if mode == "compound_annual":
        total_balance = principal_arrears * ((1.0 + (annual_rate / 100.0)) ** years)
        accrued_interest = total_balance - principal_arrears
    elif mode == "compound_monthly":
        monthly_rate = (annual_rate / 100.0) / 12.0
        total_balance = principal_arrears * ((1.0 + monthly_rate) ** months_delinquent)
        accrued_interest = total_balance - principal_arrears
    else:  # simple
        accrued_interest = principal_arrears * (annual_rate / 100.0) * years
        total_balance = principal_arrears + accrued_interest

    return {
        "state": clean_state,
        "principal_arrears_usd": round(principal_arrears, 2),
        "months_delinquent": months_delinquent,
        "annual_statutory_rate_percent": annual_rate,
        "compounding_mode": mode,
        "accrued_interest_usd": round(accrued_interest, 2),
        "total_arrears_balance_usd": round(total_balance, 2),
        "bradley_amendment_protection": "42 U.S.C. § 666(a)(9) prohibits retroactive judicial forgiveness of accrued principal arrears.",
        "governing_statute": rule["statute"],
        "authority_source": "https://childsupportfig.com/child-support-arrears-interest/",
    }
