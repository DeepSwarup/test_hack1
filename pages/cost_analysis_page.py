import streamlit as st
from src.data_loader import load_data, load_model
from src.simulation import simulate_over_hours
from src.cost_calculator import calculate_costs_and_savings, calculate_cumulative_costs
from src.visualization import plot_simulation, plot_costs_and_savings

def cost_analysis_page():
    """Cost Analysis page for calculating energy costs and savings."""
    st.title("Smart Solar Grid Management - Cost Analysis")
    st.markdown("Calculate energy costs and savings based on grid usage over a simulation period.")

    # Load data and model
    data = load_data()
    model = load_model()

    # Weather condition inputs
    st.header("Weather Conditions (Initial)")
    weather_presets = {
        "Sunny": {"irradiance": 800, "cloud_cover": 10, "temperature": 30},
        "Cloudy": {"irradiance": 300, "cloud_cover": 70, "temperature": 20},
        "Stormy": {"irradiance": 100, "cloud_cover": 90, "temperature": 15},
        "Custom": {"irradiance": 500, "cloud_cover": 50, "temperature": 25}
    }
    weather_choice = st.selectbox("Select Initial Weather Condition", list(weather_presets.keys()))

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

    # Grid parameters
    st.sidebar.header("Grid Parameters")
    hour_start = st.sidebar.slider("Starting Hour", 0, 23, 12)
    day_of_year = st.sidebar.slider("Day of Year", 1, 365, 180)
    hours = st.sidebar.slider("Number of Hours to Simulate", 1, 24, 6)
    demand = st.sidebar.number_input("Consumer Demand (kW)", 0, 1000, 400)
    battery_capacity = st.sidebar.number_input("Battery Capacity (kWh)", 0, 500, 200)
    price_per_kwh = st.sidebar.number_input("Grid Electricity Price ($/kWh)", 0.0, 1.0, 0.15, step=0.01)

    # Initialize battery level in session state
    if 'battery_level' not in st.session_state:
        st.session_state.battery_level = 100.0
    battery_level = st.session_state.battery_level
    st.sidebar.write(f"Current Battery Level: {battery_level:.2f} kWh")

    if st.button("Calculate Costs"):
        simulation_df = simulate_over_hours(
            model, hours, hour_start, day_of_year, irradiance, cloud_cover, temperature,
            demand, battery_capacity, battery_level, use_optimization
        )
        # Update battery level for next simulation
        st.session_state.battery_level = simulation_df['Battery Level (kWh)'].iloc[-1]

        # Calculate costs
        simulation_df = calculate_cumulative_costs(simulation_df, price_per_kwh)

        # Display results
        st.write("**Cost Analysis Results**:")
        st.dataframe(simulation_df.style.format({
            'Solar Output (kW)': '{:.2f}',
            'Consumer (kW)': '{:.2f}',
            'Battery Change (kWh)': '{:.2f}',
            'Battery Level (kWh)': '{:.2f}',
            'Grid (kW)': '{:.2f}',
            'Irradiance (W/m^2)': '{:.2f}',
            'Cloud Cover (%)': '{:.2f}',
            'Temperature (°C)': '{:.2f}',
            'Grid_Cost': '${:.2f}',
            'Savings': '${:.2f}',
            'Cumulative_Savings': '${:.2f}'
        }))

        # Visualizations
        st.plotly_chart(plot_costs_and_savings(simulation_df))
        st.plotly_chart(plot_simulation(simulation_df, 'Cumulative_Savings', 'Cumulative Savings Over Time'))