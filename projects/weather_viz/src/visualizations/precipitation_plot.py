import pandas as pd
import plotly.express as px

def plot_precipitation(hourly_df):
    """
    Returns a Plotly bar chart of hourly precipitation.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty and 'precipitation' in hourly_df:
        fig = px.bar(
            hourly_df,
            x='time',
            y='precipitation',
            title="Hourly Precipitation Forecast",
            labels={"time": "Time (Hourly)", "precipitation": "Precipitation (mm)"}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            template="plotly_white",
            bargap=0.1
        )
        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'precipitation': [0.0, 1.5, 0.2]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_precipitation(sample_hourly_df)
    if fig:
        fig.show()
