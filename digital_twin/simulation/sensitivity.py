"""Parameter sensitivity and tornado charts."""

import numpy as np


def calculate_sensitivity(base_value: float, param_variation: dict) -> dict:
    """Calculate parameter sensitivity."""
    sensitivity = {}
    for param, variation in param_variation.items():
        impact = variation * 0.1  # Simplified
        sensitivity[param] = impact / base_value
    return sensitivity


__all__ = ["calculate_sensitivity"]
