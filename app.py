import streamlit as st
from pages.home import home_page
from pages.simulation_page import simulation_page
from pages.cost_analysis_page import cost_analysis_page

# Configure Streamlit app
st.set_page_config(page_title="Smart Solar Grid Management", layout="wide")

# Navigation
pages = {
    "Home": home_page,
    "Simulation": simulation_page,
    "Cost Analysis": cost_analysis_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display selected page
pages[selection]()