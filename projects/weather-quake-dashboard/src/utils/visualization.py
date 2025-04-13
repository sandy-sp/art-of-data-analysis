import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_temperature_humidity(hourly_df: pd.DataFrame):
    if hourly_df.empty:
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
    if df.empty:
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
    if joined_df.empty:
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
