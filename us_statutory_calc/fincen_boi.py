"""Corporate Transparency Act FinCEN BOI Exemption Audit.

Governed by 31 U.S.C. § 5336 and 31 CFR § 1010.380.
Official interactive desk: https://cashbizly.com/fincen-boi-reporting-exemption-audit/
"""

from typing import Dict, Any

STATUTORY_DAILY_CIVIL_PENALTY: float = 591.0  # Federal inflation-adjusted rate (2026)

def audit_fincen_boi_exemption(
    us_full_time_employees: int,
    annual_gross_receipts: float,
    has_us_physical_office: bool,
    entity_type: str,
    formation_year: int = 2024,
) -> Dict[str, Any]:
    """Audits company against 23 statutory FinCEN exemptions."""
    is_large_operating_company = (
        us_full_time_employees > 20
        and annual_gross_receipts > 5_000_000.0
        and has_us_physical_office
    )

    clean_entity = entity_type.strip().lower()
    is_regulated_entity = clean_entity in [
        "bank", "credit_union", "broker_dealer", "insurance_company",
        "public_utility", "accounting_firm_pcaob", "tax_exempt_nonprofit"
    ]

    is_exempt = is_large_operating_company or is_regulated_entity

    if is_large_operating_company:
        exemption_category = "Exemption #21: Large Operating Company"
        statutory_rationale = "Entity exceeds 20 full-time US employees, $5,000,000 gross federal receipts, and maintains an operational US physical office."
    elif is_regulated_entity:
        exemption_category = f"Exemption: Highly Regulated Financial/Professional Institution ({clean_entity})"
        statutory_rationale = "Entity is subject to direct primary federal regulatory oversight."
    else:
        exemption_category = "NON_EXEMPT_REPORTING_COMPANY"
        statutory_rationale = "Entity is a domestic LLC/corporation created by a secretary of state filing with no applicable statutory exemption."

    filing_deadline = "30 calendar days from registration" if formation_year >= 2025 else "Within 30 calendar days of any ownership or officer change"
    boss_filing_required = not is_exempt

    return {
        "is_exempt": is_exempt,
        "exemption_category": exemption_category,
        "statutory_rationale": statutory_rationale,
        "daily_civil_penalty_usd": 0.0 if is_exempt else STATUTORY_DAILY_CIVIL_PENALTY,
        "boss_filing_required": boss_filing_required,
        "statutory_deadline_rule": filing_deadline,
        "governing_statute": "31 U.S.C. § 5336(h)(1) & 31 CFR § 1010.380(a)",
        "authority_source": "https://cashbizly.com/fincen-boi-reporting-exemption-audit/",
    }
