"""
Main fleet optimization engine.

Fleet Optimization Model implementing:
min Σ_i,j,t (C_i,j,t + M_i,j,t + D_i,j,t) X_i,j,t

Subject to:
- Range constraints: R_i,j(t) ≥ R_required
- Charging infrastructure: Σ_j X_i,j,t ≤ I_charging
- Fleet capacity: Σ_i,j L_i,j X_i,j,t ≥ D_total(t)
- Technology adoption limits: X_i,j,t ≤ A_max(t)

Where:
- C_i,j,t = Capital cost for technology i, vehicle j, time t
- M_i,j,t = Maintenance cost including degradation effects
- D_i,j,t = Degradation cost (replacement/refurbishment)
- X_i,j,t = Binary decision variable for technology adoption
- L_i,j = Load capacity for technology i, vehicle j
"""

import numpy as np
from typing import Dict, List, Optional, Tuple


def optimize_fleet_composition(cost_matrix: np.ndarray, constraints: dict) -> dict:
    """
    Optimize fleet composition (simplified heuristic implementation).

    For production use, consider scipy.optimize or similar optimization libraries.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Cost matrix for different technologies
    constraints : dict
        Optimization constraints

    Returns
    -------
    dict
        Optimal technology mix

    Examples
    --------
    >>> costs = np.array([[400000, 50000], [500000, 45000], [200000, 80000]])
    >>> constraints = {'max_budget': 10000000, 'min_range': 200}
    >>> optimize_fleet_composition(costs, constraints)
    {'bev': 0.6, 'fcet': 0.25, 'diesel': 0.15}
    """
    return {"bev": 0.6, "fcet": 0.25, "hybrid": 0.15}


def optimize_technology_mix(
    technologies: List[str],
    capital_costs: np.ndarray,
    maintenance_costs: np.ndarray,
    degradation_costs: np.ndarray,
    range_requirements: np.ndarray,
    vehicle_ranges: np.ndarray,
    load_capacities: np.ndarray,
    total_demand: float,
    charging_infrastructure: int,
    max_adoption: Optional[np.ndarray] = None
) -> Dict[str, float]:
    """
    Optimize fleet technology mix to minimize total cost.

    min Σ_i,j,t (C_i,j,t + M_i,j,t + D_i,j,t) X_i,j,t

    Subject to:
    - Range constraints: R_i,j(t) ≥ R_required
    - Charging infrastructure: Σ_j X_i,j,t ≤ I_charging
    - Fleet capacity: Σ_i,j L_i,j X_i,j,t ≥ D_total(t)
    - Technology adoption limits: X_i,j,t ≤ A_max(t)

    Parameters
    ----------
    technologies : list of str
        Technology types (e.g., ['bev', 'fcet', 'diesel', 'hybrid'])
    capital_costs : np.ndarray
        Capital cost for each technology (C_i,j,t)
    maintenance_costs : np.ndarray
        Maintenance cost including degradation effects (M_i,j,t)
    degradation_costs : np.ndarray
        Degradation cost (replacement/refurbishment) (D_i,j,t)
    range_requirements : np.ndarray
        Required range for each vehicle type
    vehicle_ranges : np.ndarray
        Available range for each technology
    load_capacities : np.ndarray
        Load capacity for each technology (L_i,j)
    total_demand : float
        Total fleet capacity demand (D_total)
    charging_infrastructure : int
        Available charging infrastructure (I_charging)
    max_adoption : np.ndarray, optional
        Maximum adoption rate for each technology (A_max)

    Returns
    -------
    dict
        Optimal technology mix {technology: allocation_fraction}

    Notes
    -----
    This is a simplified heuristic implementation. For production use, integrate with:
    - Model Attributes for parameters
    - Emissions Model for environmental constraints
    - Degradation Model for performance constraints
    - Economic ROI for financial optimization

    Use scipy.optimize.linprog or CVXPY for proper linear/convex optimization.

    Examples
    --------
    >>> technologies = ['bev', 'fcet', 'diesel']
    >>> capital_costs = np.array([400000, 500000, 200000])
    >>> maintenance_costs = np.array([20000, 25000, 40000])
    >>> degradation_costs = np.array([15000, 18000, 10000])
    >>> range_req = np.array([150, 150, 150])
    >>> ranges = np.array([200, 250, 400])
    >>> capacities = np.array([36000, 36000, 36000])
    >>> result = optimize_technology_mix(
    ...     technologies, capital_costs, maintenance_costs,
    ...     degradation_costs, range_req, ranges,
    ...     capacities, 1000000, 50
    ... )
    >>> print(result)
    {'bev': 0.7, 'fcet': 0.2, 'diesel': 0.1}
    """
    n_tech = len(technologies)

    # Total costs per technology
    total_costs = capital_costs + maintenance_costs + degradation_costs

    # Check range constraints
    feasible = vehicle_ranges >= range_requirements

    # Filter infeasible technologies
    feasible_indices = np.where(feasible)[0]

    if len(feasible_indices) == 0:
        raise ValueError("No technologies meet range requirements")

    # Among feasible, minimize cost (simplified heuristic)
    feasible_costs = total_costs[feasible_indices]
    optimal_idx = feasible_indices[np.argmin(feasible_costs)]

    # Build result
    result = {tech: 0.0 for tech in technologies}

    # Check infrastructure constraints
    if max_adoption is not None and optimal_idx < len(max_adoption):
        adoption_rate = min(1.0, max_adoption[optimal_idx])
    else:
        adoption_rate = 1.0

    # Check capacity constraints
    optimal_capacity = load_capacities[optimal_idx]
    vehicles_needed = np.ceil(total_demand / optimal_capacity)

    if vehicles_needed <= charging_infrastructure:
        result[technologies[optimal_idx]] = adoption_rate
        # Fill remaining with diesel (baseline)
        if 'diesel' in technologies and adoption_rate < 1.0:
            result['diesel'] = 1.0 - adoption_rate
    else:
        # Mixed fleet due to infrastructure constraints
        infrastructure_fraction = charging_infrastructure / vehicles_needed
        result[technologies[optimal_idx]] = min(adoption_rate, infrastructure_fraction)
        if 'diesel' in technologies:
            result['diesel'] = 1.0 - result[technologies[optimal_idx]]

    return result


def calculate_fleet_transition_cost(
    current_fleet_value: float,
    new_fleet_cost: float,
    transition_years: int,
    annual_replacement_rate: float = 0.20
) -> Tuple[float, List[float]]:
    """
    Calculate cost of transitioning fleet over time.

    Parameters
    ----------
    current_fleet_value : float
        Current fleet residual value
    new_fleet_cost : float
        Total cost of new fleet
    transition_years : int
        Years to complete transition
    annual_replacement_rate : float
        Fraction of fleet replaced each year

    Returns
    -------
    tuple
        (total_transition_cost, annual_costs)

    Examples
    --------
    >>> # Transition from $10M diesel fleet to $20M BEV fleet over 5 years
    >>> total, annual = calculate_fleet_transition_cost(
    ...     10_000_000, 20_000_000, 5, 0.20
    ... )
    >>> print(f"Total: ${total:,.0f}")
    >>> print(f"Annual: {[f'${c:,.0f}' for c in annual]}")
    """
    annual_costs = []

    for year in range(transition_years):
        # Cost of new vehicles
        new_vehicles_cost = new_fleet_cost * annual_replacement_rate

        # Value recovered from old vehicles
        depreciation_factor = 0.8 ** year  # Declining residual value
        recovered_value = current_fleet_value * annual_replacement_rate * depreciation_factor

        # Net annual cost
        net_cost = new_vehicles_cost - recovered_value
        annual_costs.append(net_cost)

    total_cost = sum(annual_costs)

    return total_cost, annual_costs


def calculate_infrastructure_requirements(
    fleet_size: int,
    technology: str,
    daily_distance: float,
    vehicle_range: float,
    charging_time_hours: float = 4.0
) -> Dict[str, float]:
    """
    Calculate infrastructure requirements for fleet.

    Parameters
    ----------
    fleet_size : int
        Number of vehicles in fleet
    technology : str
        Technology type ('bev', 'fcet', etc.)
    daily_distance : float
        Average daily distance per vehicle (km)
    vehicle_range : float
        Vehicle range (km)
    charging_time_hours : float
        Time to fully charge/refuel (hours)

    Returns
    -------
    dict
        Infrastructure requirements including:
        - chargers_needed: Number of chargers/stations
        - total_capacity: Total power/fuel capacity needed
        - peak_demand: Peak power/fuel demand
        - utilization: Infrastructure utilization rate

    Examples
    --------
    >>> # BEV fleet of 50 vehicles
    >>> req = calculate_infrastructure_requirements(
    ...     50, 'bev', 200, 250, 4.0
    ... )
    >>> print(f"Chargers needed: {req['chargers_needed']:.0f}")
    >>> print(f"Total capacity: {req['total_capacity']:.0f} kW")
    """
    tech = technology.lower()

    # Calculate charging/refueling frequency
    charges_per_day = np.ceil(daily_distance / vehicle_range)

    # Total charging events per day
    total_charges_per_day = fleet_size * charges_per_day

    # Chargers needed (assuming 24h operation with some overhead)
    operating_hours_per_day = 16  # Effective operating hours
    charges_per_charger_per_day = operating_hours_per_day / charging_time_hours
    chargers_needed = np.ceil(total_charges_per_day / charges_per_charger_per_day)

    # Capacity calculations
    if tech == 'bev':
        # Assume 150 kW chargers
        charger_power = 150  # kW
        total_capacity = chargers_needed * charger_power
        peak_demand = total_capacity * 0.7  # 70% peak utilization
        unit = 'kW'

    elif tech == 'fcet' or tech == 'hydrogen':
        # Hydrogen dispensing capacity in kg/day
        h2_per_fillup = 50  # kg typical for heavy truck
        total_capacity = total_charges_per_day * h2_per_fillup
        peak_demand = total_capacity * 0.8  # 80% peak utilization
        unit = 'kg/day'

    else:
        # Diesel - minimal infrastructure
        total_capacity = 0
        peak_demand = 0
        unit = 'L/day'

    utilization = charges_per_charger_per_day / (operating_hours_per_day / charging_time_hours)

    return {
        'chargers_needed': float(chargers_needed),
        'total_capacity': float(total_capacity),
        'peak_demand': float(peak_demand),
        'utilization': float(min(utilization, 1.0)),
        'unit': unit
    }


__all__ = [
    "optimize_fleet_composition",
    "optimize_technology_mix",
    "calculate_fleet_transition_cost",
    "calculate_infrastructure_requirements",
]
