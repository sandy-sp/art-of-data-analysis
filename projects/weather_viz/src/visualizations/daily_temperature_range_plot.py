import pandas as pd
import plotly.graph_objects as go

def plot_daily_temperature_range(daily_df):
    """
    Returns a Plotly line plot showing daily max and min temperature.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if daily_df is not None and not daily_df.empty:
        fig = go.Figure()

        # Add Max Temperature trace
        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_max'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='red')
        ))

        # Add Min Temperature trace
        fig.add_trace(go.Scatter(
            x=daily_df['time'],
            y=daily_df['temperature_2m_min'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='blue')
        ))

        # Update layout
        fig.update_layout(
            title="Daily Temperature Range",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            legend_title="Legend",
            xaxis=dict(tickangle=-45),
            template="plotly_white",
            margin=dict(t=60, b=40)
        )

        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04', '2025-04-05', '2025-04-06']),
        'temperature_2m_max': [15, 18, 16],
        'temperature_2m_min': [5, 7, 6]
    }
    sample_df = pd.DataFrame(data)
    fig = plot_daily_temperature_range(sample_df)
    if fig:
        fig.show()
