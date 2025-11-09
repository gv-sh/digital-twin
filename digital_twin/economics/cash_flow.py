"""Multi-year cash flow modeling."""

from typing import List
from digital_twin.core.constants import (
    FUEL_PRICE_ESCALATION,
    ELECTRICITY_PRICE_ESCALATION,
    MAINTENANCE_ESCALATION,
)


def calculate_annual_cashflows(
    annual_savings: float,
    years: int,
    escalation_rate: float = 0.0
) -> List[float]:
    """Calculate annual cash flows with escalation."""
    cashflows = []
    for year in range(1, years + 1):
        cf = annual_savings * ((1 + escalation_rate) ** (year - 1))
        cashflows.append(cf)
    return cashflows


def calculate_fuel_cost_with_escalation(
    base_fuel_cost: float,
    years: int,
    escalation_rate: float = FUEL_PRICE_ESCALATION
) -> List[float]:
    """Calculate fuel costs with price escalation."""
    return calculate_annual_cashflows(base_fuel_cost, years, escalation_rate)


__all__ = ["calculate_annual_cashflows", "calculate_fuel_cost_with_escalation"]
