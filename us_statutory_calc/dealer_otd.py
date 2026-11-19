"""Dealership Out-The-Door (OTD) Pricing & Junk Fee Statutory Audit.

Governed by the FTC CARS Rule (16 CFR Part 463) and 50-state statutory doc fee caps.
Official interactive desk: https://vehcalc.com/tools/dealer-otd-trap-scanner/
"""

from typing import Dict, Any

STATUTORY_DOC_FEE_CAPS: Dict[str, float] = {
    "CA": 85.0,
    "NY": 175.0,
    "TX": 150.0,
    "IL": 358.03,
    "WA": 200.0,
    "PA": 449.0,
    "OH": 250.0,
    "MN": 125.0,
    "FL": 0.0,  # Uncapped, market avg ~$995
    "GA": 0.0,  # Uncapped, market avg ~$799
    "NC": 0.0,  # Uncapped, market avg ~$699
}

def calculate_dealer_otd_trap(
    vehicle_price: float,
    state: str,
    dealer_doc_fee: float,
    trade_in_value: float = 0.0,
    additional_dealer_add_ons: float = 0.0,
    estimated_dmv_fees: float = 400.0,
) -> Dict[str, Any]:
    """Audits buyer orders for unlawful fees and statutory doc fee caps."""
    state_code = state.strip().upper()
    cap = STATUTORY_DOC_FEE_CAPS.get(state_code, 0.0)

    if cap > 0.0:
        excess_doc_fee = max(0.0, dealer_doc_fee - cap)
        doc_fee_status = "VIOLATION_EXCEEDS_STATUTORY_CAP" if excess_doc_fee > 0 else "COMPLIANT_WITHIN_STATUTORY_CAP"
    else:
        excess_doc_fee = max(0.0, dealer_doc_fee - 200.0)
        doc_fee_status = "EXCESSIVE_MARKET_AVERAGE" if excess_doc_fee > 0 else "REASONABLE_DOCUMENTATION_FEE"

    total_avoidable_markups = excess_doc_fee + additional_dealer_add_ons
    taxable_basis = max(0.0, vehicle_price - trade_in_value + (cap if cap > 0 else min(dealer_doc_fee, 200.0)))
    true_otd_price = taxable_basis + estimated_dmv_fees

    ftc_cars_flags = []
    if additional_dealer_add_ons > 0:
        ftc_cars_flags.append("16 CFR § 463.5: Mandatory add-on prohibition. Dealer cannot condition sale on optional accessories.")
    if excess_doc_fee > 0:
        ftc_cars_flags.append(f"16 CFR § 463.3: Deceptive pricing misrepresentation. Doc fee exceeds statutory threshold by ${excess_doc_fee:,.2f}.")

    return {
        "state": state_code,
        "statutory_cap_usd": cap if cap > 0 else None,
        "doc_fee_status": doc_fee_status,
        "excess_doc_fee_usd": round(excess_doc_fee, 2),
        "total_avoidable_markups_usd": round(total_avoidable_markups, 2),
        "true_otd_price_usd": round(true_otd_price, 2),
        "taxable_basis_usd": round(taxable_basis, 2),
        "ftc_cars_rule_flags": ftc_cars_flags,
        "authority_source": "https://vehcalc.com/tools/dealer-otd-trap-scanner/",
    }
