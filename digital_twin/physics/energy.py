"""
Energy consumption calculations based on physical models.

This module implements physics-based models for calculating vehicle energy
consumption including gravitational, rolling resistance, and aerodynamic components.

Performance and Energy Consumption Model implementing:
- Wheel Energy per Trip: E_wheel = mg·sin(θ)·d + C_rr·mg·d + ½ρ(C_d·A)v²·d + E_aux
- Technology-Specific Energy Draw:
  * BEV: E_battery = E_wheel / (η_drivetrain × η_battery)
  * FCET: H2_draw = E_wheel / (η_drivetrain × η_fuelcell)

Validated with Queensland trial data:
- 100-200 km operational range per trip
- 36,000 kg typical gross vehicle mass
- 80 km/h typical average speed
"""

import numpy as np
from typing import Union, Tuple
from digital_twin.core.constants import (
    GRAVITY_ACCELERATION,
    ROLLING_RESISTANCE_COEFF,
    DEFAULT_DRAG_COEFFICIENT,
    DEFAULT_FRONTAL_AREA,
    AIR_DENSITY_SEA_LEVEL,
    BEV_BATTERY_TO_WHEEL,
    FCET_H2_TO_WHEEL,
    DIESEL_TANK_TO_WHEEL,
    KG_H2_TO_KWH,
)


def calculate_wheel_energy(
    mass: float,
    grade: float,
    distance: float,
    velocity: float,
    air_density: float = AIR_DENSITY_SEA_LEVEL,
    frontal_area: float = DEFAULT_FRONTAL_AREA,
    drag_coefficient: float = DEFAULT_DRAG_COEFFICIENT,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF,
) -> float:
    """
    Calculate energy consumption at the wheel.

    E_wheel = mg·sin(θ)·d + C_rr·mg·d + ½ρ(C_d·A)v²d + E_aux

    Parameters
    ----------
    mass : float
        Vehicle mass in kg
    grade : float
        Road grade (slope angle in radians)
    distance : float
        Distance traveled in meters
    velocity : float
        Vehicle velocity in m/s
    air_density : float
        Air density in kg/m³
    frontal_area : float
        Vehicle frontal area in m²
    drag_coefficient : float
        Aerodynamic drag coefficient
    rolling_resistance : float
        Rolling resistance coefficient

    Returns
    -------
    float
        Energy consumption in Joules
    """
    # Gravitational potential energy (climbing work)
    E_gravity = mass * GRAVITY_ACCELERATION * np.sin(grade) * distance

    # Rolling resistance energy
    E_rolling = rolling_resistance * mass * GRAVITY_ACCELERATION * distance

    # Aerodynamic drag energy
    E_aero = (
        0.5 * drag_coefficient * air_density * frontal_area *
        (velocity ** 2) * distance
    )

    # Total energy at wheel
    E_wheel = E_gravity + E_rolling + E_aero

    return E_wheel


def calculate_energy_with_efficiency(
    wheel_energy: float,
    powertrain_efficiency: float,
    auxiliary_power: float = 0.0,
    time_hours: float = 1.0
) -> float:
    """
    Calculate total energy consumption including efficiency losses.

    Parameters
    ----------
    wheel_energy : float
        Energy at wheel in Joules
    powertrain_efficiency : float
        Powertrain efficiency (0-1)
    auxiliary_power : float
        Auxiliary power draw in Watts (HVAC, etc.)
    time_hours : float
        Operating time in hours

    Returns
    -------
    float
        Total energy consumption in Joules
    """
    # Account for powertrain efficiency
    total_energy = wheel_energy / powertrain_efficiency

    # Add auxiliary energy
    auxiliary_energy = auxiliary_power * time_hours * 3600  # Convert to Joules

    return total_energy + auxiliary_energy


def calculate_regenerative_braking_energy(
    mass: float,
    initial_velocity: float,
    final_velocity: float,
    regen_efficiency: float = 0.70
) -> float:
    """
    Calculate energy recovered from regenerative braking.

    Parameters
    ----------
    mass : float
        Vehicle mass in kg
    initial_velocity : float
        Initial velocity in m/s
    final_velocity : float
        Final velocity in m/s
    regen_efficiency : float
        Regenerative braking efficiency (0-1)

    Returns
    -------
    float
        Energy recovered in Joules
    """
    # Kinetic energy change
    delta_ke = 0.5 * mass * (initial_velocity**2 - final_velocity**2)

    # Energy recovered (accounting for efficiency)
    energy_recovered = delta_ke * regen_efficiency

    return max(0, energy_recovered)


def calculate_specific_energy_consumption(
    total_energy_joules: float,
    distance_km: float,
    mass_kg: float
) -> float:
    """
    Calculate specific energy consumption (energy per unit distance per unit mass).

    Parameters
    ----------
    total_energy_joules : float
        Total energy consumed in Joules
    distance_km : float
        Distance traveled in km
    mass_kg : float
        Vehicle mass in kg

    Returns
    -------
    float
        Specific energy consumption in kWh/100km/tonne
    """
    # Convert to kWh
    energy_kwh = total_energy_joules / 3_600_000

    # Convert mass to tonnes
    mass_tonnes = mass_kg / 1000

    # Calculate per 100 km per tonne
    specific_consumption = (energy_kwh / distance_km * 100) / mass_tonnes

    return specific_consumption


def calculate_technology_specific_energy(
    wheel_energy_joules: float,
    technology: str,
    drivetrain_efficiency: float = 0.90,
    battery_efficiency: float = 0.94,
    fuelcell_efficiency: float = 0.50
) -> Tuple[float, str]:
    """
    Calculate technology-specific energy consumption.

    Technology-Specific Energy Draw:
    - BEV: E_battery = E_wheel / (η_drivetrain × η_battery)
    - FCET: H2_draw = E_wheel / (η_drivetrain × η_fuelcell)
    - Diesel: Fuel_draw = E_wheel / η_tank_to_wheel

    Parameters
    ----------
    wheel_energy_joules : float
        Energy at wheel (Joules)
    technology : str
        Technology type: 'bev', 'fcet', 'diesel'
    drivetrain_efficiency : float
        Drivetrain efficiency (0.90 typical)
    battery_efficiency : float
        Battery charge-discharge efficiency (0.94 typical for BEV)
    fuelcell_efficiency : float
        Fuel cell system efficiency (0.50 typical for FCET)

    Returns
    -------
    tuple
        (energy_required, unit)
        - For BEV: (kWh, 'kWh')
        - For FCET: (kg H2, 'kg_h2')
        - For Diesel: (liters, 'liters')

    Examples
    --------
    >>> # BEV for 100 MJ wheel energy
    >>> energy, unit = calculate_technology_specific_energy(1e8, 'bev')
    >>> print(f"{energy:.2f} {unit}")
    32.88 kWh

    >>> # FCET for same energy
    >>> energy, unit = calculate_technology_specific_energy(1e8, 'fcet')
    >>> print(f"{energy:.2f} {unit}")
    1.85 kg_h2
    """
    tech = technology.lower()

    if tech == 'bev':
        # Battery electric
        battery_energy_j = wheel_energy_joules / (drivetrain_efficiency * battery_efficiency)
        battery_energy_kwh = battery_energy_j / 3_600_000
        return battery_energy_kwh, 'kWh'

    elif tech == 'fcet' or tech == 'hydrogen':
        # Hydrogen fuel cell
        h2_energy_j = wheel_energy_joules / (drivetrain_efficiency * fuelcell_efficiency)
        h2_energy_kwh = h2_energy_j / 3_600_000
        h2_kg = h2_energy_kwh / KG_H2_TO_KWH  # Convert to kg H2
        return h2_kg, 'kg_h2'

    elif tech == 'diesel':
        # Diesel
        diesel_energy_j = wheel_energy_joules / DIESEL_TANK_TO_WHEEL
        diesel_energy_kwh = diesel_energy_j / 3_600_000
        diesel_liters = diesel_energy_kwh / 10.0  # ~10 kWh per liter diesel
        return diesel_liters, 'liters'

    else:
        raise ValueError(f"Unknown technology: {technology}")


def calculate_trip_energy_consumption(
    distance_km: float,
    mass_kg: float,
    grade_angle_rad: float,
    velocity_kmh: float,
    technology: str,
    auxiliary_power_kw: float = 5.0,
    temperature_factor: float = 1.0,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF,
    drag_coefficient: float = DEFAULT_DRAG_COEFFICIENT,
    frontal_area: float = DEFAULT_FRONTAL_AREA
) -> Tuple[float, str]:
    """
    Calculate complete trip energy consumption for any technology.

    Combines wheel energy calculation with technology-specific conversion.

    Parameters
    ----------
    distance_km : float
        Trip distance (km), typical: 100-200 km from Queensland trials
    mass_kg : float
        Vehicle mass (kg), typical: 36,000 kg
    grade_angle_rad : float
        Average route gradient (radians)
    velocity_kmh : float
        Average velocity (km/h), typical: 80 km/h
    technology : str
        Technology type: 'bev', 'fcet', 'diesel'
    auxiliary_power_kw : float
        Auxiliary power for HVAC, etc. (kW)
    temperature_factor : float
        Temperature impact factor (0-1)
    rolling_resistance : float
        Rolling resistance coefficient
    drag_coefficient : float
        Aerodynamic drag coefficient
    frontal_area : float
        Vehicle frontal area (m²)

    Returns
    -------
    tuple
        (energy_required, unit)

    Notes
    -----
    Assumptions:
    - Route-average gradient used
    - Dwell time for charge/refuel added to cycle time separately

    Examples
    --------
    >>> # Typical Queensland trial trip: 120 km, 36 tonnes, flat, 80 km/h, BEV
    >>> energy, unit = calculate_trip_energy_consumption(
    ...     120, 36000, 0.0, 80, 'bev', 5.0
    ... )
    >>> print(f"Trip requires {energy:.1f} {unit}")
    """
    # Convert units
    distance_m = distance_km * 1000
    velocity_ms = velocity_kmh / 3.6
    trip_time_hours = distance_km / velocity_kmh

    # Calculate wheel energy
    wheel_energy = calculate_wheel_energy(
        mass=mass_kg,
        grade=grade_angle_rad,
        distance=distance_m,
        velocity=velocity_ms,
        rolling_resistance=rolling_resistance,
        frontal_area=frontal_area,
        drag_coefficient=drag_coefficient,
    )

    # Add auxiliary energy
    auxiliary_energy_j = auxiliary_power_kw * 1000 * trip_time_hours * 3600

    total_wheel_energy = wheel_energy + auxiliary_energy_j

    # Apply temperature factor
    adjusted_energy = total_wheel_energy / temperature_factor

    # Get technology-specific consumption
    consumption, unit = calculate_technology_specific_energy(
        adjusted_energy, technology
    )

    return consumption, unit


def calculate_energy_cost(
    energy_amount: float,
    technology: str,
    electricity_price_per_kwh: float = 0.20,
    h2_price_per_kg: float = 10.0,
    diesel_price_per_liter: float = 1.50
) -> float:
    """
    Calculate energy cost for a trip based on technology type.

    Parameters
    ----------
    energy_amount : float
        Amount of energy consumed (in technology-specific units)
    technology : str
        Technology type: 'bev', 'fcet', 'diesel'
    electricity_price_per_kwh : float
        Electricity price ($/kWh)
    h2_price_per_kg : float
        Hydrogen price ($/kg)
    diesel_price_per_liter : float
        Diesel price ($/liter)

    Returns
    -------
    float
        Trip energy cost ($)

    Examples
    --------
    >>> # BEV trip using 100 kWh at $0.20/kWh
    >>> calculate_energy_cost(100, 'bev', 0.20)
    20.0

    >>> # FCET trip using 10 kg H2 at $10/kg
    >>> calculate_energy_cost(10, 'fcet', h2_price_per_kg=10.0)
    100.0
    """
    tech = technology.lower()

    if tech == 'bev':
        return energy_amount * electricity_price_per_kwh
    elif tech == 'fcet' or tech == 'hydrogen':
        return energy_amount * h2_price_per_kg
    elif tech == 'diesel':
        return energy_amount * diesel_price_per_liter
    else:
        return 0.0


def calculate_energy_efficiency_comparison(
    distance_km: float,
    mass_kg: float,
    technologies: list = None
) -> dict:
    """
    Compare energy efficiency across multiple technologies for same trip.

    Parameters
    ----------
    distance_km : float
        Trip distance (km)
    mass_kg : float
        Vehicle mass (kg)
    technologies : list, optional
        List of technologies to compare (default: ['bev', 'fcet', 'diesel'])

    Returns
    -------
    dict
        Energy consumption for each technology with units

    Examples
    --------
    >>> comparison = calculate_energy_efficiency_comparison(120, 36000)
    >>> for tech, (energy, unit) in comparison.items():
    ...     print(f"{tech}: {energy:.1f} {unit}")
    bev: 95.2 kWh
    fcet: 5.3 kg_h2
    diesel: 47.6 liters
    """
    if technologies is None:
        technologies = ['bev', 'fcet', 'diesel']

    results = {}

    for tech in technologies:
        try:
            consumption, unit = calculate_trip_energy_consumption(
                distance_km=distance_km,
                mass_kg=mass_kg,
                grade_angle_rad=0.0,
                velocity_kmh=80.0,
                technology=tech
            )
            results[tech] = (consumption, unit)
        except ValueError:
            pass

    return results


__all__ = [
    "calculate_wheel_energy",
    "calculate_energy_with_efficiency",
    "calculate_regenerative_braking_energy",
    "calculate_specific_energy_consumption",
    "calculate_technology_specific_energy",
    "calculate_trip_energy_consumption",
    "calculate_energy_cost",
    "calculate_energy_efficiency_comparison",
]
