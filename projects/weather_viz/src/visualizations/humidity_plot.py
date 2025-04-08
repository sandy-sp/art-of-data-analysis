import pandas as pd
import plotly.express as px

def plot_humidity(hourly_df):
    """
    Returns a Plotly line plot of hourly relative humidity.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty and 'relativehumidity_2m' in hourly_df:
        fig = px.line(
            hourly_df,
            x='time',
            y='relativehumidity_2m',
            title="Hourly Relative Humidity Forecast",
            labels={"time": "Time (Hourly)", "relativehumidity_2m": "Relative Humidity (%)"},
        )
        fig.update_traces(mode='lines+markers', line=dict(color='green'))
        fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_humidity(sample_hourly_df)
    if fig:
        fig.show()
