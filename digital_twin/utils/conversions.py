"""
Unit conversion utilities.

This module provides conversion functions between different units
commonly used in fleet decarbonization analysis.
"""

from typing import Union
import numpy as np


# Distance conversions
def km_to_miles(km: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kilometers to miles."""
    return km * 0.621371


def miles_to_km(miles: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert miles to kilometers."""
    return miles * 1.60934


def m_to_km(meters: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert meters to kilometers."""
    return meters / 1000.0


def km_to_m(km: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kilometers to meters."""
    return km * 1000.0


# Speed conversions
def kmh_to_ms(kmh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert km/h to m/s."""
    return kmh / 3.6


def ms_to_kmh(ms: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert m/s to km/h."""
    return ms * 3.6


def mph_to_kmh(mph: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert miles per hour to km/h."""
    return mph * 1.60934


def kmh_to_mph(kmh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert km/h to miles per hour."""
    return kmh * 0.621371


# Energy conversions
def kwh_to_joules(kwh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kWh to Joules."""
    return kwh * 3_600_000


def joules_to_kwh(joules: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert Joules to kWh."""
    return joules / 3_600_000


def kwh_to_mj(kwh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kWh to MJ (megajoules)."""
    return kwh * 3.6


def mj_to_kwh(mj: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert MJ (megajoules) to kWh."""
    return mj / 3.6


def liter_diesel_to_kwh(liters: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert liters of diesel to kWh equivalent energy."""
    return liters * 10.0  # ~10 kWh per liter


def kwh_to_liter_diesel(kwh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kWh to diesel liter equivalent."""
    return kwh / 10.0


def kg_h2_to_kwh(kg_h2: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kg of hydrogen to kWh equivalent energy."""
    return kg_h2 * 33.3  # ~33.3 kWh per kg H2


def kwh_to_kg_h2(kwh: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kWh to hydrogen kg equivalent."""
    return kwh / 33.3


# Mass conversions
def kg_to_tonnes(kg: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kilograms to metric tonnes."""
    return kg / 1000.0


def tonnes_to_kg(tonnes: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert metric tonnes to kilograms."""
    return tonnes * 1000.0


def kg_to_lbs(kg: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kilograms to pounds."""
    return kg * 2.20462


def lbs_to_kg(lbs: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert pounds to kilograms."""
    return lbs / 2.20462


# Temperature conversions
def celsius_to_fahrenheit(celsius: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9


def celsius_to_kelvin(celsius: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


# Power conversions
def kw_to_hp(kw: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert kilowatts to horsepower."""
    return kw * 1.34102


def hp_to_kw(hp: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert horsepower to kilowatts."""
    return hp / 1.34102


# Pressure conversions
def bar_to_psi(bar: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert bar to PSI."""
    return bar * 14.5038


def psi_to_bar(psi: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert PSI to bar."""
    return psi / 14.5038


# Volume conversions
def liters_to_gallons_us(liters: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert liters to US gallons."""
    return liters * 0.264172


def gallons_us_to_liters(gallons: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert US gallons to liters."""
    return gallons / 0.264172


# Area conversions
def m2_to_ft2(m2: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert square meters to square feet."""
    return m2 * 10.7639


def ft2_to_m2(ft2: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert square feet to square meters."""
    return ft2 / 10.7639


# Financial conversions (percentage)
def decimal_to_percentage(decimal: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert decimal to percentage (0.05 -> 5)."""
    return decimal * 100


def percentage_to_decimal(percentage: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert percentage to decimal (5 -> 0.05)."""
    return percentage / 100


__all__ = [
    # Distance
    "km_to_miles",
    "miles_to_km",
    "m_to_km",
    "km_to_m",
    # Speed
    "kmh_to_ms",
    "ms_to_kmh",
    "mph_to_kmh",
    "kmh_to_mph",
    # Energy
    "kwh_to_joules",
    "joules_to_kwh",
    "kwh_to_mj",
    "mj_to_kwh",
    "liter_diesel_to_kwh",
    "kwh_to_liter_diesel",
    "kg_h2_to_kwh",
    "kwh_to_kg_h2",
    # Mass
    "kg_to_tonnes",
    "tonnes_to_kg",
    "kg_to_lbs",
    "lbs_to_kg",
    # Temperature
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "celsius_to_kelvin",
    "kelvin_to_celsius",
    # Power
    "kw_to_hp",
    "hp_to_kw",
    # Pressure
    "bar_to_psi",
    "psi_to_bar",
    # Volume
    "liters_to_gallons_us",
    "gallons_us_to_liters",
    # Financial
    "decimal_to_percentage",
    "percentage_to_decimal",
]
