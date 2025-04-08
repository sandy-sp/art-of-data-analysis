import pandas as pd
import plotly.graph_objects as go
from .plot_utils import apply_common_layout 

def plot_daily_temperature_range(daily_df, location=None):
    """
    Returns a Plotly line plot showing daily max and min temperature.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    required_cols = ['time', 'temperature_2m_max', 'temperature_2m_min']
    if (
        daily_df is not None and 
        not daily_df.empty and 
        all(col in daily_df.columns for col in required_cols)
    ):
        fig = go.Figure()

        # Max Temperature trace
        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_max'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='red')
        ))

        # Min Temperature trace
        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_min'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='blue')
        ))

        # Dynamic title
        title = f"Daily Temperature Range Forecast for {location}" if location else "Daily Temperature Range Forecast"
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            legend_title="Legend"
        )

        return apply_common_layout(fig, title)  # Reuse common layout
    return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04', '2025-04-05', '2025-04-06']),
        'temperature_2m_max': [15, 18, 16],
        'temperature_2m_min': [5, 7, 6]
    }
    sample_df = pd.DataFrame(data)
    fig = plot_daily_temperature_range(sample_df, location="Cleveland, OH")
    if fig:
        fig.show()
