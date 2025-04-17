import pandas as pd
import plotly.io as pio
import streamlit as st

def export_plotly_to_html(fig, filename):
    pio.write_html(fig, filename)

def export_plotly_to_png(fig, filename):
    fig.write_image(filename)

def export_dataframe_to_excel(df: pd.DataFrame, filename: str):
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return filename
