import pandas as pd
import plotly.express as px

def plot_wind_speed(hourly_df):
    """
    Returns a Plotly line plot of hourly wind speed.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty and 'windspeed_10m' in hourly_df:
        fig = px.line(
            hourly_df,
            x='time',
            y='windspeed_10m',
            title="Hourly Wind Speed Forecast",
            labels={"time": "Time (Hourly)", "windspeed_10m": "Wind Speed (km/h)"},
        )
        fig.update_traces(mode='lines+markers', line=dict(color='teal'))
        fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'windspeed_10m': [10, 15, 12]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_wind_speed(sample_hourly_df)
    if fig:
        fig.show()
