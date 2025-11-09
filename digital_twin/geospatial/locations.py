"""Depot placement and coverage analysis."""


def calculate_depot_coverage(depot_location: tuple, service_radius_km: float) -> float:
    """Calculate depot coverage area."""
    return 3.14159 * (service_radius_km ** 2)


__all__ = ["calculate_depot_coverage"]
