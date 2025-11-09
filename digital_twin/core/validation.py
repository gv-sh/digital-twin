"""
Input validation and constraint checking.

This module provides validation functions to ensure data integrity
and constraint satisfaction throughout the analysis.
"""

from typing import Any, List, Optional, Tuple
from digital_twin.core.models import (
    VehicleSpecs,
    OperationalProfile,
    FinancialParams,
    DecarbonizationScenario,
)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_positive(value: float, name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")


def validate_range(value: float, name: str, min_val: float, max_val: float) -> None:
    """Validate that a value is within a specified range."""
    if not (min_val <= value <= max_val):
        raise ValidationError(
            f"{name} must be between {min_val} and {max_val}, got {value}"
        )


def validate_percentage(value: float, name: str) -> None:
    """Validate that a value represents a valid percentage (0-1)."""
    validate_range(value, name, 0.0, 1.0)


def validate_vehicle_specs(specs: VehicleSpecs) -> Tuple[bool, List[str]]:
    """
    Validate vehicle specifications.

    Parameters
    ----------
    specs : VehicleSpecs
        Vehicle specifications to validate

    Returns
    -------
    tuple
        (is_valid, list of error messages)
    """
    errors = []

    try:
        validate_positive(specs.mass_kg, "Vehicle mass")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(specs.frontal_area_m2, "Frontal area")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_range(specs.drag_coefficient, "Drag coefficient", 0.1, 2.0)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_range(specs.rolling_resistance, "Rolling resistance", 0.001, 0.05)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(specs.max_range_km, "Maximum range")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_percentage(specs.energy_efficiency, "Energy efficiency")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(specs.initial_cost, "Initial cost")
    except ValidationError as e:
        errors.append(str(e))

    if specs.battery_degradation_rate is not None:
        try:
            validate_range(
                specs.battery_degradation_rate,
                "Battery degradation rate",
                0.0,
                1.0
            )
        except ValidationError as e:
            errors.append(str(e))

    return len(errors) == 0, errors


def validate_operational_profile(profile: OperationalProfile) -> Tuple[bool, List[str]]:
    """
    Validate operational profile.

    Parameters
    ----------
    profile : OperationalProfile
        Operational profile to validate

    Returns
    -------
    tuple
        (is_valid, list of error messages)
    """
    errors = []

    try:
        validate_positive(profile.annual_km, "Annual kilometers")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(profile.operating_days_per_year, "Operating days")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_range(
            profile.operating_days_per_year,
            "Operating days per year",
            1,
            365
        )
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(profile.daily_km, "Daily kilometers")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(profile.average_velocity_kmh, "Average velocity")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_percentage(profile.utilization_rate, "Utilization rate")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_percentage(profile.load_factor, "Load factor")
    except ValidationError as e:
        errors.append(str(e))

    # Check consistency: annual_km should be reasonable given daily operation
    expected_annual_km = profile.daily_km * profile.operating_days_per_year
    if abs(profile.annual_km - expected_annual_km) > expected_annual_km * 0.2:
        errors.append(
            f"Annual km ({profile.annual_km}) inconsistent with "
            f"daily km ({profile.daily_km}) × operating days "
            f"({profile.operating_days_per_year})"
        )

    return len(errors) == 0, errors


def validate_financial_params(params: FinancialParams) -> Tuple[bool, List[str]]:
    """
    Validate financial parameters.

    Parameters
    ----------
    params : FinancialParams
        Financial parameters to validate

    Returns
    -------
    tuple
        (is_valid, list of error messages)
    """
    errors = []

    try:
        validate_range(params.discount_rate, "Discount rate", 0.0, 0.5)
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(params.analysis_period_years, "Analysis period")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_range(
            params.analysis_period_years,
            "Analysis period years",
            1,
            30
        )
    except ValidationError as e:
        errors.append(str(e))

    # Price escalation rates should be reasonable (not negative, not too high)
    escalation_params = [
        (params.fuel_price_escalation, "Fuel price escalation"),
        (params.electricity_price_escalation, "Electricity price escalation"),
        (params.h2_price_escalation, "H2 price escalation"),
        (params.maintenance_cost_escalation, "Maintenance cost escalation"),
    ]

    for rate, name in escalation_params:
        try:
            validate_range(rate, name, -0.1, 0.3)  # -10% to +30% per year
        except ValidationError as e:
            errors.append(str(e))

    # Validate prices are positive
    try:
        validate_positive(params.fuel_price_per_unit, "Fuel price")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(params.electricity_price_per_kwh, "Electricity price")
    except ValidationError as e:
        errors.append(str(e))

    try:
        validate_positive(params.h2_price_per_kg, "Hydrogen price")
    except ValidationError as e:
        errors.append(str(e))

    return len(errors) == 0, errors


def validate_scenario(scenario: DecarbonizationScenario) -> Tuple[bool, List[str]]:
    """
    Validate complete decarbonization scenario.

    Parameters
    ----------
    scenario : DecarbonizationScenario
        Scenario to validate

    Returns
    -------
    tuple
        (is_valid, list of error messages)
    """
    errors = []

    # Validate vehicle specs
    is_valid_specs, spec_errors = validate_vehicle_specs(scenario.vehicle_specs)
    errors.extend(spec_errors)

    # Validate operational profile
    is_valid_ops, ops_errors = validate_operational_profile(
        scenario.operational_profile
    )
    errors.extend(ops_errors)

    # Validate financial parameters
    is_valid_fin, fin_errors = validate_financial_params(scenario.financial_params)
    errors.extend(fin_errors)

    return len(errors) == 0, errors


def check_range_feasibility(
    vehicle_range_km: float,
    daily_km: float,
    safety_margin: float = 0.2
) -> Tuple[bool, str]:
    """
    Check if vehicle range is feasible for daily operation.

    Parameters
    ----------
    vehicle_range_km : float
        Vehicle range in km
    daily_km : float
        Daily travel distance in km
    safety_margin : float
        Safety margin factor (default: 0.2 for 20%)

    Returns
    -------
    tuple
        (is_feasible, message)
    """
    required_range = daily_km * (1 + safety_margin)

    if vehicle_range_km >= required_range:
        return True, "Range is feasible"
    else:
        return False, (
            f"Insufficient range: vehicle range {vehicle_range_km:.0f} km "
            f"< required {required_range:.0f} km "
            f"(daily: {daily_km:.0f} km + {safety_margin*100:.0f}% margin)"
        )


__all__ = [
    "ValidationError",
    "validate_positive",
    "validate_range",
    "validate_percentage",
    "validate_vehicle_specs",
    "validate_operational_profile",
    "validate_financial_params",
    "validate_scenario",
    "check_range_feasibility",
]
