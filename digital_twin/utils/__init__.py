"""
Utils module - Utility functions with no dependencies.

This module provides mathematical utilities, conversions, date handling,
validators, and formatters.
"""

from digital_twin.utils.math_utils import (
    linear_interpolate,
    exponential_decay,
    calculate_gradient,
    moving_average,
    compound_growth,
)

from digital_twin.utils.conversions import (
    km_to_miles,
    miles_to_km,
    kmh_to_ms,
    ms_to_kmh,
    kwh_to_joules,
    joules_to_kwh,
    liter_diesel_to_kwh,
    kg_h2_to_kwh,
    celsius_to_fahrenheit,
    kg_to_tonnes,
)

from digital_twin.utils.date_utils import (
    add_years,
    years_between,
    generate_date_range,
)

from digital_twin.utils.validators import (
    is_positive,
    is_non_negative,
    is_percentage,
    is_in_range,
)

from digital_twin.utils.formatters import (
    format_currency,
    format_percentage,
    format_number,
    format_large_number,
    format_distance,
    format_energy,
    format_co2,
)

__all__ = [
    # Math utils
    "linear_interpolate",
    "exponential_decay",
    "calculate_gradient",
    "moving_average",
    "compound_growth",
    # Conversions
    "km_to_miles",
    "miles_to_km",
    "kmh_to_ms",
    "ms_to_kmh",
    "kwh_to_joules",
    "joules_to_kwh",
    "liter_diesel_to_kwh",
    "kg_h2_to_kwh",
    "celsius_to_fahrenheit",
    "kg_to_tonnes",
    # Date utils
    "add_years",
    "years_between",
    "generate_date_range",
    # Validators
    "is_positive",
    "is_non_negative",
    "is_percentage",
    "is_in_range",
    # Formatters
    "format_currency",
    "format_percentage",
    "format_number",
    "format_large_number",
    "format_distance",
    "format_energy",
    "format_co2",
]
