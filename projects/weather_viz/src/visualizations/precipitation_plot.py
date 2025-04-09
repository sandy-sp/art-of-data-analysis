import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout

def plot_precipitation(hourly_df, location=None):
    required_cols = ['time', 'precipitation']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.bar(
            hourly_df,
            x='time',
            y='precipitation',
            labels={"time": "Time (Hourly)", "precipitation": "Precipitation (mm)"}
        )
        fig.update_traces(
            hovertemplate='Time: %{x}<br>Precipitation: %{y:.2f} mm<extra></extra>'
        )
        fig.update_layout(bargap=0.1)

        title = f"Hourly Precipitation Forecast for {location}" if location else "Hourly Precipitation Forecast"
        return apply_common_layout(fig, title)
    return None
