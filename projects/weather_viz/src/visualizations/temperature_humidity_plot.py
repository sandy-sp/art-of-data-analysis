import pandas as pd
import plotly.graph_objects as go
from .plot_utils import apply_common_layout  # ⬅️ Add this import

def plot_temperature_and_humidity(hourly_df, location=None):
    """
    Returns a Plotly figure combining hourly temperature and relative humidity with dual y-axes.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'temperature_2m', 'relativehumidity_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = go.Figure()

        # Temperature trace
        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['temperature_2m'],
            name='Temperature (°C)',
            mode='lines+markers',
            yaxis='y1',
            line=dict(color='red')
        ))

        # Humidity trace
        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['relativehumidity_2m'],
            name='Humidity (%)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='blue', dash='dash')
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

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11],
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_temperature_and_humidity(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
