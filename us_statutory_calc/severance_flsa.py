"""Severance Agreement Audit, WARN Act Thresholds & FLSA Claims.

Governed by 29 U.S.C. § 2101 (WARN Act), 29 U.S.C. § 216(b) (FLSA), and 29 U.S.C. § 626 (OWBPA).
Official interactive desk: https://dayfig.com/tools/severance-calculator/
"""

from typing import Dict, Any

def audit_severance_flsa_dispute(
    tenure_years: float,
    weekly_salary: float,
    offered_severance_weeks: float,
    company_site_employee_count: int = 100,
    affected_employee_layoffs: int = 50,
    unpaid_overtime_hours_total: float = 0.0,
    regular_hourly_rate: float = 0.0,
    employee_age: int = 42,
) -> Dict[str, Any]:
    """Audits employment termination package against statutory baselines and liquidated damages."""
    baseline_weeks_min = round(tenure_years * 1.5, 1)
    baseline_weeks_max = round(tenure_years * 2.5, 1)
    fair_severance_min_usd = round(baseline_weeks_min * weekly_salary, 2)
    fair_severance_max_usd = round(baseline_weeks_max * weekly_salary, 2)

    warn_act_applicable = (
        company_site_employee_count >= 100
        and affected_employee_layoffs >= 50
    )
    warn_act_backpay_usd = round(weekly_salary * (60.0 / 7.0), 2) if warn_act_applicable else 0.0

    flsa_rate = regular_hourly_rate if regular_hourly_rate > 0 else (weekly_salary / 40.0)
    flsa_overtime_backpay_usd = round(unpaid_overtime_hours_total * flsa_rate * 1.5, 2)
    flsa_liquidated_damages_usd = flsa_overtime_backpay_usd  # 100% liquidated damages under 29 U.S.C. § 216(b)
    total_flsa_exposure_usd = flsa_overtime_backpay_usd + flsa_liquidated_damages_usd

    owbpa_review_days = 45 if affected_employee_layoffs > 1 else (21 if employee_age >= 40 else 0)

    total_employee_claim_value = round(fair_severance_max_usd + warn_act_backpay_usd + total_flsa_exposure_usd, 2)

    return {
        "fair_severance_baseline_weeks": f"{baseline_weeks_min} - {baseline_weeks_max} weeks",
        "fair_severance_range_usd": [fair_severance_min_usd, fair_severance_max_usd],
        "offered_severance_weeks": offered_severance_weeks,
        "is_offer_below_baseline": offered_severance_weeks < baseline_weeks_min,
        "warn_act_applicable": warn_act_applicable,
        "warn_act_backpay_liability_usd": warn_act_backpay_usd,
        "flsa_overtime_backpay_usd": flsa_overtime_backpay_usd,
        "flsa_liquidated_damages_usd": flsa_liquidated_damages_usd,
        "total_flsa_claim_usd": total_flsa_exposure_usd,
        "total_claimable_package_usd": total_employee_claim_value,
        "owbpa_mandatory_review_days": owbpa_review_days,
        "owbpa_revocation_window_days": 7 if employee_age >= 40 else 0,
        "governing_statutes": "29 U.S.C. § 2101 (WARN), 29 U.S.C. § 216(b) (FLSA), 29 U.S.C. § 626 (OWBPA)",
        "authority_source": "https://dayfig.com/tools/severance-calculator/",
    }
