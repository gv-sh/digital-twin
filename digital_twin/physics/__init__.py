"""
Physics module - Physical models for energy, emissions, and degradation.

This module depends on core/ for types and constants.
"""

from digital_twin.physics.energy import (
    calculate_wheel_energy,
    calculate_energy_with_efficiency,
    calculate_regenerative_braking_energy,
)

from digital_twin.physics.emissions import (
    calculate_co2_emissions,
    calculate_nox_emissions,
    calculate_pm_emissions,
    calculate_total_emissions,
    calculate_emission_reduction,
)

from digital_twin.physics.degradation import (
    calculate_battery_degradation,
    calculate_cycle_degradation,
    calculate_combined_degradation,
)

from digital_twin.physics.thermodynamics import (
    calculate_battery_temperature_factor,
    calculate_hvac_load,
    calculate_air_density_correction,
)

__all__ = [
    # Energy
    "calculate_wheel_energy",
    "calculate_energy_with_efficiency",
    "calculate_regenerative_braking_energy",
    # Emissions
    "calculate_co2_emissions",
    "calculate_nox_emissions",
    "calculate_pm_emissions",
    "calculate_total_emissions",
    "calculate_emission_reduction",
    # Degradation
    "calculate_battery_degradation",
    "calculate_cycle_degradation",
    "calculate_combined_degradation",
    # Thermodynamics
    "calculate_battery_temperature_factor",
    "calculate_hvac_load",
    "calculate_air_density_correction",
]
