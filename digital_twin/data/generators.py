"""Synthetic data generation based on Queensland trial parameters."""

from digital_twin.core.models import VehicleSpecs, OperationalProfile, FinancialParams
from digital_twin.core.types import VehicleType, FuelType, TechnologyType


def generate_fleet_data(num_vehicles: int = 50) -> list:
    """Generate synthetic fleet data."""
    return [{"vehicle_id": i, "type": "heavy_truck"} for i in range(num_vehicles)]


def create_diesel_baseline() -> VehicleSpecs:
    """Create diesel baseline vehicle specs."""
    return VehicleSpecs(
        name="Diesel Baseline",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.DIESEL,
        technology_type=TechnologyType.DIESEL,
        mass_kg=18000,
        initial_cost=150000,
        annual_operating_cost=85000,
        energy_efficiency=0.35,
        co2_emission_factor=2.68,
        max_range_km=1200,
    )


def create_bev_specs() -> VehicleSpecs:
    """Create BEV vehicle specs."""
    return VehicleSpecs(
        name="Battery Electric",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.ELECTRIC,
        technology_type=TechnologyType.BEV,
        mass_kg=20000,
        initial_cost=300000,
        annual_operating_cost=51000,
        energy_efficiency=0.85,
        co2_emission_factor=0.75,
        max_range_km=400,
        battery_degradation_rate=0.106,
        charging_power_kw=150,
    )


__all__ = ["generate_fleet_data", "create_diesel_baseline", "create_bev_specs"]
