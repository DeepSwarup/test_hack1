import pandas as pd
import joblib
import os

def load_data(data_path="data/solar_data.csv"):
    """Load the solar dataset."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    return pd.read_csv(data_path)

def load_model(model_path="data/solar_model.pkl"):
    """Load the trained ML model."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)