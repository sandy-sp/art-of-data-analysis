import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_temperature_humidity(hourly_df: pd.DataFrame):
    if hourly_df.empty or 'temperature_2m' not in hourly_df or 'relativehumidity_2m' not in hourly_df:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_df['time'],
        y=hourly_df['temperature_2m'],
        name='Temperature (°C)',
        mode='lines+markers',
        line=dict(color='red')
    ))
    fig.add_trace(go.Scatter(
        x=hourly_df['time'],
        y=hourly_df['relativehumidity_2m'],
        name='Humidity (%)',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='blue', dash='dot')
    ))
    fig.update_layout(
        title='Hourly Temperature and Humidity',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Temperature (°C)', color='red'),
        yaxis2=dict(title='Humidity (%)', overlaying='y', side='right', color='blue'),
        legend=dict(x=0.01, y=1.1, orientation='h')
    )
    return fig

def plot_earthquake_frequency(df: pd.DataFrame):
    if df.empty or 'Time' not in df:
        return None

    df['Time'] = pd.to_datetime(df['Time'])
    df['Date'] = df['Time'].dt.date
    count_by_date = df.groupby('Date').size().reset_index(name='Quakes')

    fig = px.bar(
        count_by_date,
        x='Date',
        y='Quakes',
        title='Daily Earthquake Frequency',
        labels={'Quakes': 'Earthquake Count'}
    )
    return fig

def plot_magnitude_vs_weather(joined_df: pd.DataFrame):
    if joined_df.empty or 'temperature_2m' not in joined_df or 'Magnitude' not in joined_df or 'relativehumidity_2m' not in joined_df:
        return None

    fig = px.scatter(
        joined_df,
        x='temperature_2m',
        y='Magnitude',
        color='relativehumidity_2m',
        title='Magnitude vs. Temperature (colored by Humidity)',
        labels={
            'temperature_2m': 'Temperature (°C)',
            'Magnitude': 'Earthquake Magnitude',
            'relativehumidity_2m': 'Humidity (%)'
        },
        hover_data=['Place']
    )
    return fig

def plot_magnitude_histogram(df: pd.DataFrame):
    if df.empty or 'Magnitude' not in df:
        return None

    fig = px.histogram(
        df,
        x='Magnitude',
        nbins=20,
        title='Distribution of Earthquake Magnitudes',
        labels={'Magnitude': 'Magnitude'},
        opacity=0.75
    )
    fig.update_layout(bargap=0.1)
    return fig

def plot_3d_quake_depth(df: pd.DataFrame):
    if df.empty or not all(col in df.columns for col in ['Latitude', 'Longitude', 'Depth_km', 'Magnitude']):
        return None

    fig = px.scatter_3d(
        df,
        x='Longitude',
        y='Latitude',
        z='Depth_km',
        color='Magnitude',
        title='3D View of Earthquake Depths',
        labels={
            'Depth_km': 'Depth (km)',
            'Latitude': 'Latitude',
            'Longitude': 'Longitude',
            'Magnitude': 'Magnitude'
        },
        height=600,
    )
    fig.update_traces(marker=dict(size=5, opacity=0.7))
    return fig
