"""
Mathematical models for fleet decarbonization analysis.

This module provides comprehensive mathematical frameworks for:
- Extended emissions calculations
- Fleet durability and performance
- Performance and energy consumption
- Economic ROI with risk assessment
- Fleet optimization

Based on research from Paper A (emissions methodology) and Paper B (corrosion/degradation),
extended for multi-fuel fleet analysis with Queensland trial data validation.
"""

from digital_twin.models.equations import (
    # Emissions Models
    calculate_total_fleet_emissions,
    calculate_technology_trip_emissions,
    calculate_longitudinal_transition_emissions,

    # Degradation Models
    calculate_battery_performance_degradation,
    calculate_linear_degradation,
    calculate_operational_range,

    # Energy Models
    calculate_wheel_energy_per_trip,
    calculate_battery_electric_energy,
    calculate_hydrogen_energy,

    # Economic Models
    calculate_risk_adjusted_npv,
    calculate_breakeven_with_degradation,

    # Fleet Optimization
    optimize_technology_mix,
)

__all__ = [
    # Emissions Models
    "calculate_total_fleet_emissions",
    "calculate_technology_trip_emissions",
    "calculate_longitudinal_transition_emissions",

    # Degradation Models
    "calculate_battery_performance_degradation",
    "calculate_linear_degradation",
    "calculate_operational_range",

    # Energy Models
    "calculate_wheel_energy_per_trip",
    "calculate_battery_electric_energy",
    "calculate_hydrogen_energy",

    # Economic Models
    "calculate_risk_adjusted_npv",
    "calculate_breakeven_with_degradation",

    # Fleet Optimization
    "optimize_technology_mix",
]
