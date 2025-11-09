"""Route optimization and elevation profiles."""

import numpy as np


def calculate_route_distance(waypoints: list) -> float:
    """Calculate total route distance from waypoints."""
    return sum(np.linalg.norm(np.array(waypoints[i+1]) - np.array(waypoints[i]))
               for i in range(len(waypoints)-1))


def optimize_route(start: tuple, end: tuple, waypoints: list) -> list:
    """Optimize route (stub implementation)."""
    return [start] + waypoints + [end]


__all__ = ["calculate_route_distance", "optimize_route"]
