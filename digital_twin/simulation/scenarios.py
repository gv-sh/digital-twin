"""Scenario management and comparison."""


def create_scenario(name: str, params: dict) -> dict:
    """Create a scenario."""
    return {"name": name, **params}


def compare_scenarios(scenarios: list) -> dict:
    """Compare multiple scenarios."""
    return {"best": scenarios[0]["name"] if scenarios else None}


__all__ = ["create_scenario", "compare_scenarios"]
