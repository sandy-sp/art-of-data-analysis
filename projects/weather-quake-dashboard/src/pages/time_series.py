import streamlit as st
from src.api.open_meteo_api import fetch_historical_weather
from src.api.usgs_earthquake_api import fetch_earthquake_data
from src.utils.visualization import plot_temperature_humidity, plot_earthquake_frequency


def display_timeseries(user_inputs):
    st.subheader("📈 Time Series Plots")

    with st.spinner("Loading weather and earthquake data..."):
        hourly_df, _ = fetch_historical_weather(
            user_inputs['latitude'],
            user_inputs['longitude'],
            str(user_inputs['start_date']),
            str(user_inputs['end_date'])
        )

        quake_df = fetch_earthquake_data(
            starttime=str(user_inputs['start_date']),
            endtime=str(user_inputs['end_date']),
            min_magnitude=user_inputs['min_magnitude'],
            latitude=user_inputs['latitude'],
            longitude=user_inputs['longitude'],
            limit=user_inputs['limit']
        )

    if hourly_df.empty:
        st.warning("No weather data available for the selected location and time range.")
    if quake_df.empty:
        st.warning("No earthquake data available for the selected location and time range.")

    st.markdown("### 🌡️ Temperature and Humidity")
    fig1 = plot_temperature_humidity(hourly_df)
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No data to plot temperature and humidity.")

    st.markdown("### 🌋 Earthquake Frequency")
    fig2 = plot_earthquake_frequency(quake_df)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data to plot earthquake frequency.")
