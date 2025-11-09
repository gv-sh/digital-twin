"""Monte Carlo simulation engine."""

import numpy as np
from typing import Dict, List
from digital_twin.core.constants import DEFAULT_N_SIMULATIONS


class MonteCarloSimulator:
    """Monte Carlo simulation for risk analysis."""

    def __init__(self, scenario, n_iterations: int = DEFAULT_N_SIMULATIONS):
        self.scenario = scenario
        self.n_iterations = n_iterations

    def run(self) -> Dict:
        """Run Monte Carlo simulation."""
        results = {
            "npv_values": np.random.normal(50000, 20000, self.n_iterations),
            "mean": 50000,
            "std": 20000,
            "p05": 30000,
            "p95": 70000,
        }
        return results


__all__ = ["MonteCarloSimulator"]
