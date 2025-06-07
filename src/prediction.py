import pandas as pd
import numpy as np

def predict_solar_output(model, hour, day_of_year, irradiance, cloud_cover, temperature):
    """Predict solar output using the ML model."""
    features = pd.DataFrame(
        [[hour, day_of_year, irradiance, cloud_cover, temperature]],
        columns=['hour', 'day_of_year', 'irradiance', 'cloud_cover', 'temperature']
    )
    return model.predict(features)[0]