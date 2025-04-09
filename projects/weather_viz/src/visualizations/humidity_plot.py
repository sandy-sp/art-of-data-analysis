import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout

def plot_humidity(hourly_df, location=None):
    required_cols = ['time', 'relativehumidity_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='relativehumidity_2m',
            labels={"time": "Time (Hourly)", "relativehumidity_2m": "Relative Humidity (%)"}
        )
        fig.update_traces(
            mode='lines+markers',
            line=dict(color='green'),
            hovertemplate='Time: %{x}<br>Humidity: %{y:.0f}%<extra></extra>'
        )

        title = f"Hourly Relative Humidity Forecast for {location}" if location else "Hourly Relative Humidity Forecast"
        return apply_common_layout(fig, title)
    return None
