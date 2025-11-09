"""
Core type definitions for fleet decarbonization analysis.

This module defines the fundamental types, enumerations, and type aliases
used throughout the fleet decarbonization system.
"""

from enum import Enum
from typing import TypedDict, Optional


class VehicleType(Enum):
    """Vehicle type classifications."""
    HEAVY_TRUCK = "heavy_truck"
    MEDIUM_TRUCK = "medium_truck"
    LIGHT_TRUCK = "light_truck"
    BUS = "bus"
    VAN = "van"


class FuelType(Enum):
    """Fuel/energy source types."""
    DIESEL = "diesel"
    PETROL = "petrol"
    ELECTRIC = "electric"
    HYDROGEN = "hydrogen"
    HYBRID_DIESEL_ELECTRIC = "hybrid_diesel_electric"
    HYBRID_PETROL_ELECTRIC = "hybrid_petrol_electric"
    CNG = "cng"  # Compressed Natural Gas
    LNG = "lng"  # Liquefied Natural Gas


class TechnologyType(Enum):
    """Clean energy technology types."""
    DIESEL = "diesel"
    BEV = "bev"  # Battery Electric Vehicle
    FCET = "fcet"  # Fuel Cell Electric Truck
    HYBRID = "hybrid"


class OperationalContext(Enum):
    """Operational environment contexts."""
    URBAN = "urban"
    SUBURBAN = "suburban"
    HIGHWAY = "highway"
    MIXED = "mixed"
    OFF_ROAD = "off_road"


class TerrainType(Enum):
    """Terrain classifications."""
    FLAT = "flat"
    ROLLING = "rolling"
    HILLY = "hilly"
    MOUNTAINOUS = "mountainous"


class ChargingType(Enum):
    """Charging infrastructure types."""
    SLOW_AC = "slow_ac"  # Level 1/2
    FAST_DC = "fast_dc"  # DC Fast Charging
    ULTRA_FAST = "ultra_fast"  # 350kW+
    DEPOT = "depot"
    OPPORTUNITY = "opportunity"


class IncentiveType(Enum):
    """Government incentive types."""
    CAPITAL_GRANT = "capital_grant"
    TAX_CREDIT = "tax_credit"
    REBATE = "rebate"
    LOAN = "loan"
    SUBSIDY = "subsidy"


__all__ = [
    "VehicleType",
    "FuelType",
    "TechnologyType",
    "OperationalContext",
    "TerrainType",
    "ChargingType",
    "IncentiveType",
]
