import pandas as pd
import plotly.graph_objects as go

def plot_temperature_and_humidity(hourly_df):
    """
    Returns a Plotly figure combining hourly temperature and relative humidity with dual y-axes.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if (
        hourly_df is not None and not hourly_df.empty and
        'temperature_2m' in hourly_df and 'relativehumidity_2m' in hourly_df
    ):
        fig = go.Figure()

        # Add temperature trace
        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['temperature_2m'],
            name='Temperature (°C)',
            mode='lines+markers',
            yaxis='y1',
            line=dict(color='red')
        ))

        # Add humidity trace on secondary y-axis
        fig.add_trace(go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['relativehumidity_2m'],
            name='Humidity (%)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='blue', dash='dash')
        ))

        # Set up layout with dual y-axes
        fig.update_layout(
            title="Hourly Temperature and Relative Humidity",
            xaxis=dict(title="Time (Hourly)", tickangle=-45),
            yaxis=dict(title="Temperature (°C)", titlefont=dict(color="red"), tickfont=dict(color="red")),
            yaxis2=dict(
                title="Relative Humidity (%)",
                overlaying='y',
                side='right',
                titlefont=dict(color="blue"),
                tickfont=dict(color="blue")
            ),
            legend=dict(x=0.01, y=1.05, orientation='h'),
            template="plotly_white",
            margin=dict(t=60, b=40)
        )

        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11],
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_temperature_and_humidity(sample_hourly_df)
    if fig:
        fig.show()
