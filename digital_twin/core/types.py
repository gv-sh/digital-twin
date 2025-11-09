"""
Core type definitions for fleet decarbonization analysis.

This module defines the fundamental types, enumerations, and type aliases
used throughout the fleet decarbonization system.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from enum import Enum
from datetime import datetime, date

# Enumerations
class VehicleType(Enum):
    HEAVY_TRUCK = "heavy_truck"  # Generic heavy truck category
    HEAVY_RIGID = "heavy_rigid"
    ARTICULATED = "articulated"
    B_DOUBLE = "b_double"
    ROAD_TRAIN = "road_train"

class FuelType(Enum):
    DIESEL = "diesel"
    ELECTRIC = "electric"  # Alias for backward compatibility
    ELECTRIC_BEV = "electric_bev"
    HYDROGEN = "hydrogen"  # Alias for backward compatibility
    HYDROGEN_FCEV = "hydrogen_fcev"
    BIODIESEL = "biodiesel"
    CNG = "cng"
    LNG = "lng"

class OperationalContext(Enum):
    URBAN = "urban"
    REGIONAL = "regional"
    LONG_HAUL = "long_haul"
    MINING = "mining"
    MIXED = "mixed"

class TechnologyType(Enum):
    DIESEL = "diesel"
    BEV = "bev"
    FCEV = "fcev"
    HYBRID = "hybrid"
    PHEV = "phev"
    BIODIESEL = "biodiesel"
    CNG = "cng"
    LNG = "lng"

class TerrainType(Enum):
    FLAT = "flat"
    ROLLING = "rolling"
    HILLY = "hilly"
    MOUNTAINOUS = "mountainous"

class ChargingType(Enum):
    DEPOT = "depot"
    OPPORTUNITY = "opportunity"
    EN_ROUTE = "en_route"
    PUBLIC = "public"

class InfrastructureType(Enum):
    FAST_CHARGER = "fast_charger"
    SLOW_CHARGER = "slow_charger"
    HYDROGEN_STATION = "hydrogen_station"
    CNG_STATION = "cng_station"
    LNG_STATION = "lng_station"
    BIODIESEL_DEPOT = "biodiesel_depot"

class MaintenanceType(Enum):
    SCHEDULED = "scheduled"
    UNSCHEDULED = "unscheduled"
    BREAKDOWN = "breakdown"
    PREVENTIVE = "preventive"

class IncentiveType(Enum):
    GRANT = "grant"
    REBATE = "rebate"
    TAX_CREDIT = "tax_credit"
    SUBSIDY = "subsidy"
    LOAN = "loan"

class TariffType(Enum):
    FLAT = "flat"
    TIME_OF_USE = "time_of_use"
    DEMAND = "demand"

class DepreciationMethod(Enum):
    STRAIGHT_LINE = "straight_line"
    DIMINISHING_VALUE = "diminishing_value"
    UNITS_OF_PRODUCTION = "units_of_production"

class AustralianState(Enum):
    NSW = "NSW"
    VIC = "VIC"
    QLD = "QLD"
    SA = "SA"
    WA = "WA"
    TAS = "TAS"
    NT = "NT"
    ACT = "ACT"

class RegionType(Enum):
    URBAN = "urban"
    REGIONAL = "regional"
    REMOTE = "remote"

# Time-series and temporal helpers
@dataclass
class TimeSeries:
    timestamps: List[datetime]
    values: List[float]
    unit: str
    label: str

@dataclass
class TimeRange:
    start_date: date
    end_date: date

    def duration_years(self) -> float:
        return (self.end_date - self.start_date).days / 365.25

    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

# Geographic helpers
@dataclass
class Location:
    location_id: str
    name: str
    latitude: float
    longitude: float
    state: AustralianState
    region_type: RegionType
    elevation: Optional[float] = None  # meters above sea level

@dataclass
class Route:
    route_id: str
    origin: Location
    destination: Location
    distance: float  # km
    average_gradient: float  # %
    road_quality_index: float  # 0-1
    charging_stations_available: List[str]
    typical_traffic_conditions: str

# Climate and environmental
@dataclass
class ClimateConditions:
    location_id: str
    average_temperature: float  # °C
    temperature_range: Tuple[float, float]  # (min, max)
    humidity_average: float  # %
    altitude: float  # m above sea level
    extreme_weather_days: int  # days per year

# Conversion factors
@dataclass
class EnergyConversionFactors:
    diesel_to_kwh: float = 10.0  # kWh/L
    lng_to_kwh: float = 6.7  # kWh/L
    cng_energy_density: float = 9.0  # kWh/m³
    hydrogen_energy_density: float = 33.3  # kWh/kg
    biodiesel_to_kwh: float = 9.8  # kWh/L

@dataclass
class EmissionFactors:
    fuel_type: FuelType
    co2_per_unit: float  # kg CO2e per L, kWh, or kg
    ch4_per_unit: float  # kg CH4
    n2o_per_unit: float  # kg N2O
    scope: int  # 1, 2, or 3
    source: str  # e.g., "NGER 2024"
    last_updated: date

# Financial helpers
@dataclass
class CashFlow:
    year: int
    capital_expenditure: float
    operational_expenditure: float
    revenue: float
    tax: float
    depreciation: float
    net_cash_flow: float

@dataclass
class DepreciationSchedule:
    asset_id: str
    method: DepreciationMethod
    initial_value: float
    residual_value: float
    useful_life: int  # years
    annual_depreciation: List[float]

    def total_depreciation(self) -> float:
        return sum(self.annual_depreciation)

@dataclass
class IncentiveProgram:
    program_id: str
    name: str
    jurisdiction: str  # Federal, NSW, VIC, etc.
    incentive_type: IncentiveType
    amount: float  # AUD or percentage
    eligibility_criteria: Dict[str, any]
    start_date: date
    end_date: Optional[date]
    application_url: Optional[str]
    maximum_per_vehicle: Optional[float]

# Operational helpers
@dataclass
class LoadProfile:
    profile_id: str
    time_of_day: str  # e.g., "06:00-09:00"
    day_of_week: int  # 1-7 (Monday=1)
    load_factor: float  # % of max payload (0-1)
    frequency: int  # trips per period

@dataclass
class DutyCycle:
    cycle_id: str
    cycle_name: str
    segments: List[Dict[str, float]]  # [{"speed": 60, "duration": 2.5, "load": 0.8}, ...]
    total_distance: float  # km
    total_time: float  # hours
    energy_demand: float  # kWh or L

# Energy tariffs
@dataclass
class EnergyTariff:
    tariff_id: str
    provider: str
    tariff_type: TariffType
    peak_rate: float  # AUD/kWh
    off_peak_rate: Optional[float]
    shoulder_rate: Optional[float]
    demand_charge: Optional[float]  # AUD/kW
    peak_hours: Optional[List[Tuple[int, int]]]  # [(start_hour, end_hour), ...]
    supply_charge: float  # AUD/day

@dataclass
class ChargingSession:
    session_id: str
    vehicle_id: str
    start_time: datetime
    end_time: datetime
    energy_delivered: float  # kWh or kg H2
    cost: float  # AUD
    state_of_charge_initial: float  # %
    state_of_charge_final: float  # %
    location_id: str

# Performance tracking
@dataclass
class PerformanceIndicator:
    indicator_name: str
    target_value: float
    actual_value: float
    unit: str
    measurement_period: TimeRange
    variance: float

    def is_meeting_target(self) -> bool:
        return self.actual_value >= self.target_value

    def percentage_of_target(self) -> float:
        return (self.actual_value / self.target_value) * 100 if self.target_value != 0 else 0

@dataclass
class MaintenanceEvent:
    event_id: str
    vehicle_id: str
    event_date: date
    event_type: MaintenanceType
    description: str
    cost: float
    downtime_hours: float
    parts_replaced: List[str]
    odometer_reading: float  # km

@dataclass
class ReliabilityMetrics:
    vehicle_id: str
    mean_time_between_failures: float  # hours
    mean_time_to_repair: float  # hours
    availability: float  # %
    failure_rate: float  # failures per 100,000 km
    measurement_period: TimeRange

# Validation and constraints
@dataclass
class OperationalConstraints:
    constraint_id: str
    min_range_required: float  # km
    max_refuel_time: float  # minutes
    min_payload_capacity: float  # kg
    max_vehicle_weight: float  # kg (road limits)
    temperature_operating_range: Tuple[float, float]  # °C
    gradient_capability: float  # max % grade
    required_certifications: List[str]

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    passed_checks: List[str]
    timestamp: datetime = datetime.now()

# Sensitivity analysis
@dataclass
class SensitivityParameter:
    parameter_name: str
    base_value: float
    variation_range: Tuple[float, float]  # (min, max)
    step_size: float
    unit: str

@dataclass
class SensitivityResult:
    scenario_id: str
    parameter_varied: str
    parameter_values: List[float]
    npv_outcomes: List[float]
    payback_outcomes: List[float]
    emissions_outcomes: List[float]
    elasticity: float  # % change in output per % change in input

# Benchmarking
@dataclass
class BenchmarkData:
    benchmark_id: str
    category: str  # industry_average, best_in_class, worst_case, etc.
    vehicle_type: VehicleType
    fuel_type: FuelType
    metric_name: str
    metric_value: float
    source: str
    date_collected: date
    sample_size: Optional[int]

@dataclass
class ComparativeAnalysis:
    comparison_id: str
    scenario_a_id: str
    scenario_b_id: str
    comparison_metrics: Dict[str, Tuple[float, float]]  # metric: (value_a, value_b)
    percentage_differences: Dict[str, float]
    winner: Optional[str]  # scenario_id
    confidence_level: float  # 0-1

# Aggregation helpers
@dataclass
class FleetSummary:
    fleet_id: str
    reporting_period: TimeRange
    total_distance_traveled: float  # km
    total_fuel_consumed: float
    total_emissions: float  # tCO2e
    total_operating_cost: float  # AUD
    average_efficiency: float
    utilization_rate: float  # %
    vehicles_count: int

@dataclass
class MonthlyReport:
    report_id: str
    month: date
    vehicles_active: int
    total_distance: float
    fuel_cost: float
    maintenance_cost: float
    downtime_hours: float
    emissions_total: float
    incidents: int
    availability: float  # %

__all__ = [
    # Enumerations
    "VehicleType",
    "FuelType",
    "OperationalContext",
    "TechnologyType",
    "TerrainType",
    "ChargingType",
    "InfrastructureType",
    "MaintenanceType",
    "IncentiveType",
    "TariffType",
    "DepreciationMethod",
    "AustralianState",
    "RegionType",
    # Time-series and temporal
    "TimeSeries",
    "TimeRange",
    # Geographic
    "Location",
    "Route",
    # Climate and environmental
    "ClimateConditions",
    # Conversion factors
    "EnergyConversionFactors",
    "EmissionFactors",
    # Financial
    "CashFlow",
    "DepreciationSchedule",
    "IncentiveProgram",
    # Operational
    "LoadProfile",
    "DutyCycle",
    # Energy
    "EnergyTariff",
    "ChargingSession",
    # Performance tracking
    "PerformanceIndicator",
    "MaintenanceEvent",
    "ReliabilityMetrics",
    # Validation and constraints
    "OperationalConstraints",
    "ValidationResult",
    # Sensitivity analysis
    "SensitivityParameter",
    "SensitivityResult",
    # Benchmarking
    "BenchmarkData",
    "ComparativeAnalysis",
    # Aggregation
    "FleetSummary",
    "MonthlyReport",
]
