import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

# --- Output Directory ---
OUTPUT_DIR = "temp_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Core Animation Helper ---
def get_dynamic_frames(data_len, max_frames=60):
    step = max(1, data_len // max_frames)
    frames = list(range(0, data_len, step))
    interval = max(50, 10000 // len(frames))  # ms/frame, ~10 sec total
    return frames, interval

# --- Magnitude Histogram ---
def create_magnitude_histogram_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/magnitude.gif"):
    df = df.dropna(subset=["Magnitude"])
    mags = df["Magnitude"].sort_values().values
    frames, interval = get_dynamic_frames(len(mags))

    fig, ax = plt.subplots()
    bins = range(0, 11)

    def update(i):
        ax.clear()
        ax.hist(mags[:i+1], bins=bins, color='skyblue', edgecolor='black')
        ax.set_title("Earthquake Magnitude Histogram")
        ax.set_xlabel("Magnitude")
        ax.set_ylabel("Count")
        ax.set_xlim(0, 10)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

# --- Depth Histogram ---
def create_depth_histogram_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/depth.gif"):
    df = df.dropna(subset=["Depth (km)"])
    depths = df["Depth (km)"].sort_values().values
    frames, interval = get_dynamic_frames(len(depths))

    fig, ax = plt.subplots()
    bins = range(0, 700, 50)

    def update(i):
        ax.clear()
        ax.hist(depths[:i+1], bins=bins, color='salmon', edgecolor='black')
        ax.set_title("Earthquake Depth Histogram")
        ax.set_xlabel("Depth (km)")
        ax.set_ylabel("Count")
        ax.set_xlim(0, 700)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

# --- Time Series ---
def create_time_series_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/timeseries.gif"):
    if "Time" not in df.columns:
        return None

    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"])
    df["Date"] = df["Parsed_Time"].dt.date
    daily_counts = df.groupby("Date").size().sort_index()

    if daily_counts.empty:
        return None

    dates = daily_counts.index
    values = daily_counts.values
    frames, interval = get_dynamic_frames(len(dates))

    fig, ax = plt.subplots()

    def update(i):
        ax.clear()
        ax.bar(dates[:i+1], values[:i+1], color='mediumseagreen')
        ax.set_title("Earthquakes Per Day")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlim(dates[0], dates[-1])
        ax.set_ylim(0, max(values) + 5)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

# --- Location Scatter Plot ---
def create_location_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/locations.gif"):
    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        return None

    df = df.dropna(subset=["Latitude", "Longitude"])
    frames, interval = get_dynamic_frames(len(df))

    fig, ax = plt.subplots()
    lat_range = (df["Latitude"].min() - 5, df["Latitude"].max() + 5)
    lon_range = (df["Longitude"].min() - 5, df["Longitude"].max() + 5)

    def update(i):
        ax.clear()
        ax.set_title("Earthquake Locations")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim(*lon_range)
        ax.set_ylim(*lat_range)
        ax.scatter(df["Longitude"][:i+1], df["Latitude"][:i+1], color='orange', alpha=0.6)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_cumulative_time_series(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/cumulative_timeseries.gif", max_frames=60):
    """Creates an animated cumulative time series chart of earthquakes per day."""
    if "Time" not in df.columns:
        return None

    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"])
    df["Date"] = df["Parsed_Time"].dt.date
    daily_counts = df.groupby("Date").size().sort_index().cumsum()

    dates = daily_counts.index
    values = daily_counts.values

    total = len(dates)
    step = max(1, total // max_frames)
    frames = list(range(0, total, step))
    interval = max(50, 10000 // len(frames))  # Total ~10 sec

    fig, ax = plt.subplots(figsize=(10, 4))

    def update(i):
        ax.clear()
        ax.plot(dates[:i+1], values[:i+1], color='dodgerblue', marker='o')
        ax.set_title("Cumulative Earthquakes Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Earthquakes")
        ax.set_ylim(0, max(values) + 5)
        ax.set_xlim(dates[0], dates[-1])
        ax.tick_params(axis='x', rotation=45)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_magnitude_depth_scatter(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/magnitude_vs_depth.gif", max_frames=60):
    """Creates an animated scatter plot of Magnitude vs. Depth."""
    df = df.dropna(subset=["Magnitude", "Depth (km)"])
    df = df.sort_values("Magnitude")  # Optional: order by magnitude

    x = df["Magnitude"].values
    y = df["Depth (km)"].values

    total = len(x)
    step = max(1, total // max_frames)
    frames = list(range(0, total, step))
    interval = max(50, 10000 // len(frames))  # ms per frame

    fig, ax = plt.subplots(figsize=(8, 5))

    def update(i):
        ax.clear()
        ax.scatter(x[:i+1], y[:i+1], color='crimson', alpha=0.6, edgecolors='black')
        ax.set_title("Magnitude vs. Depth")
        ax.set_xlabel("Magnitude")
        ax.set_ylabel("Depth (km)")
        ax.set_xlim(0, 10)
        ax.set_ylim(max(y) + 10, 0)  # Invert Y to show shallow at top
        ax.grid(True)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

