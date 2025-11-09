"""Terrain and gradient calculations."""

import numpy as np


def calculate_terrain_gradient(elevation_profile: np.ndarray, distance_profile: np.ndarray) -> np.ndarray:
    """Calculate gradient from elevation and distance."""
    rise = np.diff(elevation_profile)
    run = np.diff(distance_profile)
    run = np.where(run == 0, 1e-10, run)
    return np.arctan(rise / run)


__all__ = ["calculate_terrain_gradient"]
