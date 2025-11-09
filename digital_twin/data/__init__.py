"""Data module - Data management and generation."""

from digital_twin.data.generators import (
    generate_fleet_data,
    create_diesel_baseline,
    create_bev_specs,
    create_fcet_specs,
    create_hybrid_specs,
    create_base_technologies,
    create_base_operational_profile,
    create_base_financial_params,
)
from digital_twin.data.loaders import load_csv, load_excel
from digital_twin.data.preprocessors import clean_numeric_data, normalize_data
from digital_twin.data.providers import get_weather_data, get_fuel_prices

__all__ = [
    "generate_fleet_data",
    "create_diesel_baseline",
    "create_bev_specs",
    "create_fcet_specs",
    "create_hybrid_specs",
    "create_base_technologies",
    "create_base_operational_profile",
    "create_base_financial_params",
    "load_csv",
    "load_excel",
    "clean_numeric_data",
    "normalize_data",
    "get_weather_data",
    "get_fuel_prices",
]
