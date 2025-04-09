import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout 

def plot_hourly_temperature(hourly_df, location=None):
    """
    Returns a Plotly line plot of hourly temperature.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'temperature_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='temperature_2m',
            labels={"time": "Time (Hourly)", "temperature_2m": "Temperature (°C)"}
        )
        fig.update_traces(
            mode='lines+markers',
            line=dict(color='orange'),
            hovertemplate='Time: %{x}<br>Temp: %{y:.1f} °C<extra></extra>'
        )

        title = f"Hourly Temperature Forecast for {location}" if location else "Hourly Temperature Forecast"
        return apply_common_layout(fig, title)
    return None
