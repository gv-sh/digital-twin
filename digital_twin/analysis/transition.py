"""Transition planning analysis."""


def create_transition_plan(current_fleet: dict, target_fleet: dict, years: int) -> list:
    """Create phased transition plan."""
    return [{"year": i, "action": "Replace vehicles"} for i in range(1, years + 1)]


__all__ = ["create_transition_plan"]
