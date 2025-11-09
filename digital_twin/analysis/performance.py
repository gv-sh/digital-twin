"""KPI calculations (utilization, efficiency)."""


def calculate_utilization(actual_km: float, potential_km: float) -> float:
    """Calculate fleet utilization rate."""
    return actual_km / potential_km if potential_km > 0 else 0.0


def calculate_efficiency(energy_consumed: float, distance: float) -> float:
    """Calculate energy efficiency in kWh/km."""
    return energy_consumed / distance if distance > 0 else 0.0


__all__ = ["calculate_utilization", "calculate_efficiency"]
