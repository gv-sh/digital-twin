"""
Physical and economic constants for fleet decarbonization analysis.

This module contains fundamental constants used throughout the system.
"""

# Physical Constants
GRAVITY_ACCELERATION = 9.81  # m/s²
AIR_DENSITY_SEA_LEVEL = 1.225  # kg/m³ at 15°C
ROLLING_RESISTANCE_COEFF = 0.006  # Typical for heavy trucks on asphalt
DEFAULT_DRAG_COEFFICIENT = 1.0  # Cd for heavy trucks (0.6-1.0 typical)
DEFAULT_FRONTAL_AREA = 8.0  # m² for heavy trucks

# Energy Conversion Factors
KWH_TO_JOULES = 3_600_000  # 1 kWh = 3.6 MJ
LITER_DIESEL_TO_KWH = 10.0  # Energy content of diesel
KG_H2_TO_KWH = 33.3  # Energy content of hydrogen
LITER_DIESEL_TO_MJ = 36.0  # Energy content of diesel in MJ

# Emission Factors (kg CO2 equivalent)
DIESEL_CO2_PER_LITER = 2.68  # kg CO2 per liter of diesel
PETROL_CO2_PER_LITER = 2.31  # kg CO2 per liter of petrol
GRID_ELECTRICITY_CO2_PER_KWH = 0.75  # kg CO2 per kWh (Australian grid average)
GREEN_H2_CO2_PER_KG = 0.48  # kg CO2 per kg H2 (green hydrogen via electrolysis)
GREY_H2_CO2_PER_KG = 10.0  # kg CO2 per kg H2 (from natural gas)

# NOx Emission Factors (g/km)
DIESEL_NOX_PER_KM = 5.0  # Euro VI standard
BEV_NOX_PER_KM = 0.0
FCET_NOX_PER_KM = 0.0

# PM Emission Factors (g/km)
DIESEL_PM_PER_KM = 0.01  # Euro VI standard
BEV_PM_PER_KM = 0.0
FCET_PM_PER_KM = 0.0

# Efficiency Factors
DIESEL_TANK_TO_WHEEL = 0.35  # 35% efficiency
BEV_BATTERY_TO_WHEEL = 0.85  # 85% efficiency
FCET_H2_TO_WHEEL = 0.50  # 50% efficiency
HYBRID_COMBINED = 0.60  # 60% efficiency

# Battery Parameters
BATTERY_DEGRADATION_RATE = 0.106  # ~10% capacity loss per year
BATTERY_CYCLE_LIFE = 3000  # Typical cycles
BATTERY_ENERGY_DENSITY_WH_KG = 150  # Wh/kg for commercial batteries

# Economic Defaults
DEFAULT_DISCOUNT_RATE = 0.08  # 8% discount rate
DEFAULT_ANALYSIS_PERIOD = 5  # years
DEFAULT_RESIDUAL_VALUE_FACTOR = 0.20  # 20% of initial cost

# Price Escalation Rates (annual)
FUEL_PRICE_ESCALATION = 0.03  # 3% per year
ELECTRICITY_PRICE_ESCALATION = 0.02  # 2% per year
H2_PRICE_ESCALATION = 0.01  # 1% per year (decreasing over time)
MAINTENANCE_ESCALATION = 0.025  # 2.5% per year

# Operating Parameters
OPERATING_DAYS_PER_YEAR = 250
HOURS_PER_YEAR = 8760
AVERAGE_AMBIENT_TEMP = 25.0  # °C

# Vehicle Parameters
TYPICAL_TRUCK_MASS_KG = 18000  # kg (laden)
TYPICAL_ANNUAL_KM = 100000  # km per year
TYPICAL_DAILY_KM = 400  # km per day
TYPICAL_AVERAGE_SPEED_KMH = 80  # km/h

# Uncertainty Parameters (for Monte Carlo)
FUEL_PRICE_STD_DEV = 0.20  # 20% standard deviation
ELECTRICITY_PRICE_STD_DEV = 0.15  # 15% standard deviation
UTILIZATION_MIN = 0.70  # 70% minimum
UTILIZATION_MAX = 0.95  # 95% maximum
DEGRADATION_UNCERTAINTY_STD = 0.25  # 25% uncertainty

# Monte Carlo Simulation
DEFAULT_N_SIMULATIONS = 10000
CONFIDENCE_LEVEL_95 = 0.95
CONFIDENCE_LEVEL_99 = 0.99

# Infrastructure
DEPOT_CHARGER_POWER_KW = 150  # kW
FAST_CHARGER_POWER_KW = 350  # kW
H2_STATION_CAPACITY_KG_DAY = 1000  # kg/day
GRID_CONNECTION_COST_PER_KW = 500  # AUD per kW

__all__ = [
    "GRAVITY_ACCELERATION",
    "AIR_DENSITY_SEA_LEVEL",
    "ROLLING_RESISTANCE_COEFF",
    "DEFAULT_DRAG_COEFFICIENT",
    "DEFAULT_FRONTAL_AREA",
    "KWH_TO_JOULES",
    "LITER_DIESEL_TO_KWH",
    "KG_H2_TO_KWH",
    "DIESEL_CO2_PER_LITER",
    "GRID_ELECTRICITY_CO2_PER_KWH",
    "GREEN_H2_CO2_PER_KG",
    "DIESEL_TANK_TO_WHEEL",
    "BEV_BATTERY_TO_WHEEL",
    "FCET_H2_TO_WHEEL",
    "BATTERY_DEGRADATION_RATE",
    "DEFAULT_DISCOUNT_RATE",
    "DEFAULT_ANALYSIS_PERIOD",
    "FUEL_PRICE_ESCALATION",
    "ELECTRICITY_PRICE_ESCALATION",
    "TYPICAL_TRUCK_MASS_KG",
    "TYPICAL_ANNUAL_KM",
    "DEFAULT_N_SIMULATIONS",
]
