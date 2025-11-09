"""H2 station capacity and storage."""


def calculate_h2_station_capacity(daily_demand_kg: float, storage_days: int = 7) -> float:
    """Calculate required H2 storage capacity."""
    return daily_demand_kg * storage_days


__all__ = ["calculate_h2_station_capacity"]
