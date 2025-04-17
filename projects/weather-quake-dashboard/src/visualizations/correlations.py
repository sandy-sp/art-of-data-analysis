import streamlit as st
import plotly.express as px
import pandas as pd

def align_weather_quake_data(weather_df, quake_df):
    if weather_df.empty or quake_df.empty:
        return pd.DataFrame()

    weather_df['hour'] = pd.to_datetime(weather_df['time']).dt.floor('h')
    quake_df['hour'] = pd.to_datetime(quake_df['Time']).dt.floor('h')

    merged_df = pd.merge(quake_df, weather_df, on='hour', how='inner')
    return merged_df

def plot_correlation(joined_df):
    if joined_df.empty:
        return None

    fig = px.scatter(
        joined_df,
        x='temperature_2m',
        y='Magnitude',
        color='relativehumidity_2m',
        color_continuous_scale='Viridis',
        title='🔬 Earthquake Magnitude vs Temperature & Humidity',
        labels={
            'temperature_2m': 'Temperature (°C)',
            'Magnitude': 'Earthquake Magnitude',
            'relativehumidity_2m': 'Humidity (%)'
        },
        hover_data=['Place', 'Time']
    )

    fig.update_layout(coloraxis_colorbar=dict(title='Humidity (%)'))
    return fig

def display_correlations(weather_df, quake_df):
    st.subheader("🔍 Correlation Analysis")

    joined_df = align_weather_quake_data(weather_df, quake_df)

    correlation_fig = plot_correlation(joined_df)

    if correlation_fig:
        st.plotly_chart(correlation_fig, use_container_width=True)
    else:
        st.warning("Insufficient overlapping data to generate correlation plot.")
