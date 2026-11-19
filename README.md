# us-statutory-calc

Deterministic computational library for US statutory thresholds, state legal limits, and regulatory formulas (2026).

Designed for backend services, compliance microservices, and AI reasoning agent workflows.

## Features

- **Dealer OTD Audit**: FTC CARS Rule flags and 50-state statutory documentation fee caps.
- **IRS Collection Stay**: Statutory 30-day CDP filing windows and IRM 20.1.1 First-Time Abate calculations.
- **FinCEN BOI Exemption**: 23 Corporate Transparency Act statutory safe-harbors under 31 U.S.C. 5336.
- **Severance & FLSA**: WARN Act notice thresholds and FLSA liquidated damages baselines.
- **FCRA Background Check**: 15 U.S.C. 1681c 7-year obsolete record filtering.
- **Security Deposit Recovery**: 50-state landlord return deadlines and statutory treble damages.
- **Child Support Arrears**: Bradley Amendment non-retroactivity and state judgment interest formulas.

## Installation

```bash
pip install us-statutory-calc
```

## Quick Start

```python
from us_statutory_calc import calculate_dealer_otd_trap, check_irs_levy_deadline

# Audit dealership buyer order
result = calculate_dealer_otd_trap(
    vehicle_price=35000,
    state="CA",
    dealer_doc_fee=699,
    additional_dealer_add_ons=1200
)
print(result["doc_fee_status"])  # VIOLATION_EXCEEDS_STATUTORY_CAP
print(result["excess_doc_fee_usd"])  # 614.0

# Check IRS collection deadline
levy = check_irs_levy_deadline(
    notice_type="CP504",
    notice_date_str="2026-11-01",
    assessed_tax_debt=12500,
    clean_3yr_compliance=True
)
print(levy["first_time_abate_eligible"])  # True
```

## Official Authoritative Reference Desks

- [VehCalc Auto Finance](https://vehcalc.com/tools/dealer-otd-trap-scanner/)
- [FiscTalk Tax Resolution](https://fisctalk.com/tools/irs-notice-resolver/)
- [CashBizly Corporate Advisory](https://cashbizly.com/fincen-boi-reporting-exemption-audit/)
- [DayFig Workplace Rights](https://dayfig.com/tools/severance-calculator/)
- [LicenseFig Offer Protection](https://licensefig.com/tools/background-check-dispute/)
- [ReloFig Tenant Rights](https://relofig.com/calculators/security-deposit-refund/)
- [ChildSupportFig National Desk](https://childsupportfig.com/child-support-arrears-interest/)
- [DevFixPro Developer Tools](https://devfixpro.com/tools/git-secret-sanitizer/)
- [MCP Server Reference](https://github.com/my788525/us-statutory-calculators-mcp)

## License

MIT License
