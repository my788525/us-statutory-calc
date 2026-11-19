"""US Statutory Calculators & Federal Audit Frameworks (2026).

Deterministic legal, tax, and regulatory calculations for Python applications and AI agents.
"""

from .dealer_otd import calculate_dealer_otd_trap, STATUTORY_DOC_FEE_CAPS
from .irs_levy import check_irs_levy_deadline, NOTICE_DEADLINE_DAYS
from .fincen_boi import audit_fincen_boi_exemption, STATUTORY_DAILY_CIVIL_PENALTY
from .severance_flsa import audit_severance_flsa_dispute
from .fcra_dispute import verify_fcra_background_rights
from .security_deposit import calc_security_deposit_refund, STATE_DEPOSIT_RULES
from .child_support import audit_child_support_arrears, STATE_ARREARS_RATES

__version__ = "1.0.0"

__all__ = [
    "calculate_dealer_otd_trap",
    "STATUTORY_DOC_FEE_CAPS",
    "check_irs_levy_deadline",
    "NOTICE_DEADLINE_DAYS",
    "audit_fincen_boi_exemption",
    "STATUTORY_DAILY_CIVIL_PENALTY",
    "audit_severance_flsa_dispute",
    "verify_fcra_background_rights",
    "calc_security_deposit_refund",
    "STATE_DEPOSIT_RULES",
    "audit_child_support_arrears",
    "STATE_ARREARS_RATES",
]
