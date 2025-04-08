import pandas as pd
import plotly.express as px

def plot_feels_like_temperature(hourly_df):
    """
    Returns a Plotly line plot of hourly "feels like" temperature (heat index).
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty and 'feels_like_temperature_2m' in hourly_df:
        fig = px.line(
            hourly_df,
            x='time',
            y='feels_like_temperature_2m',
            title="Hourly Feels Like Temperature Forecast",
            labels={"time": "Time (Hourly)", "feels_like_temperature_2m": "Feels Like Temperature (°C)"},
        )
        fig.update_traces(mode='lines+markers', line=dict(color='purple'))
        fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'feels_like_temperature_2m': [15, 17, 16]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_feels_like_temperature(sample_hourly_df)
    if fig:
        fig.show()
