"""Range, charging, capacity constraints."""


def check_range_constraint(vehicle_range: float, daily_distance: float, margin: float = 0.2) -> bool:
    """Check if vehicle range meets daily distance requirement."""
    return vehicle_range >= daily_distance * (1 + margin)


__all__ = ["check_range_constraint"]
