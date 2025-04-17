import streamlit as st
from src.utils.visualization import plot_3d_quake_depth


def display_3d_quake_map(data_bundle):
    st.subheader("🌐 3D Earthquake Depth Visualization")

    quake_df = data_bundle["earthquakes"]

    if quake_df.empty:
        st.warning("No earthquake data available to visualize in 3D.")
        return

    fig = plot_3d_quake_depth(quake_df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for 3D plotting. Ensure depth and location data are available.")
