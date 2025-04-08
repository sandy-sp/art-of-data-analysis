import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout 

def plot_wind_speed(hourly_df, location=None):
    """
    Returns a Plotly line plot of hourly wind speed.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'windspeed_10m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='windspeed_10m',
            labels={"time": "Time (Hourly)", "windspeed_10m": "Wind Speed (km/h)"}
        )
        fig.update_traces(mode='lines+markers', line=dict(color='teal'))

        title = f"Hourly Wind Speed Forecast for {location}" if location else "Hourly Wind Speed Forecast"
        return apply_common_layout(fig, title)
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'windspeed_10m': [10, 15, 12]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_wind_speed(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
