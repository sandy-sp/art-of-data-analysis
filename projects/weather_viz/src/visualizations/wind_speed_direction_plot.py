import pandas as pd
import numpy as np
import plotly.graph_objects as go
from .plot_utils import apply_common_layout

def plot_wind_speed_and_direction(hourly_df, location=None):
    """
    Returns a Plotly figure with wind speed vectors (direction + magnitude).
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'windspeed_10m', 'winddirection_10m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        times = hourly_df['time']
        speeds = hourly_df['windspeed_10m']
        directions_deg = hourly_df['winddirection_10m']
        directions_rad = np.radians(directions_deg)

        # Calculate vector components
        u = speeds * np.cos(directions_rad)
        v = speeds * np.sin(directions_rad)

        scale = 0.1
        x_base = np.arange(len(times))
        y_base = np.zeros_like(x_base)
        x_tip = x_base + u * scale
        y_tip = y_base + v * scale

        fig = go.Figure()

        # Arrows as lines
        for i in range(len(times)):
            fig.add_trace(go.Scatter(
                x=[x_base[i], x_tip[i]],
                y=[y_base[i], y_tip[i]],
                mode='lines+markers',
                line=dict(color='green', width=2),
                marker=dict(size=6),
                showlegend=False,
                hovertemplate=(
                    f"Time: {times.iloc[i].strftime('%H:%M')}<br>"
                    f"Speed: {speeds.iloc[i]:.1f} km/h<br>"
                    f"Direction: {directions_deg.iloc[i]:.0f}°<extra></extra>"
                )
            ))

        title = f"Hourly Wind Speed and Direction (Vector Field) for {location}" if location else "Hourly Wind Speed and Direction (Vector Field)"

        fig.update_layout(
            title=title,
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(times))),
                ticktext=[t.strftime('%H:%M') for t in times],
                title="Time (Hourly)",
                tickangle=-45
            ),
            yaxis=dict(title="Vector Magnitude (Scaled)", zeroline=True),
            showlegend=False
        )

        return apply_common_layout(fig, title)
    return None
