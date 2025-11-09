"""
Core data models for fleet decarbonization analysis.

This module defines the fundamental data structures used throughout
the analysis, including vehicle specifications, scenarios, and results.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from digital_twin.core.types import (
    VehicleType,
    FuelType,
    TechnologyType,
    OperationalContext,
    TerrainType,
)


@dataclass
class VehicleSpecs:
    """Vehicle specifications and characteristics."""

    name: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    technology_type: TechnologyType

    # Physical characteristics
    mass_kg: float
    frontal_area_m2: float = 8.0
    drag_coefficient: float = 1.0
    rolling_resistance: float = 0.006

    # Performance
    max_range_km: float = 400.0
    max_payload_kg: float = 18000.0
    max_speed_kmh: float = 100.0

    # Energy/Fuel
    energy_efficiency: float = 0.85  # Tank/battery-to-wheel
    fuel_capacity: float = 0.0  # Liters or kWh

    # Economic
    initial_cost: float = 0.0
    annual_operating_cost: float = 0.0
    residual_value_factor: float = 0.20  # % of initial cost after analysis period

    # Environmental
    co2_emission_factor: float = 0.0  # kg CO2 per unit fuel/energy
    nox_emission_factor: float = 0.0  # g NOx per km
    pm_emission_factor: float = 0.0  # g PM per km

    # Technology-specific
    battery_degradation_rate: Optional[float] = None  # For BEV
    charging_power_kw: Optional[float] = None  # For BEV
    h2_tank_pressure_bar: Optional[float] = None  # For FCET

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationalProfile:
    """Operational profile for vehicle usage."""

    annual_km: float = 100000.0
    operating_days_per_year: int = 250
    daily_km: float = 400.0

    # Operational characteristics
    context: OperationalContext = OperationalContext.MIXED
    terrain: TerrainType = TerrainType.ROLLING
    average_velocity_kmh: float = 80.0
    average_grade_radians: float = 0.0

    # Utilization
    utilization_rate: float = 0.85  # % of max capacity used
    load_factor: float = 0.75  # % of max payload carried

    # Environmental
    ambient_temp_celsius: float = 25.0
    altitude_m: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FinancialParams:
    """Financial parameters for economic analysis."""

    discount_rate: float = 0.08
    analysis_period_years: int = 5

    # Price escalation
    fuel_price_escalation: float = 0.03
    electricity_price_escalation: float = 0.02
    h2_price_escalation: float = 0.01
    maintenance_cost_escalation: float = 0.025

    # Costs
    fuel_price_per_unit: float = 1.50  # AUD per liter
    electricity_price_per_kwh: float = 0.25
    h2_price_per_kg: float = 8.00

    # Incentives
    capital_grant: float = 0.0
    annual_subsidy: float = 0.0
    tax_benefits: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecarbonizationScenario:
    """Complete scenario for decarbonization analysis."""

    name: str
    description: str = ""

    vehicle_specs: VehicleSpecs = field(default_factory=lambda: VehicleSpecs(
        name="Default",
        vehicle_type=VehicleType.HEAVY_TRUCK,
        fuel_type=FuelType.DIESEL,
        technology_type=TechnologyType.DIESEL,
        mass_kg=18000.0
    ))

    operational_profile: OperationalProfile = field(default_factory=OperationalProfile)
    financial_params: FinancialParams = field(default_factory=FinancialParams)

    # Comparison baseline
    baseline_technology: Optional[TechnologyType] = TechnologyType.DIESEL

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ROIAnalysis:
    """Results of return on investment analysis."""

    technology_name: str

    # Financial metrics
    npv: float = 0.0
    irr: float = 0.0  # Internal Rate of Return
    payback_period_years: float = 0.0
    total_cost_of_ownership: float = 0.0

    # Cash flows
    initial_investment: float = 0.0
    annual_cashflows: List[float] = field(default_factory=list)
    cumulative_cashflows: List[float] = field(default_factory=list)

    # Savings vs baseline
    annual_savings: List[float] = field(default_factory=list)
    total_savings: float = 0.0

    # Environmental
    annual_co2_reduction_kg: float = 0.0
    total_co2_reduction_kg: float = 0.0
    co2_reduction_percentage: float = 0.0

    # Risk metrics
    success_probability: float = 0.0  # From Monte Carlo
    var_95: float = 0.0  # Value at Risk (95%)
    sharpe_ratio: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationResult:
    """Results from Monte Carlo simulation."""

    scenario_name: str
    n_simulations: int

    # NPV distribution
    npv_mean: float = 0.0
    npv_std: float = 0.0
    npv_median: float = 0.0
    npv_p05: float = 0.0  # 5th percentile
    npv_p95: float = 0.0  # 95th percentile

    # Success metrics
    probability_positive_npv: float = 0.0
    expected_value: float = 0.0

    # Sensitivity
    sensitivity_factors: Dict[str, float] = field(default_factory=dict)

    # Raw data
    npv_values: List[float] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


__all__ = [
    "VehicleSpecs",
    "OperationalProfile",
    "FinancialParams",
    "DecarbonizationScenario",
    "ROIAnalysis",
    "SimulationResult",
]
