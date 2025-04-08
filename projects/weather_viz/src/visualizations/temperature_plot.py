import pandas as pd
import plotly.express as px

def plot_hourly_temperature(hourly_df):
    """
    Returns a Plotly line plot of hourly temperature.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty and 'temperature_2m' in hourly_df:
        fig = px.line(
            hourly_df,
            x='time',
            y='temperature_2m',
            title="Hourly Temperature Forecast",
            labels={"time": "Time (Hourly)", "temperature_2m": "Temperature (°C)"},
        )
        fig.update_traces(mode='lines+markers', line=dict(color='orange'))
        fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_hourly_temperature(sample_hourly_df)
    if fig:
        fig.show()
