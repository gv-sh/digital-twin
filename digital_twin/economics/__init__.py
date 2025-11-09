"""Economics module - Financial analysis."""

from digital_twin.economics.roi import calculate_npv, calculate_irr, calculate_payback_period
from digital_twin.economics.cash_flow import calculate_annual_cashflows
from digital_twin.economics.depreciation import calculate_straight_line_depreciation
from digital_twin.economics.incentives import apply_capital_grant
from digital_twin.economics.risk import calculate_sharpe_ratio, calculate_var

__all__ = [
    "calculate_npv", "calculate_irr", "calculate_payback_period",
    "calculate_annual_cashflows", "calculate_straight_line_depreciation",
    "apply_capital_grant", "calculate_sharpe_ratio", "calculate_var",
]
