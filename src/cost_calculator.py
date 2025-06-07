def calculate_costs_and_savings(allocation, demand, price_per_kwh=0.15):
    """
    Calculate grid cost and savings from using solar and battery.
    Args:
        allocation (dict): Energy allocation result.
        demand (float): Consumer demand in kW.
        price_per_kwh (float): Grid electricity price in $/kWh.
    Returns:
        dict: Grid cost, savings, and total cost.
    """
    grid_cost = allocation['grid'] * price_per_kwh
    # Assume solar and battery energy is free; savings = cost of energy met by solar/battery
    savings = (demand - allocation['grid']) * price_per_kwh if allocation['grid'] >= 0 else demand * price_per_kwh
    total_cost = grid_cost
    return {
        'grid_cost': grid_cost,
        'savings': savings,
        'total_cost': total_cost
    }

def calculate_cumulative_costs(simulation_df, price_per_kwh=0.15):
    """
    Calculate cumulative costs and savings over a simulation.
    Args:
        simulation_df (DataFrame): Simulation results.
        price_per_kwh (float): Grid electricity price in $/kWh.
    Returns:
        DataFrame: Updated with cost and savings columns.
    """
    grid_costs = simulation_df['Grid (kW)'] * price_per_kwh
    savings = (simulation_df['Consumer (kW)'] - simulation_df['Grid (kW)']) * price_per_kwh
    savings = savings.where(simulation_df['Grid (kW)'] >= 0, simulation_df['Consumer (kW)'] * price_per_kwh)
    cumulative_savings = savings.cumsum()
    return simulation_df.assign(
        Grid_Cost=grid_costs,
        Savings=savings,
        Cumulative_Savings=cumulative_savings
    )