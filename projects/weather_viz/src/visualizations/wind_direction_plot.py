import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot_wind_direction_rose(hourly_df):
    """
    Returns a Plotly wind rose (Barpolar) showing frequency of wind directions.
    Suitable for use in Streamlit with st.plotly_chart().
    """
    if hourly_df is not None and not hourly_df.empty:
        if 'winddirection_10m' not in hourly_df:
            return None

        # Bin wind directions into compass sectors
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        bins = np.linspace(0, 360, len(directions)+1)

        wind_dirs = hourly_df['winddirection_10m'].dropna().values
        counts, _ = np.histogram(wind_dirs, bins=bins)

        fig = go.Figure(go.Barpolar(
            r=counts,
            theta=[(bins[i] + bins[i+1])/2 for i in range(len(directions))],
            width=[22.5] * len(directions),
            marker_color='rgba(0,123,255,0.7)',
            marker_line_color='black',
            marker_line_width=1,
            opacity=0.8,
        ))

        fig.update_layout(
            title="Hourly Wind Direction Rose",
            polar=dict(
                angularaxis=dict(
                    direction="clockwise",
                    rotation=90,
                    tickmode="array",
                    tickvals=np.arange(0, 360, 45),
                    ticktext=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                )
            ),
            template="plotly_white",
            margin=dict(t=60, b=40)
        )

        return fig
    else:
        return None

# Optional standalone test
if __name__ == "__main__":
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00', '2025-04-04T03:00']),
        'winddirection_10m': [0, 90, 180, 270],
        'windspeed_10m': [5, 10, 8, 12]
    }
    sample_hourly_df = pd.DataFrame(data)
    fig = plot_wind_direction_rose(sample_hourly_df)
    if fig:
        fig.show()
