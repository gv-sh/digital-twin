"""Grid connections and demand charges."""


def calculate_grid_connection_cost(peak_power_kw: float, cost_per_kw: float = 500) -> float:
    """Calculate grid connection cost."""
    return peak_power_kw * cost_per_kw


__all__ = ["calculate_grid_connection_cost"]
