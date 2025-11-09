"""Charger capacity and queue theory."""


def calculate_charging_time(battery_capacity_kwh: float, charger_power_kw: float) -> float:
    """Calculate charging time in hours."""
    return battery_capacity_kwh / charger_power_kw


def calculate_charger_utilization(vehicles_per_day: int, avg_charging_time_hours: float) -> float:
    """Calculate charger utilization rate."""
    return (vehicles_per_day * avg_charging_time_hours) / 24.0


__all__ = ["calculate_charging_time", "calculate_charger_utilization"]
