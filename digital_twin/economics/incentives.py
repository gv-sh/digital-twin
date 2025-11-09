"""Government incentives and subsidies."""


def apply_capital_grant(initial_cost: float, grant_amount: float) -> float:
    """Apply capital grant to reduce initial cost."""
    return initial_cost - grant_amount


def calculate_tax_benefit(
    annual_depreciation: float,
    tax_rate: float = 0.30
) -> float:
    """Calculate annual tax benefit from depreciation."""
    return annual_depreciation * tax_rate


__all__ = ["apply_capital_grant", "calculate_tax_benefit"]
