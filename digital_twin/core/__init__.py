"""
Core module - Foundation layer with no dependencies.

This module provides the foundational types, models, constants, and validation
for the fleet decarbonization analysis system.
"""

from digital_twin.core.types import (
    VehicleType,
    FuelType,
    TechnologyType,
    OperationalContext,
    TerrainType,
    ChargingType,
    IncentiveType,
)

from digital_twin.core.models import (
    VehicleSpecs,
    OperationalProfile,
    FinancialParams,
    DecarbonizationScenario,
    ROIAnalysis,
    SimulationResult,
)

from digital_twin.core.constants import (
    GRAVITY_ACCELERATION,
    AIR_DENSITY_SEA_LEVEL,
    ROLLING_RESISTANCE_COEFF,
    DEFAULT_DRAG_COEFFICIENT,
    DIESEL_CO2_PER_LITER,
    GRID_ELECTRICITY_CO2_PER_KWH,
    GREEN_H2_CO2_PER_KG,
    DIESEL_TANK_TO_WHEEL,
    BEV_BATTERY_TO_WHEEL,
    FCET_H2_TO_WHEEL,
    BATTERY_DEGRADATION_RATE,
    DEFAULT_DISCOUNT_RATE,
    DEFAULT_ANALYSIS_PERIOD,
)

from digital_twin.core.validation import (
    ValidationError,
    validate_vehicle_specs,
    validate_operational_profile,
    validate_financial_params,
    validate_scenario,
    check_range_feasibility,
)

from digital_twin.core.attributes import (
    VehiclePerformanceParameters,
    OperationalContextParameters,
    EconomicEnvironmentalParameters,
    DegradationDurabilityParameters,
    TechnologyEfficiencyParameters,
    PerformanceMetrics,
    EconomicReturns,
    EnvironmentalImpact,
    ModelInputAttributes,
    ModelOutputAttributes,
    DataIntegrationMetadata,
)

__all__ = [
    # Types
    "VehicleType",
    "FuelType",
    "TechnologyType",
    "OperationalContext",
    "TerrainType",
    "ChargingType",
    "IncentiveType",
    # Models
    "VehicleSpecs",
    "OperationalProfile",
    "FinancialParams",
    "DecarbonizationScenario",
    "ROIAnalysis",
    "SimulationResult",
    # Constants
    "GRAVITY_ACCELERATION",
    "AIR_DENSITY_SEA_LEVEL",
    "ROLLING_RESISTANCE_COEFF",
    "DEFAULT_DRAG_COEFFICIENT",
    "DIESEL_CO2_PER_LITER",
    "GRID_ELECTRICITY_CO2_PER_KWH",
    "GREEN_H2_CO2_PER_KG",
    "DIESEL_TANK_TO_WHEEL",
    "BEV_BATTERY_TO_WHEEL",
    "FCET_H2_TO_WHEEL",
    "BATTERY_DEGRADATION_RATE",
    "DEFAULT_DISCOUNT_RATE",
    "DEFAULT_ANALYSIS_PERIOD",
    # Validation
    "ValidationError",
    "validate_vehicle_specs",
    "validate_operational_profile",
    "validate_financial_params",
    "validate_scenario",
    "check_range_feasibility",
    # Model Attributes - Input
    "VehiclePerformanceParameters",
    "OperationalContextParameters",
    "EconomicEnvironmentalParameters",
    "DegradationDurabilityParameters",
    "TechnologyEfficiencyParameters",
    # Model Attributes - Output
    "PerformanceMetrics",
    "EconomicReturns",
    "EnvironmentalImpact",
    # Model Attributes - Composite
    "ModelInputAttributes",
    "ModelOutputAttributes",
    "DataIntegrationMetadata",
]
