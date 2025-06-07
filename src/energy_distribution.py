import numpy as np
from scipy.optimize import minimize

def rule_based_distribution(predicted_solar_output, demand, battery_capacity, battery_level):
    """
    Rule-based energy distribution for a simple grid.
    Args:
        predicted_solar_output (float): Predicted solar power in kW.
        demand (float): Consumer demand in kW.
        battery_capacity (float): Max battery capacity in kWh.
        battery_level (float): Current battery level in kWh.
    Returns:
        dict: Allocation of energy to consumer, battery (change in level), and grid.
    """
    allocation = {'consumer': 0, 'battery_change': 0, 'grid': 0}
    
    if predicted_solar_output >= demand:
        allocation['consumer'] = demand
        excess = predicted_solar_output - demand
        if battery_level < battery_capacity:
            allocation['battery_change'] = min(excess, battery_capacity - battery_level)
        allocation['grid'] = excess - allocation['battery_change']
    else:
        allocation['consumer'] = predicted_solar_output
        shortfall = demand - predicted_solar_output
        if battery_level > 0:
            battery_used = min(battery_level, shortfall)
            allocation['consumer'] += battery_used
            allocation['battery_change'] = -battery_used
    
    return allocation

def optimization_based_distribution(predicted_solar_output, demand, battery_capacity, battery_level):
    """
    Optimization-based energy distribution using SciPy.
    Args:
        predicted_solar_output (float): Predicted solar power in kW.
        demand (float): Consumer demand in kW.
        battery_capacity (float): Max battery capacity in kWh.
        battery_level (float): Current battery level in kWh.
    Returns:
        dict: Allocation of energy (solar, battery change, grid) to consumer.
    """
    def objective(x):
        return x[2]  # Minimize grid usage

    x0 = [min(predicted_solar_output, demand), 0, 0, 0]
    constraints = [
        {'type': 'ineq', 'fun': lambda x: x[0] + x[1] + x[2] - demand},
        {'type': 'ineq', 'fun': lambda x: predicted_solar_output - (x[0] + x[3])},
        {'type': 'ineq', 'fun': lambda x: battery_level - x[1]},
        {'type': 'ineq', 'fun': lambda x: battery_capacity - (battery_level + x[3])},
    ]
    bounds = [(0, predicted_solar_output), (0, battery_level), (0, None), (0, predicted_solar_output)]
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints, options={'disp': False})

    if result.success:
        solar_to_consumer, battery_to_consumer, grid_to_consumer, solar_to_battery = result.x
        return {
            'consumer': solar_to_consumer + battery_to_consumer + grid_to_consumer,
            'battery_change': solar_to_battery - battery_to_consumer,
            'grid': grid_to_consumer
        }
    return rule_based_distribution(predicted_solar_output, demand, battery_capacity, battery_level)

def distribute_energy(predicted_solar_output, demand, battery_capacity, battery_level, use_optimization=True):
    """
    Wrapper to choose between rule-based and optimization-based distribution.
    """
    if use_optimization:
        return optimization_based_distribution(predicted_solar_output, demand, battery_capacity, battery_level)
    return rule_based_distribution(predicted_solar_output, demand, battery_capacity, battery_level)