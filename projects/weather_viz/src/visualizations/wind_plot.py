import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout 

def plot_wind_speed(hourly_df, location=None):
    required_cols = ['time', 'windspeed_10m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='windspeed_10m',
            labels={"time": "Time (Hourly)", "windspeed_10m": "Wind Speed (km/h)"}
        )
        fig.update_traces(
            mode='lines+markers',
            line=dict(color='teal'),
            hovertemplate='Time: %{x}<br>Wind Speed: %{y:.1f} km/h<extra></extra>'
        )

        title = f"Hourly Wind Speed Forecast for {location}" if location else "Hourly Wind Speed Forecast"
        return apply_common_layout(fig, title)
    return None
