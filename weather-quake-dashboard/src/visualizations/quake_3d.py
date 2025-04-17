import streamlit as st
import plotly.express as px

def plot_3d_quake(quake_df):
    if quake_df.empty:
        return None
    
    fig = px.scatter_3d(
        quake_df,
        x='Longitude',
        y='Latitude',
        z='Depth_km',
        size='Magnitude',
        color='Magnitude',
        color_continuous_scale='Inferno',
        title='🌐 3D Earthquake Visualization (Depth & Magnitude)',
        labels={
            'Longitude': 'Longitude',
            'Latitude': 'Latitude',
            'Depth_km': 'Depth (km)',
            'Magnitude': 'Magnitude'
        },
        hover_data=['Place', 'Time']
    )

    fig.update_layout(scene=dict(
        zaxis=dict(autorange='reversed')  # Ensures depth is intuitive (surface at top)
    ))

    return fig

def display_3d_quakes(quake_df):
    st.subheader("🌎 3D Earthquake Depth and Magnitude")

    quake_3d_fig = plot_3d_quake(quake_df)
    
    if quake_3d_fig:
        st.plotly_chart(quake_3d_fig, use_container_width=True)
    else:
        st.warning("No earthquake data available for 3D visualization.")
