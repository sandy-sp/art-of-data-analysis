import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout 

def plot_feels_like_temperature(hourly_df, location=None):
    required_cols = ['time', 'feels_like_temperature_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='feels_like_temperature_2m',
            labels={
                "time": "Time (Hourly)", 
                "feels_like_temperature_2m": "Feels Like Temperature (°C)"
            }
        )
        fig.update_traces(
            mode='lines+markers',
            line=dict(color='purple'),
            hovertemplate='Time: %{x}<br>Feels Like: %{y:.1f} °C<extra></extra>'
        )

        title = f"Hourly Feels Like Temperature Forecast for {location}" if location else "Hourly Feels Like Temperature Forecast"
        return apply_common_layout(fig, title)
    return None
