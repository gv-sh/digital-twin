"""Monte Carlo risk assessment algorithm."""

from digital_twin.simulation import MonteCarloSimulator
from digital_twin.economics import calculate_npv


def run_risk_assessment(scenario, n_simulations: int = 10000) -> dict:
    """Run comprehensive risk assessment."""
    simulator = MonteCarloSimulator(scenario, n_simulations)
    results = simulator.run()
    return results


__all__ = ["run_risk_assessment"]
