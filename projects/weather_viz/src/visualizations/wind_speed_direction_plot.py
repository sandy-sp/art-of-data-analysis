import pandas as pd
import numpy as np
import plotly.graph_objects as go
from .plot_utils import apply_common_layout  # ⬅️ Add this import

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
        # Prepare time and vector components
        times = hourly_df['time']
        speeds = hourly_df['windspeed_10m']
        directions_deg = hourly_df['winddirection_10m']
        directions_rad = np.radians(directions_deg)

        # Vector components
        u = speeds * np.cos(directions_rad)
        v = speeds * np.sin(directions_rad)

        # Normalize arrows
        scale = 0.1
        x_end = np.arange(len(times))
        y_base = np.zeros_like(x_end)
        x_tip = x_end + u * scale
        y_tip = y_base + v * scale

        fig = go.Figure()

        # Base points
        fig.add_trace(go.Scatter(
            x=x_end,
            y=y_base,
            mode='markers',
            marker=dict(size=6, color='blue'),
            name='Wind Origin'
        ))

        # Arrow annotations
        for i in range(len(times)):
            fig.add_annotation(
                ax=x_end[i], ay=y_base[i],
                axref='x', ayref='y',
                x=x_tip[i], y=y_tip[i],
                xref='x', yref='y',
                showarrow=True,
                arrowhead=3,
                arrowsize=1.5,
                arrowwidth=1.5,
                arrowcolor='green'
            )

        # Dynamic title
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

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'windspeed_10m': [5, 10, 8],
        'winddirection_10m': [0, 90, 180]  # N, E, S
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_wind_speed_and_direction(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
