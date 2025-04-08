import pandas as pd
import plotly.express as px
from .plot_utils import apply_common_layout  # ⬅️ Add this import

def plot_precipitation(hourly_df, location=None):
    """
    Returns a Plotly bar chart of hourly precipitation.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'precipitation']
    if (
        hourly_df is not None and 
        not hourly_df.empty and 
        all(col in hourly_df.columns for col in required_cols)
    ):
        fig = px.bar(
            hourly_df,
            x='time',
            y='precipitation',
            labels={"time": "Time (Hourly)", "precipitation": "Precipitation (mm)"}
        )
        fig.update_layout(bargap=0.1)

        title = f"Hourly Precipitation Forecast for {location}" if location else "Hourly Precipitation Forecast"
        return apply_common_layout(fig, title)
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'precipitation': [0.0, 1.5, 0.2]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_precipitation(sample_hourly_df, location="Cleveland, OH")
    if fig:
        fig.show()
