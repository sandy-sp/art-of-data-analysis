import pandas as pd
import plotly.graph_objects as go
from .plot_utils import apply_common_layout 

def plot_daily_temperature_range(daily_df, location=None):
    required_cols = ['time', 'temperature_2m_max', 'temperature_2m_min']
    if (
        daily_df is not None and 
        not daily_df.empty and 
        all(col in daily_df.columns for col in required_cols)
    ):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_max'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='red'),
            hovertemplate='Date: %{x}<br>Max Temp: %{y:.1f} °C<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_min'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='blue'),
            hovertemplate='Date: %{x}<br>Min Temp: %{y:.1f} °C<extra></extra>'
        ))

        title = f"Daily Temperature Range Forecast for {location}" if location else "Daily Temperature Range Forecast"
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            legend_title="Legend"
        )

        return apply_common_layout(fig, title)
    return None
