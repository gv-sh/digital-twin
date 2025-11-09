"""Geospatial module - Geographic analysis."""

from digital_twin.geospatial.routes import calculate_route_distance, optimize_route
from digital_twin.geospatial.terrain import calculate_terrain_gradient
from digital_twin.geospatial.climate import get_regional_climate
from digital_twin.geospatial.locations import calculate_depot_coverage

__all__ = [
    "calculate_route_distance", "optimize_route", "calculate_terrain_gradient",
    "get_regional_climate", "calculate_depot_coverage",
]
