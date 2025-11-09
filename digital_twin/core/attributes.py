"""
Model attributes for fleet decarbonization mathematical modeling framework.

This module defines comprehensive input and output attributes for the mathematical
modeling framework, supporting performance prediction, economic analysis, and
environmental impact assessment.

References:
- Initial Analysis: Core challenge of quantifying performance trade-offs
- Proposed Algorithms: Algorithm parameter definitions
- Model Equations: Mathematical calculation support
- Queensland Trial Data: Real-world validation benchmarks
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum
from digital_twin.core.types import FuelType, TechnologyType


# ============================================================================
# INPUT ATTRIBUTES
# ============================================================================


@dataclass
class VehiclePerformanceParameters:
    """
    Core specifications required for performance prediction and energy consumption modeling.

    These parameters form the foundation of energy consumption calculations
    and performance predictions across different operational scenarios.
    """

    # Physical specifications
    vehicle_mass_gross: float  # kg - Includes payload when loaded
    battery_capacity: Optional[float] = None  # kWh - BEV only, affects range calculation
    hydrogen_storage: Optional[float] = None  # kg H2 - FCET only, determines refueling frequency
    rolling_resistance_coefficient: float = 0.006  # dimensionless - Heavy truck typical
    drag_area_coefficient: float = 8.0  # m² - Typical tractor-trailer

    # Default values based on industry standards
    default_vehicle_mass: float = 36000.0  # kg
    default_battery_capacity: float = 500.0  # kWh
    default_hydrogen_storage: float = 30.0  # kg H2

    # Source metadata
    source: str = "Spec sheet"
    notes: str = "Industry standard specifications"

    def __post_init__(self):
        """Validate parameters."""
        if self.vehicle_mass_gross <= 0:
            raise ValueError("Vehicle mass must be positive")
        if self.battery_capacity is not None and self.battery_capacity <= 0:
            raise ValueError("Battery capacity must be positive")
        if self.hydrogen_storage is not None and self.hydrogen_storage <= 0:
            raise ValueError("Hydrogen storage must be positive")


@dataclass
class OperationalContextParameters:
    """
    Real-world operational constraints based on Queensland trial data.

    These parameters reflect actual operational requirements and constraints
    observed in field trials, supporting realistic scenario modeling.

    Queensland Trial Data:
    - Maximum per trip for small trucks/buses: 100-200 km
    - Typical operational frequency: 1-3 trips/day
    - Charging infrastructure constraint: 2-5 hours
    - Maximum achievable range: ~300 km
    """

    # Route characteristics
    route_distance: float  # km - Per trip distance
    daily_operations: int  # trips/day - Typical operational frequency
    elevation_gain: float = 0.0  # m - Per cycle, affects energy consumption

    # Charging/refueling constraints
    charging_time_required: float = 3.5  # hours - Default mid-range
    full_charge_capacity_range: float = 300.0  # km - Maximum achievable range

    # Queensland trial validated ranges
    route_distance_min: float = 100.0  # km
    route_distance_max: float = 200.0  # km
    daily_operations_min: int = 1
    daily_operations_max: int = 3
    charging_time_min: float = 2.0  # hours
    charging_time_max: float = 5.0  # hours

    # Source metadata
    source: str = "Queensland trials"
    notes: str = "Real-world operational constraints from Queensland transport trials"

    def __post_init__(self):
        """Validate parameters against Queensland trial ranges."""
        if not (self.route_distance_min <= self.route_distance <= self.route_distance_max):
            raise ValueError(
                f"Route distance {self.route_distance} km outside Queensland trial range "
                f"[{self.route_distance_min}, {self.route_distance_max}]"
            )
        if not (self.daily_operations_min <= self.daily_operations <= self.daily_operations_max):
            raise ValueError(
                f"Daily operations {self.daily_operations} outside Queensland trial range "
                f"[{self.daily_operations_min}, {self.daily_operations_max}]"
            )


@dataclass
class EconomicEnvironmentalParameters:
    """
    Supporting cost analysis and emissions quantification.

    These parameters enable financial modeling and environmental impact
    assessment, supporting investment decision-making and Net Zero pathway analysis.
    """

    # Energy pricing
    energy_price_grid: float = 0.25  # $/kWh - Market data for BEV operational cost
    hydrogen_price: float = 8.0  # $/kg - Market data for FCET operational cost
    diesel_price: float = 1.50  # $/L - Baseline comparison

    # Financial parameters
    discount_rate: float = 0.08  # 8% - NPV calculations, risk assessment
    investment_multiplier_min: float = 2.0  # Clean energy vs diesel cost ratio
    investment_multiplier_max: float = 4.0  # Clean energy vs diesel cost ratio

    # Emissions factors
    diesel_emission_factor: float = 2.68  # kg CO2/L
    grid_emission_factor: float = 0.65  # kg CO2/kWh
    hydrogen_emission_factor: float = 9.0  # kg CO2/kg H2 (depends on production method)

    # Source metadata
    source: str = "Market data"
    application: str = "Cost analysis and emissions quantification"

    def get_investment_multiplier(self, technology: TechnologyType) -> float:
        """Get investment multiplier for specific technology."""
        multipliers = {
            TechnologyType.BEV: 2.0,
            TechnologyType.FCEV: 3.0,
            TechnologyType.HYBRID: 4.0,
            TechnologyType.DIESEL: 1.0,  # baseline
        }
        return multipliers.get(technology, 2.0)


@dataclass
class DegradationDurabilityParameters:
    """
    Critical factors incorporating real-world performance decline.

    Based on Queensland trial observations showing 15% battery degradation
    over 1.5 years (300km initial range → 255km after 1.5 years).

    Source: Queensland Trial Data - Update 1 (10/9)
    """

    # Battery degradation
    battery_degradation_rate: float = 0.10  # %/year - Annualized from Queensland data
    initial_battery_performance: float = 300.0  # km - Baseline range
    degraded_performance_18months: float = 255.0  # km - Real-world validation benchmark
    cycle_based_degradation: Optional[float] = None  # %/cycle - Usage-dependent wear

    # Degradation modeling
    lambda_batt: float = 0.15  # 15% over 1.5 years from Queensland trials
    measurement_period_years: float = 1.5  # years

    # Source metadata
    source: str = "Queensland trials - 1.5 year observation"
    application: str = "Range reduction modeling and real-world validation"

    def calculate_degraded_range(self, initial_range: float, years: float) -> float:
        """
        Calculate degraded range after specified years.

        Args:
            initial_range: Initial battery range in km
            years: Years of operation

        Returns:
            Degraded range in km
        """
        degradation_factor = 1 - (self.battery_degradation_rate * years)
        return initial_range * max(degradation_factor, 0.5)  # Cap at 50% degradation

    def validate_against_trial_data(self) -> bool:
        """Validate model against Queensland trial observations."""
        predicted = self.calculate_degraded_range(
            self.initial_battery_performance,
            self.measurement_period_years
        )
        tolerance = 5.0  # km
        return abs(predicted - self.degraded_performance_18months) <= tolerance


@dataclass
class TechnologyEfficiencyParameters:
    """
    Technology-specific efficiency parameters for energy consumption modeling.

    These parameters capture the fundamental efficiency characteristics of
    different powertrain technologies, enabling accurate energy consumption
    and emissions calculations.
    """

    technology_type: TechnologyType

    # Efficiency parameters
    drivetrain_efficiency: float  # Tank/battery-to-wheel efficiency
    energy_storage_efficiency: float  # Storage round-trip efficiency
    co2_intensity: float  # kg CO2 per unit energy
    investment_multiplier: float  # Relative to diesel baseline

    # Technology-specific metadata
    notes: str = ""

    @classmethod
    def for_technology(cls, tech: TechnologyType) -> 'TechnologyEfficiencyParameters':
        """Create efficiency parameters for specific technology."""
        params = {
            TechnologyType.BEV: {
                'drivetrain_efficiency': 0.90,
                'energy_storage_efficiency': 0.94,
                'co2_intensity': 0.65,  # kg/kWh
                'investment_multiplier': 2.0,
                'notes': 'Battery electric vehicle - highest efficiency'
            },
            TechnologyType.FCEV: {
                'drivetrain_efficiency': 0.85,
                'energy_storage_efficiency': 0.50,
                'co2_intensity': 9.0,  # kg/kg H2
                'investment_multiplier': 3.0,
                'notes': 'Fuel cell electric truck - depends on H2 source'
            },
            TechnologyType.HYBRID: {
                'drivetrain_efficiency': 0.88,
                'energy_storage_efficiency': 0.75,
                'co2_intensity': 1.5,  # Combined
                'investment_multiplier': 4.0,
                'notes': 'Hybrid powertrain - combined efficiency'
            },
            TechnologyType.DIESEL: {
                'drivetrain_efficiency': 0.35,
                'energy_storage_efficiency': 1.0,  # N/A
                'co2_intensity': 2.68,  # kg/L
                'investment_multiplier': 1.0,  # baseline
                'notes': 'Conventional diesel - baseline for comparison'
            },
        }

        if tech not in params:
            raise ValueError(f"Unknown technology type: {tech}")

        return cls(technology_type=tech, **params[tech])


# ============================================================================
# OUTPUT ATTRIBUTES
# ============================================================================


@dataclass
class PerformanceMetrics:
    """
    Key performance indicators for technology comparison and validation.

    These metrics enable quantitative comparison of different technologies
    and validation of model predictions against real-world performance.
    """

    # Range and efficiency
    effective_operational_range: float  # km - Actual vs theoretical range
    energy_efficiency: float  # kWh/km or kg H2/km - Consumption rate

    # Utilization metrics
    daily_utilization_rate: float  # % - Fleet capacity optimization
    charging_refueling_downtime: float  # hours/day - Operational efficiency

    # Performance validation
    theoretical_range: Optional[float] = None  # km - For comparison
    range_achievement_ratio: Optional[float] = None  # Actual/theoretical

    # Algorithm usage metadata
    algorithms_used: List[str] = field(default_factory=list)
    validation_criteria: str = "Queensland trial benchmarks"

    def calculate_range_achievement(self) -> float:
        """Calculate ratio of actual to theoretical range."""
        if self.theoretical_range is not None and self.theoretical_range > 0:
            self.range_achievement_ratio = self.effective_operational_range / self.theoretical_range
            return self.range_achievement_ratio
        return 0.0

    def meets_utilization_target(self, target: float = 0.85) -> bool:
        """Check if utilization meets target threshold."""
        return self.daily_utilization_rate >= target


@dataclass
class EconomicReturns:
    """
    Financial metrics supporting investment decision-making.

    Target: Break-even by year 4-5 with positive NPV and acceptable ROI.
    Validation: 95% confidence intervals from risk-adjusted projections.

    Source: Problem and Objective - Investment decision support
    """

    # Core financial metrics
    net_present_value: float  # $ - NPV
    return_on_investment: float  # % - ROI
    payback_period: float  # years
    total_cost_of_ownership: float  # $/year

    # Target ranges for validation
    target_payback_min: float = 4.0  # years
    target_payback_max: float = 5.0  # years
    target_npv_positive: bool = True

    # Validation confidence
    confidence_level: float = 0.95  # 95% confidence intervals

    # Validation metadata
    validation_criteria: str = "Queensland trial validation"
    risk_adjusted: bool = True

    def meets_investment_criteria(self) -> bool:
        """Check if investment meets target criteria."""
        npv_acceptable = self.net_present_value > 0 if self.target_npv_positive else True
        payback_acceptable = self.target_payback_min <= self.payback_period <= self.target_payback_max
        roi_acceptable = self.return_on_investment > 0

        return npv_acceptable and payback_acceptable and roi_acceptable

    def get_performance_summary(self) -> Dict[str, bool]:
        """Get summary of performance against criteria."""
        return {
            'npv_positive': self.net_present_value > 0,
            'payback_within_target': self.target_payback_min <= self.payback_period <= self.target_payback_max,
            'roi_positive': self.return_on_investment > 0,
            'meets_all_criteria': self.meets_investment_criteria()
        }


@dataclass
class EnvironmentalImpact:
    """
    Emissions quantification supporting Net Zero transition objectives.

    Baseline: Current transport sector contributes 44% of emissions
    Target: Significant reduction toward Net Zero pathway
    """

    # Emissions metrics
    co2_emissions_per_trip: float  # kg CO2
    annual_fleet_emissions: float  # tonnes CO2/year
    emission_factor_by_fuel: float  # kg CO2/unit energy

    # Baseline comparison
    baseline_diesel_emissions: float = 2.68  # kg CO2/L diesel
    current_sector_contribution: float = 0.44  # 44% sector contribution

    # Reduction targets
    target_reduction_percentage: float = 0.0  # Target % reduction
    actual_reduction_percentage: float = 0.0  # Achieved % reduction

    # Net Zero pathway alignment
    net_zero_aligned: bool = False
    pathway_description: str = "Technology-specific emissions pathway"

    def calculate_reduction(self, baseline_emissions: float) -> float:
        """
        Calculate emissions reduction percentage vs baseline.

        Args:
            baseline_emissions: Baseline annual emissions in tonnes CO2/year

        Returns:
            Reduction percentage (0-100)
        """
        if baseline_emissions <= 0:
            return 0.0

        reduction = baseline_emissions - self.annual_fleet_emissions
        self.actual_reduction_percentage = (reduction / baseline_emissions) * 100
        return self.actual_reduction_percentage

    def is_significant_reduction(self, threshold: float = 50.0) -> bool:
        """Check if reduction meets significance threshold."""
        return self.actual_reduction_percentage >= threshold

    def assess_net_zero_alignment(self, target_year: int = 2050) -> bool:
        """Assess if emissions trajectory aligns with Net Zero by target year."""
        # Simplified assessment - in practice would use trajectory modeling
        self.net_zero_aligned = self.is_significant_reduction(threshold=70.0)
        return self.net_zero_aligned


# ============================================================================
# COMPOSITE ATTRIBUTE SETS
# ============================================================================


@dataclass
class ModelInputAttributes:
    """
    Complete set of input attributes for mathematical modeling.

    Aggregates all input parameters required for comprehensive
    fleet decarbonization analysis.
    """

    vehicle_performance: VehiclePerformanceParameters
    operational_context: OperationalContextParameters
    economic_environmental: EconomicEnvironmentalParameters
    degradation_durability: DegradationDurabilityParameters
    technology_efficiency: TechnologyEfficiencyParameters

    # Integration metadata
    model_version: str = "1.0"
    created_date: str = ""
    notes: str = ""

    def validate_all(self) -> Dict[str, bool]:
        """Validate all input parameters."""
        return {
            'vehicle_performance': True,  # Already validated in __post_init__
            'operational_context': True,  # Already validated in __post_init__
            'degradation_validated': self.degradation_durability.validate_against_trial_data(),
        }


@dataclass
class ModelOutputAttributes:
    """
    Complete set of output attributes from mathematical modeling.

    Aggregates all output metrics for technology comparison,
    investment decision-making, and environmental impact assessment.
    """

    performance_metrics: PerformanceMetrics
    economic_returns: EconomicReturns
    environmental_impact: EnvironmentalImpact

    # Integration metadata
    scenario_id: str = ""
    technology_evaluated: Optional[TechnologyType] = None
    model_version: str = "1.0"
    calculation_date: str = ""

    # Validation status
    validated: bool = False
    confidence_score: float = 0.0

    def evaluate_scenario_viability(self) -> Dict[str, any]:
        """
        Evaluate overall scenario viability across all metrics.

        Returns:
            Dictionary with viability assessment
        """
        return {
            'performance_acceptable': self.performance_metrics.meets_utilization_target(),
            'economics_acceptable': self.economic_returns.meets_investment_criteria(),
            'environmental_acceptable': self.environmental_impact.is_significant_reduction(),
            'overall_viable': (
                self.performance_metrics.meets_utilization_target() and
                self.economic_returns.meets_investment_criteria() and
                self.environmental_impact.is_significant_reduction()
            ),
            'economic_summary': self.economic_returns.get_performance_summary(),
            'confidence': self.confidence_score
        }


# ============================================================================
# DATA INTEGRATION REFERENCES
# ============================================================================


@dataclass
class DataIntegrationMetadata:
    """
    Cross-references to related model components and validation data.

    These references ensure consistent parameter usage across the
    analytical framework while incorporating real-world validation data.
    """

    # Model integration points
    model_equations_ref: str = "Model Equations - Mathematical calculations"
    algorithm_parameters_ref: str = "Proposed Algorithms - Algorithm parameters"
    validation_scenarios_ref: str = "Synthetic Trial Results - Validation scenarios"
    implementation_timeline_ref: str = "Roadmap - Implementation timeline"

    # Research foundation
    emissions_methodology_ref: str = "Standard emissions modeling methodology"
    materials_durability_ref: str = "Al-Saadi et al. (2020) - Corrosion Modeling"
    industry_emissions_ref: str = "Industry emissions data (44% sector contribution)"
    technology_pathway_ref: str = "Arena (2024) - Future Fuels Report"
    transition_planning_ref: str = "Transition planning gap analysis"

    # Field validation
    queensland_trials_ref: str = "Queensland trials - Update 1 (10/9)"
    validation_benchmarks: List[str] = field(default_factory=lambda: [
        "Battery degradation: 15% over 1.5 years",
        "Operational range: 100-200km per trip",
        "Daily operations: 1-3 trips/day",
        "Charging time: 2-5 hours"
    ])

    # Data quality indicators
    data_quality_score: float = 0.0  # 0-1 scale
    validation_status: str = "Pending"
    last_updated: str = ""


__all__ = [
    # Input Attributes
    'VehiclePerformanceParameters',
    'OperationalContextParameters',
    'EconomicEnvironmentalParameters',
    'DegradationDurabilityParameters',
    'TechnologyEfficiencyParameters',

    # Output Attributes
    'PerformanceMetrics',
    'EconomicReturns',
    'EnvironmentalImpact',

    # Composite Sets
    'ModelInputAttributes',
    'ModelOutputAttributes',

    # Integration
    'DataIntegrationMetadata',
]
