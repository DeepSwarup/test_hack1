import pandas as pd
import numpy as np
from src.prediction import predict_solar_output
from src.energy_distribution import distribute_energy

def simulate_over_hours(model, hours, hour_start, day_of_year, irradiance, cloud_cover, temperature, 
                        demand, battery_capacity, initial_battery_level, use_optimization):
    """
    Simulate energy distribution over a range of hours, tracking battery level.
    Args:
        model: Trained ML model.
        hours: Number of hours to simulate.
        hour_start: Starting hour.
        day_of_year: Day of year.
        irradiance, cloud_cover, temperature: Initial weather conditions.
        demand, battery_capacity, initial_battery_level: Grid parameters.
        use_optimization: Use optimization-based distribution if True.
    Returns:
        DataFrame with simulation results.
    """
    results = []
    battery_level = initial_battery_level

    for h in range(hours):
        current_hour = (hour_start + h) % 24
        # Simulate weather variation: reduce irradiance at night (hours 18-6), add small random noise
        if 6 <= current_hour <= 18:
            irr = irradiance * (1 + np.random.uniform(-0.1, 0.1))
        else:
            irr = irradiance * 0.1  # Nighttime reduction
        cc = cloud_cover + np.random.uniform(-5, 5)
        temp = temperature + np.random.uniform(-2, 2)
        irr = max(0, min(1000, irr))
        cc = max(0, min(100, cc))
        temp = max(0, min(40, temp))

        solar_output = predict_solar_output(model, current_hour, day_of_year, irr, cc, temp)
        allocation = distribute_energy(solar_output, demand, battery_capacity, battery_level, use_optimization)
        battery_level = max(0, min(battery_level + allocation['battery_change'], battery_capacity))

        results.append({
            'Hour': current_hour,
            'Solar Output (kW)': solar_output,
            'Consumer (kW)': allocation['consumer'],
            'Battery Change (kWh)': allocation['battery_change'],
            'Battery Level (kWh)': battery_level,
            'Grid (kW)': allocation['grid'],
            'Irradiance (W/m^2)': irr,
            'Cloud Cover (%)': cc,
            'Temperature (°C)': temp
        })

    return pd.DataFrame(results)