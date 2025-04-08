import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout  # ⬅️ Add this import

def plot_humidity(hourly_df, location=None):
    """
    Returns a Plotly line plot of hourly relative humidity.
    Suitable for use in Streamlit with st.plotly_chart().
    """
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
        fig.update_traces(mode='lines+markers', line=dict(color='green'))

        title = f"Hourly Relative Humidity Forecast for {location}" if location else "Hourly Relative Humidity Forecast"
        return apply_common_layout(fig, title)
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_humidity(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
