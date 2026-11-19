"""IRS Notice Resolution, CDP 30-Day Deadline & Penalty Abatement.

Governed by 26 U.S.C. § 6330, § 6331 and Internal Revenue Manual (IRM) 20.1.1.
Official interactive desk: https://fisctalk.com/tools/irs-notice-resolver/
"""

from datetime import datetime, timedelta
from typing import Dict, Any

NOTICE_DEADLINE_DAYS: Dict[str, int] = {
    "CP504": 30,
    "LT11_LETTER_1058": 30,
    "CP2000": 30,
    "CP14": 21,
    "NOTICE_OF_DEFICIENCY_90D": 90,
}

def check_irs_levy_deadline(
    notice_type: str,
    notice_date_str: str,
    assessed_tax_debt: float,
    months_delinquent: int = 1,
    clean_3yr_compliance: bool = False,
) -> Dict[str, Any]:
    """Calculates statutory deadline to file Form 12153 and First-Time Abate eligibility."""
    clean_type = notice_type.strip().upper()
    days = NOTICE_DEADLINE_DAYS.get(clean_type, 30)

    try:
        notice_date = datetime.strptime(notice_date_str, "%Y-%m-%d").date()
    except ValueError:
        notice_date = datetime.now().date()

    statutory_deadline = notice_date + timedelta(days=days)
    today = datetime.now().date()
    days_remaining = (statutory_deadline - today).days
    is_stay_active = days_remaining >= 0

    ftp_rate_per_month = 0.005  # 0.5% per month, capped at 25% under IRC § 6651(a)(2)
    ftp_capped_rate = min(0.25, ftp_rate_per_month * max(1, months_delinquent))
    ftp_penalty_accrued = round(assessed_tax_debt * ftp_capped_rate, 2)

    fta_eligible = clean_3yr_compliance
    fta_savings_potential = ftp_penalty_accrued if fta_eligible else 0.0

    return {
        "notice_type": clean_type,
        "notice_date": notice_date.isoformat(),
        "statutory_deadline": statutory_deadline.isoformat(),
        "days_remaining": days_remaining,
        "is_collection_stay_active": is_stay_active,
        "action_required": "File IRS Form 12153 immediately to stay levy actions under IRC § 6330." if is_stay_active else "File Form 12153 Request for Equivalent Hearing or CNC hardship petition.",
        "failure_to_pay_penalty_usd": ftp_penalty_accrued,
        "first_time_abate_eligible": fta_eligible,
        "potential_penalty_savings_usd": fta_savings_potential,
        "governing_irm": "IRM 20.1.1.3.6.1 (First-Time Abate Administrative Waiver)",
        "authority_source": "https://fisctalk.com/tools/irs-notice-resolver/",
    }
