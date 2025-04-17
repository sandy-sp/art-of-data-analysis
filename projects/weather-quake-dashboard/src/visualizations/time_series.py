import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_weather_trends(weather_df):
    if weather_df.empty:
        return None
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weather_df['time'],
        y=weather_df['temperature_2m'],
        mode='lines+markers',
        name='Temperature (°C)',
        line=dict(color='firebrick')
    ))

    fig.add_trace(go.Scatter(
        x=weather_df['time'],
        y=weather_df['relativehumidity_2m'],
        mode='lines+markers',
        name='Humidity (%)',
        yaxis='y2',
        line=dict(color='royalblue')
    ))

    fig.update_layout(
        title="🌤️ Temperature and Humidity Trends",
        xaxis=dict(title="Date & Time"),
        yaxis=dict(title="Temperature (°C)", color='firebrick'),
        yaxis2=dict(title="Humidity (%)", overlaying='y', side='right', color='royalblue'),
        legend=dict(x=0, y=1.1, orientation='h')
    )

    return fig

def plot_earthquake_frequency(quake_df):
    if quake_df.empty:
        return None
    
    quake_df['Date'] = pd.to_datetime(quake_df['Time']).dt.date
    daily_counts = quake_df.groupby('Date').size().reset_index(name='Earthquake Count')

    fig = px.bar(
        daily_counts,
        x='Date',
        y='Earthquake Count',
        title='🧨 Daily Earthquake Frequency',
        labels={'Earthquake Count': 'Number of Earthquakes'}
    )

    return fig

def display_timeseries(weather_df, quake_df):
    st.subheader("📈 Time Series Analysis")

    weather_fig = plot_weather_trends(weather_df)
    if weather_fig:
        st.plotly_chart(weather_fig, use_container_width=True)
    else:
        st.warning("No weather data available.")

    quake_fig = plot_earthquake_frequency(quake_df)
    if quake_fig:
        st.plotly_chart(quake_fig, use_container_width=True)
    else:
        st.warning("No earthquake data available.")
