import plotly.express as px
import pandas as pd

def plot_solar_output(data, hour, solar_output, title="Solar Output (Sample Data)"):
    """Plot solar output sample data with predicted point."""
    fig = px.line(data, x='hour', y='solar_output', title=title)
    fig.add_scatter(x=[hour], y=[solar_output], mode='markers', name='Predicted', marker=dict(size=10, color='red'))
    return fig

def plot_allocation(allocation, use_optimization=True):
    """Plot energy allocation as a bar chart."""
    allocation_data = pd.DataFrame({
        'Component': ['Consumer', 'Battery Change', 'Grid'],
        'Energy (kW/kWh)': [allocation['consumer'], allocation['battery_change'], allocation['grid']],
        'Method': ['Consumer', 'Battery Change', 'Grid'] if use_optimization else ['Consumer (Rule-Based)', 'Battery Change (Rule-Based)', 'Grid (Rule-Based)']
    })
    fig = px.bar(
        allocation_data, 
        x='Component', 
        y='Energy (kW/kWh)', 
        title='Energy Allocation', 
        color='Method',
        color_discrete_map={
            'Consumer': '#1f77b4',
            'Battery Change': '#ff7f0e',
            'Grid': '#2ca02c',
            'Consumer (Rule-Based)': '#aec7e8',
            'Battery Change (Rule-Based)': '#ffbb78',
            'Grid (Rule-Based)': '#98df8a'
        }
    )
    return fig

def plot_simulation(simulation_df, y_col, title):
    """Plot a time-series metric from simulation results."""
    fig = px.line(simulation_df, x='Hour', y=y_col, title=title, markers=True)
    return fig

def plot_costs_and_savings(simulation_df):
    """Plot grid costs and savings over time."""
    fig = px.line(
        simulation_df, 
        x='Hour', 
        y=['Grid_Cost', 'Savings'], 
        title='Grid Costs and Savings Over Time', 
        markers=True
    )
    return fig