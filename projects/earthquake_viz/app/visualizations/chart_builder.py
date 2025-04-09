import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Optional: Use Streamlit-friendly theming
sns.set(style="whitegrid")

def create_magnitude_histogram(df: pd.DataFrame):
    """Plots a histogram of earthquake magnitudes."""
    if "Magnitude" not in df.columns or df["Magnitude"].dropna().empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["Magnitude"].dropna(), bins=20, kde=False, color="skyblue", ax=ax)
    ax.set_title("Earthquake Magnitude Distribution")
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Number of Events")
    return fig

def create_depth_histogram(df: pd.DataFrame):
    """Plots a histogram of earthquake depths."""
    if "Depth (km)" not in df.columns or df["Depth (km)"].dropna().empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["Depth (km)"].dropna(), bins=20, kde=False, color="salmon", ax=ax)
    ax.set_title("Earthquake Depth Distribution")
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Number of Events")
    return fig

def create_time_series(df: pd.DataFrame):
    """Plots a time series of earthquakes per day."""
    if "Time" not in df.columns:
        return None

    # Convert to datetime (if possible)
    try:
        df["Parsed_Time"] = pd.to_datetime(df["Time"], errors="coerce")
        df["Date"] = df["Parsed_Time"].dt.date
        daily_counts = df.groupby("Date").size()
    except Exception:
        return None

    if daily_counts.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 4))
    daily_counts.plot(kind="bar", ax=ax, color="mediumseagreen")
    ax.set_title("Earthquakes Per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Events")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig
