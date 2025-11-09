"""
Fleet Decarbonization Analysis - Digital Twin

A comprehensive Python package for analyzing heavy transport fleet decarbonization
using mathematical models, risk analysis, and optimization.

Architecture:
    Layer 5 (Interface)   → api/, visualization/
    Layer 4 (Integration) → algorithms/
    Layer 3 (Services)    → infrastructure/, optimization/, simulation/, analysis/
    Layer 2 (Domain)      → data/, physics/, economics/, geospatial/
    Layer 1 (Foundation)  → core/, utils/
"""

__version__ = "0.2.0"
__author__ = "Digital Twin Team"
__description__ = "Fleet Decarbonization Analysis - Digital Twin"

# Layer 1: Foundation - Core types and utilities
from digital_twin.core import (
    VehicleType,
    FuelType,
    TechnologyType,
    VehicleSpecs,
    OperationalProfile,
    FinancialParams,
    DecarbonizationScenario,
    ROIAnalysis,
    SimulationResult,
    GRAVITY_ACCELERATION,
    DEFAULT_DISCOUNT_RATE,
)

from digital_twin.utils import (
    format_currency,
    format_percentage,
    km_to_miles,
    kwh_to_joules,
)

# Layer 2: Domain - Physics, Economics, Data, Geospatial
from digital_twin.physics import (
    calculate_wheel_energy,
    calculate_co2_emissions,
    calculate_battery_degradation,
)

from digital_twin.economics import (
    calculate_npv,
    calculate_irr,
    calculate_payback_period,
)

from digital_twin.data import (
    generate_fleet_data,
    create_diesel_baseline,
    create_bev_specs,
    create_fcet_specs,
    create_hybrid_specs,
    create_base_technologies,
    create_base_operational_profile,
    create_base_financial_params,
)

# Layer 3: Services - Infrastructure, Optimization, Simulation, Analysis
from digital_twin.simulation import (
    MonteCarloSimulator,
    create_scenario,
)

from digital_twin.analysis import (
    calculate_utilization,
    compare_technologies,
)

# Layer 4: Integration - Algorithms
from digital_twin.algorithms import (
    run_risk_assessment,
    run_full_analysis,
)

# Layer 5: Interface - Visualization and API
from digital_twin.visualization import (
    create_bar_chart,
    generate_full_report,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__description__",
    # Core types
    "VehicleType",
    "FuelType",
    "TechnologyType",
    "VehicleSpecs",
    "OperationalProfile",
    "FinancialParams",
    "DecarbonizationScenario",
    "ROIAnalysis",
    "SimulationResult",
    # Constants
    "GRAVITY_ACCELERATION",
    "DEFAULT_DISCOUNT_RATE",
    # Utilities
    "format_currency",
    "format_percentage",
    "km_to_miles",
    "kwh_to_joules",
    # Physics
    "calculate_wheel_energy",
    "calculate_co2_emissions",
    "calculate_battery_degradation",
    # Economics
    "calculate_npv",
    "calculate_irr",
    "calculate_payback_period",
    # Data
    "generate_fleet_data",
    "create_diesel_baseline",
    "create_bev_specs",
    "create_fcet_specs",
    "create_hybrid_specs",
    "create_base_technologies",
    "create_base_operational_profile",
    "create_base_financial_params",
    # Simulation
    "MonteCarloSimulator",
    "create_scenario",
    # Analysis
    "calculate_utilization",
    "compare_technologies",
    # Algorithms
    "run_risk_assessment",
    "run_full_analysis",
    # Visualization
    "create_bar_chart",
    "generate_full_report",
]
