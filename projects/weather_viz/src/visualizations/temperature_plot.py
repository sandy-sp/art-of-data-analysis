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
        fig.update_traces(mode='lines+markers', line=dict(color='orange'))

        title = f"Hourly Temperature Forecast for {location}" if location else "Hourly Temperature Forecast"
        return apply_common_layout(fig, title)
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_hourly_temperature(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
