import streamlit as st
from src.data_loader import load_data, load_model
from src.prediction import predict_solar_output
from src.energy_distribution import distribute_energy
from src.visualization import plot_solar_output, plot_allocation

def home_page():
    """Home page for single solar prediction and energy distribution."""
    st.title("Smart Solar Grid Management - Home")
    st.markdown("Adjust weather conditions and toggle optimization to predict solar output and manage energy distribution.")

    # Load data and model
    data = load_data()
    model = load_model()

    # Weather condition inputs
    st.header("Weather Conditions")
    weather_presets = {
        "Sunny": {"irradiance": 800, "cloud_cover": 10, "temperature": 30},
        "Cloudy": {"irradiance": 300, "cloud_cover": 70, "temperature": 20},
        "Stormy": {"irradiance": 100, "cloud_cover": 90, "temperature": 15},
        "Custom": {"irradiance": 500, "cloud_cover": 50, "temperature": 25}
    }
    weather_choice = st.selectbox("Select Weather Condition", list(weather_presets.keys()))

    if weather_choice != "Custom":
        irradiance = weather_presets[weather_choice]["irradiance"]
        cloud_cover = weather_presets[weather_choice]["cloud_cover"]
        temperature = weather_presets[weather_choice]["temperature"]
    else:
        irradiance = 500
        cloud_cover = 50
        temperature = 25

    col1, col2, col3 = st.columns(3)
    with col1:
        irradiance = st.slider("Solar Irradiance (W/m^2)", 0, 1000, int(irradiance))
    with col2:
        cloud_cover = st.slider("Cloud Cover (%)", 0, 100, int(cloud_cover))
    with col3:
        temperature = st.slider("Temperature (°C)", 0, 40, int(temperature))

    use_optimization = st.checkbox("Use Optimization-Based Distribution", value=True)
    st.markdown("*Note*: Optimization ensures demand is met by using the grid if needed, while rule-based relies only on solar and battery, potentially leaving a shortfall.")

    # Grid parameters
    st.sidebar.header("Grid Parameters")
    hour = st.sidebar.slider("Hour of Day", 0, 23, 12)
    day_of_year = st.sidebar.slider("Day of Year", 1, 365, 180)
    demand = st.sidebar.number_input("Consumer Demand (kW)", 0, 1000, 400)
    battery_capacity = st.sidebar.number_input("Battery Capacity (kWh)", 0, 500, 200)
    battery_level = st.sidebar.number_input("Current Battery Level (kWh)", 0, 500, 100)

    # Predict and distribute
    solar_output = predict_solar_output(model, hour, day_of_year, irradiance, cloud_cover, temperature)
    st.write(f"**Predicted Solar Output**: {solar_output:.2f} kW")

    allocation = distribute_energy(solar_output, demand, battery_capacity, battery_level, use_optimization)
    st.write("**Energy Allocation**:")
    st.write(f"- Consumer: {allocation['consumer']:.2f} kW")
    st.write(f"- Battery Change: {allocation['battery_change']:.2f} kWh ({'Charging' if allocation['battery_change'] > 0 else 'Discharging' if allocation['battery_change'] < 0 else 'No Change'})")
    st.write(f"- New Battery Level: {max(0, min(battery_level + allocation['battery_change'], battery_capacity)):.2f} kWh")
    st.write(f"- Grid: {allocation['grid']:.2f} kW")

    if allocation['consumer'] >= demand:
        st.success("Grid Status: Stable")
    else:
        st.warning(f"Grid Status: Risk of Imbalance (Shortfall: {demand - allocation['consumer']:.2f} kW)")

    # Visualizations
    st.plotly_chart(plot_solar_output(data, hour, solar_output))
    st.plotly_chart(plot_allocation(allocation, use_optimization))