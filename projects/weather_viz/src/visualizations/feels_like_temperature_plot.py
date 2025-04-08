import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout 

def plot_feels_like_temperature(hourly_df, location=None):
    """
    Returns a Plotly line plot of hourly "feels like" temperature (heat index).
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'feels_like_temperature_2m']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.line(
            hourly_df,
            x='time',
            y='feels_like_temperature_2m',
            labels={
                "time": "Time (Hourly)", 
                "feels_like_temperature_2m": "Feels Like Temperature (°C)"
            }
        )
        fig.update_traces(mode='lines+markers', line=dict(color='purple'))

        title = f"Hourly Feels Like Temperature Forecast for {location}" if location else "Hourly Feels Like Temperature Forecast"
        return apply_common_layout(fig, title)
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'feels_like_temperature_2m': [15, 17, 16]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_feels_like_temperature(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
