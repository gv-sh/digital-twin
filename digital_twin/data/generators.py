"""
Synthetic data generation based on Queensland trial parameters.

This module provides functions to create realistic vehicle specifications
and fleet data for decarbonization analysis.
"""

from typing import List, Dict, Any
from digital_twin.core.models import VehicleSpecs, OperationalProfile, FinancialParams
from digital_twin.core.types import VehicleType, FuelType, TechnologyType


def generate_fleet_data(
    num_vehicles: int = 50,
    vehicle_type: VehicleType = VehicleType.HEAVY_TRUCK
) -> List[Dict[str, Any]]:
    """
    Generate synthetic fleet data.

    Parameters
    ----------
    num_vehicles : int
        Number of vehicles to generate
    vehicle_type : VehicleType
        Type of vehicles in the fleet

    Returns
    -------
    list
        List of vehicle dictionaries with basic attributes
    """
    return [
        {
            "vehicle_id": f"VEH-{i:04d}",
            "type": vehicle_type.value,
            "status": "active",
            "year_purchased": 2020 + (i % 5)
        }
        for i in range(num_vehicles)
    ]


def create_diesel_baseline() -> VehicleSpecs:
    """
    Create diesel baseline vehicle specs.

    Returns
    -------
    VehicleSpecs
        Diesel truck specifications based on typical heavy vehicle parameters
    """
    return VehicleSpecs(
        name="Diesel Baseline",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.DIESEL,
        technology_type=TechnologyType.DIESEL,
        mass_kg=18000,
        frontal_area_m2=8.0,
        drag_coefficient=1.0,
        rolling_resistance=0.006,
        max_range_km=1200,
        max_payload_kg=18000,
        max_speed_kmh=100,
        energy_efficiency=0.35,
        fuel_capacity=400,  # liters
        initial_cost=150000,
        annual_operating_cost=85000,
        residual_value_factor=0.20,
        co2_emission_factor=2.68,  # kg CO2 per liter diesel
        nox_emission_factor=8.5,  # g NOx per km
        pm_emission_factor=0.15,  # g PM per km
    )


def create_bev_specs() -> VehicleSpecs:
    """
    Create BEV (Battery Electric Vehicle) specs.

    Based on Queensland trial data:
    - 300 km full charge capacity
    - 15% battery degradation over 1.5 years
    - 2-5 hour charging times

    Returns
    -------
    VehicleSpecs
        BEV specifications
    """
    return VehicleSpecs(
        name="Battery Electric Vehicle",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.ELECTRIC,
        technology_type=TechnologyType.BEV,
        mass_kg=20000,  # Heavier due to battery
        frontal_area_m2=8.0,
        drag_coefficient=0.9,  # Slightly better aerodynamics
        rolling_resistance=0.005,  # Slightly lower
        max_range_km=400,
        max_payload_kg=16000,  # Reduced due to battery weight
        max_speed_kmh=100,
        energy_efficiency=0.85,
        fuel_capacity=500,  # kWh battery capacity
        initial_cost=300000,  # 2x diesel cost
        annual_operating_cost=51000,  # 40% lower than diesel
        residual_value_factor=0.25,
        co2_emission_factor=0.75,  # Grid emissions for electricity
        nox_emission_factor=0.0,  # Zero tailpipe emissions
        pm_emission_factor=0.0,  # Zero tailpipe emissions
        battery_degradation_rate=0.106,  # 15% over 1.5 years
        charging_power_kw=150,  # DC fast charging
    )


def create_fcet_specs() -> VehicleSpecs:
    """
    Create FCET (Fuel Cell Electric Truck) specs.

    Returns
    -------
    VehicleSpecs
        FCET specifications with hydrogen fuel cell system
    """
    return VehicleSpecs(
        name="Fuel Cell Electric Truck",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.HYDROGEN,
        technology_type=TechnologyType.FCEV,
        mass_kg=19000,  # Lighter than BEV
        frontal_area_m2=8.0,
        drag_coefficient=0.95,
        rolling_resistance=0.0055,
        max_range_km=600,  # Better range than BEV
        max_payload_kg=17000,
        max_speed_kmh=100,
        energy_efficiency=0.50,  # Fuel cell efficiency
        fuel_capacity=50,  # kg H2 at 700 bar
        initial_cost=450000,  # 3x diesel cost
        annual_operating_cost=80000,  # Similar to diesel due to H2 costs
        residual_value_factor=0.20,
        co2_emission_factor=1.5,  # Depends on H2 source (grey vs green)
        nox_emission_factor=0.0,  # Zero tailpipe emissions
        pm_emission_factor=0.0,  # Zero tailpipe emissions
        h2_tank_pressure_bar=700,
    )


def create_hybrid_specs() -> VehicleSpecs:
    """
    Create Hybrid (Diesel-Electric) truck specs.

    Returns
    -------
    VehicleSpecs
        Hybrid truck specifications
    """
    return VehicleSpecs(
        name="Diesel-Electric Hybrid",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.DIESEL,  # Primary fuel
        technology_type=TechnologyType.HYBRID,
        mass_kg=19500,
        frontal_area_m2=8.0,
        drag_coefficient=0.95,
        rolling_resistance=0.0055,
        max_range_km=800,
        max_payload_kg=16500,
        max_speed_kmh=100,
        energy_efficiency=0.45,  # Better than pure diesel
        fuel_capacity=300,  # liters diesel + small battery
        initial_cost=250000,  # Between diesel and BEV
        annual_operating_cost=68000,  # 20% lower than diesel
        residual_value_factor=0.22,
        co2_emission_factor=1.60,  # 40% reduction vs diesel
        nox_emission_factor=5.0,  # Lower than diesel
        pm_emission_factor=0.08,  # Lower than diesel
    )


def create_base_technologies() -> Dict[str, VehicleSpecs]:
    """
    Create all base technology specifications.

    Returns
    -------
    dict
        Dictionary mapping technology names to VehicleSpecs
    """
    return {
        "Diesel": create_diesel_baseline(),
        "BEV": create_bev_specs(),
        "FCET": create_fcet_specs(),
        "Hybrid": create_hybrid_specs(),
    }


def create_base_operational_profile() -> OperationalProfile:
    """
    Create default operational profile based on Queensland trials.

    Returns
    -------
    OperationalProfile
        Typical heavy truck operational profile
    """
    return OperationalProfile(
        annual_km=100000.0,
        operating_days_per_year=250,
        daily_km=400.0,
        average_velocity_kmh=80.0,
        average_grade_radians=0.0,
        utilization_rate=0.85,
        load_factor=0.75,
        ambient_temp_celsius=25.0,
        altitude_m=0.0,
    )


def create_base_financial_params() -> FinancialParams:
    """
    Create default financial parameters for analysis.

    Returns
    -------
    FinancialParams
        Standard financial parameters for Australian context
    """
    return FinancialParams(
        discount_rate=0.08,
        analysis_period_years=5,
        fuel_price_escalation=0.03,
        electricity_price_escalation=0.02,
        h2_price_escalation=0.01,
        maintenance_cost_escalation=0.025,
        fuel_price_per_unit=1.50,  # AUD per liter diesel
        electricity_price_per_kwh=0.25,  # AUD per kWh
        h2_price_per_kg=8.00,  # AUD per kg H2
        capital_grant=0.0,
        annual_subsidy=0.0,
        tax_benefits=0.0,
    )


__all__ = [
    "generate_fleet_data",
    "create_diesel_baseline",
    "create_bev_specs",
    "create_fcet_specs",
    "create_hybrid_specs",
    "create_base_technologies",
    "create_base_operational_profile",
    "create_base_financial_params",
]
