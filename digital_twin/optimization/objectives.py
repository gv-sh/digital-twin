"""Cost minimization and emissions reduction objectives."""


def cost_objective(initial_cost: float, operating_cost: float, years: int) -> float:
    """Calculate total cost objective."""
    return initial_cost + (operating_cost * years)


__all__ = ["cost_objective"]
