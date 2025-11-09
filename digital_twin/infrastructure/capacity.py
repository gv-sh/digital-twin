"""Infrastructure capacity planning."""


def calculate_required_chargers(fleet_size: int, vehicles_per_charger: int = 5) -> int:
    """Calculate required number of chargers."""
    return (fleet_size + vehicles_per_charger - 1) // vehicles_per_charger


__all__ = ["calculate_required_chargers"]
