"""Depreciation calculations."""


def calculate_straight_line_depreciation(
    initial_cost: float,
    residual_value: float,
    useful_life_years: int
) -> float:
    """Calculate annual straight-line depreciation."""
    return (initial_cost - residual_value) / useful_life_years


def calculate_residual_value(
    initial_cost: float,
    residual_factor: float = 0.20
) -> float:
    """Calculate residual value."""
    return initial_cost * residual_factor


__all__ = ["calculate_straight_line_depreciation", "calculate_residual_value"]
