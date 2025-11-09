"""
Core data models for fleet decarbonization analysis.

This module defines the fundamental data structures used throughout
the analysis, including vehicle specifications, scenarios, and results.

MODEL VERSIONING NOTES:
-----------------------
This module contains both V1 (simple) and V2 (comprehensive) model versions:

- V1 Models: VehicleSpecs, OperationalProfile, FinancialParams, etc.
  - Recommended for most use cases
  - Simpler structure with essential parameters
  - Fully integrated with the codebase
  - Used in all examples and notebooks

- V2 Models: VehicleSpecsV2, OperationalProfileV2, FinancialParamsV2, etc.
  - Advanced/experimental models with extended attributes
  - Designed for detailed fleet management scenarios
  - More comprehensive but may require additional implementation
  - Currently in experimental stage

RECOMMENDATION: Use V1 models unless you need the additional complexity
and attributes provided by V2 models. V2 models are provided for future
extensibility but are not required for standard decarbonization analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from digital_twin.core.types import (
    VehicleType,
    FuelType,
    TechnologyType,
    OperationalContext,
    TerrainType,
    InfrastructureType,
    Location,
    Route,
    EnergyTariff,
    IncentiveProgram,
    EmissionFactors,
    CashFlow,
    MaintenanceEvent,
    OperationalConstraints,
    SensitivityParameter,
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


# Enhanced data models for comprehensive fleet decarbonization analysis

@dataclass
class VehicleSpecsV2:
    """Enhanced vehicle specifications with detailed attributes."""
    vehicle_id: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    gross_vehicle_mass: float  # kg
    tare_weight: float  # kg
    payload_capacity: float  # kg
    fuel_tank_capacity: float  # L or kWh
    purchase_cost: float  # AUD
    expected_lifetime: int  # years
    manufacturer: str
    model: str
    year: int
    battery_warranty_years: Optional[int] = None
    battery_warranty_km: Optional[float] = None


@dataclass
class OperationalProfileV2:
    """Enhanced operational parameters for vehicle usage."""
    profile_id: str
    operational_context: OperationalContext
    annual_distance: float  # km
    average_payload: float  # kg
    duty_cycle_pattern: str
    average_speed: float  # km/h
    idle_time_percentage: float
    terrain_factor: float  # 1.0 = flat, >1.0 = hilly
    routes: List[Route]
    shift_pattern: str  # e.g., "2-shift", "24/7"


@dataclass
class EnergyConsumption:
    """Energy consumption profile for a vehicle."""
    vehicle_id: str
    fuel_type: FuelType
    consumption_rate: float  # L/100km or kWh/100km or kg-H2/100km
    consumption_loaded: float
    consumption_empty: float
    temperature_coefficient: float  # adjustment per °C
    gradient_coefficient: float  # adjustment per % grade
    auxiliary_load: float  # kW for HVAC, etc.
    regenerative_braking_efficiency: Optional[float] = None  # for BEV


@dataclass
class InfrastructureSpec:
    """Infrastructure requirements and specifications."""
    infrastructure_id: str
    fuel_type: FuelType
    infrastructure_type: InfrastructureType
    capacity: float  # kW or kg/day
    installation_cost: float  # AUD
    annual_maintenance_cost: float  # AUD
    footprint: float  # m²
    grid_connection_required: bool
    grid_connection_cost: Optional[float]  # AUD
    renewable_integration: bool
    number_of_units: int
    location: Location


@dataclass
class FinancialParamsV2:
    """Enhanced financial parameters for economic analysis."""
    discount_rate: float  # % (e.g., WACC)
    analysis_period: int  # years
    fuel_price: float  # AUD/L or AUD/kWh or AUD/kg
    fuel_price_escalation: float  # % per year
    electricity_tariff: Optional[EnergyTariff]
    carbon_price: Optional[float]  # AUD/tCO2e
    government_incentives: List[IncentiveProgram]
    residual_value_factor: float  # % of purchase cost
    tax_rate: float  # %
    inflation_rate: float  # %


@dataclass
class EmissionsProfile:
    """Emissions profile for a vehicle or fuel type."""
    fuel_type: FuelType
    tailpipe_emissions: float  # gCO2e/km (Scope 1)
    upstream_emissions: float  # gCO2e/km (well-to-tank, Scope 3)
    total_lifecycle_emissions: float  # gCO2e/km
    grid_emissions_factor: Optional[float]  # kgCO2e/kWh (for electric)
    renewable_percentage: Optional[float]  # % (for electric)
    emission_factors: EmissionFactors


@dataclass
class MaintenanceSchedule:
    """Maintenance schedule and costs for a vehicle."""
    vehicle_id: str
    fuel_type: FuelType
    routine_maintenance_cost: float  # AUD/km
    major_service_interval: int  # km
    major_service_cost: float  # AUD
    component_replacement_costs: Dict[str, float]  # component: cost
    component_replacement_intervals: Dict[str, int]  # component: km
    downtime_hours_per_year: float
    maintenance_events_history: List[MaintenanceEvent]


@dataclass
class PerformanceMetrics:
    """Performance metrics for a vehicle."""
    vehicle_id: str
    range: float  # km
    refueling_time: float  # minutes
    availability: float  # %
    reliability_score: float  # 0-1
    power_output: float  # kW
    torque: float  # Nm
    acceleration_0_80: float  # seconds
    max_speed: float  # km/h
    gradeability: float  # % at full load


@dataclass
class ROIAnalysisV2:
    """Enhanced ROI analysis with comprehensive metrics."""
    scenario_id: str
    vehicle_id: str
    npv: float  # AUD (Net Present Value)
    irr: float  # % (Internal Rate of Return)
    payback_period: float  # years
    discounted_payback_period: float  # years
    total_cost_of_ownership: float  # AUD
    annual_operating_cost: float  # AUD/year
    cost_per_km: float  # AUD/km
    cumulative_emissions_saved: float  # tCO2e
    cost_per_tonne_co2_avoided: float  # AUD/tCO2e
    cash_flows: List[CashFlow]
    break_even_year: Optional[int]


@dataclass
class DecarbonizationScenarioV2:
    """Enhanced scenario for decarbonization analysis."""
    scenario_id: str
    scenario_name: str
    scenario_description: str
    baseline_vehicle: VehicleSpecsV2
    alternative_vehicle: VehicleSpecsV2
    operational_profile: OperationalProfileV2
    infrastructure_required: List[InfrastructureSpec]
    financial_params: FinancialParamsV2
    emissions_baseline: EmissionsProfile
    emissions_alternative: EmissionsProfile
    analysis_start_date: date
    sensitivity_parameters: List[SensitivityParameter]
    constraints: OperationalConstraints
    assumptions: Dict[str, str]


@dataclass
class FleetComposition:
    """Fleet composition and characteristics."""
    fleet_id: str
    operator_name: str
    operator_abn: Optional[str]
    total_vehicles: int
    vehicle_breakdown: Dict[VehicleType, int]
    fuel_breakdown: Dict[FuelType, int]
    total_annual_distance: float  # km
    average_vehicle_age: float  # years
    depot_locations: List[Location]
    operational_contexts: List[OperationalContext]


@dataclass
class RiskAssessment:
    """Risk assessment for a decarbonization scenario."""
    scenario_id: str
    technology_risk: float  # 0-1 score
    supply_chain_risk: float
    regulatory_risk: float
    market_risk: float
    infrastructure_risk: float
    financial_risk: float
    operational_risk: float
    overall_risk_score: float
    mitigation_strategies: List[str]
    contingency_plans: Dict[str, str]
    risk_register: List[Dict[str, Any]]


@dataclass
class TransitionPlan:
    """Transition plan for fleet decarbonization."""
    plan_id: str
    fleet_id: str
    start_date: date
    completion_date: date
    phases: List[Dict[str, Any]]  # List of transition phases
    vehicles_to_replace: List[str]  # vehicle_ids
    replacement_schedule: Dict[int, List[str]]  # year: [vehicle_ids]
    infrastructure_deployment: Dict[int, List[str]]  # year: [infrastructure_ids]
    total_investment: float  # AUD
    funding_sources: List[str]
    key_milestones: List[Dict[str, Any]]
    success_criteria: List[str]


@dataclass
class DecisionMatrix:
    """Decision support matrix for scenario evaluation."""
    matrix_id: str
    scenarios_evaluated: List[str]  # scenario_ids
    criteria: List[str]  # evaluation criteria
    weights: Dict[str, float]  # criterion: weight
    scores: Dict[str, Dict[str, float]]  # scenario_id: {criterion: score}
    weighted_scores: Dict[str, float]  # scenario_id: total_weighted_score
    ranking: List[str]  # scenario_ids in order of preference
    recommended_scenario: str
    confidence: float  # 0-1
    notes: str


__all__ = [
    # Original models
    "VehicleSpecs",
    "OperationalProfile",
    "FinancialParams",
    "DecarbonizationScenario",
    "ROIAnalysis",
    "SimulationResult",
    # Enhanced models (V2)
    "VehicleSpecsV2",
    "OperationalProfileV2",
    "EnergyConsumption",
    "InfrastructureSpec",
    "FinancialParamsV2",
    "EmissionsProfile",
    "MaintenanceSchedule",
    "PerformanceMetrics",
    "ROIAnalysisV2",
    "DecarbonizationScenarioV2",
    "FleetComposition",
    "RiskAssessment",
    "TransitionPlan",
    "DecisionMatrix",
]
