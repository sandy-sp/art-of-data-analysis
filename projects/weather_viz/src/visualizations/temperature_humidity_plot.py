import pandas as pd
import plotly.graph_objects as go
from .plot_utils import apply_common_layout

def plot_temperature_and_humidity(hourly_df, location=None):
    required_cols = ['time', 'temperature_2m', 'relativehumidity_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['temperature_2m'],
            name='Temperature (°C)',
            mode='lines+markers',
            yaxis='y1',
            line=dict(color='red'),
            hovertemplate='Time: %{x}<br>Temp: %{y:.1f} °C<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['relativehumidity_2m'],
            name='Humidity (%)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='blue', dash='dash'),
            hovertemplate='Time: %{x}<br>Humidity: %{y:.0f}%<extra></extra>'
        ))

        title = f"Hourly Temperature and Relative Humidity in {location}" if location else "Hourly Temperature and Relative Humidity"

        fig.update_layout(
            title=title,
            xaxis=dict(title="Time (Hourly)", tickangle=-45),
            yaxis=dict(
                title=dict(text="Temperature (°C)", font=dict(color="red")),
                tickfont=dict(color="red")
            ),
            yaxis2=dict(
                title=dict(text="Relative Humidity (%)", font=dict(color="blue")),
                tickfont=dict(color="blue"),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.01, y=1.05, orientation='h')
        )

        return apply_common_layout(fig, title)
    return None
