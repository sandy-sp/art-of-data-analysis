import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

OUTPUT_DIR = "temp_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_magnitude_histogram_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/magnitude.gif"):
    df = df.dropna(subset=["Magnitude"])
    mags = df["Magnitude"].sort_values().values
    fig, ax = plt.subplots()
    bins = range(0, 11)

    def update(i):
        ax.clear()
        current = mags[:i + 1]
        ax.hist(current, bins=bins, color='skyblue', edgecolor='black')
        ax.set_title("Earthquake Magnitude Histogram")
        ax.set_xlabel("Magnitude")
        ax.set_ylabel("Count")
        ax.set_xlim(0, 10)

    ani = animation.FuncAnimation(fig, update, frames=len(mags), interval=100, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_depth_histogram_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/depth.gif"):
    df = df.dropna(subset=["Depth (km)"])
    depths = df["Depth (km)"].sort_values().values
    fig, ax = plt.subplots()
    bins = range(0, 700, 50)

    def update(i):
        ax.clear()
        current = depths[:i + 1]
        ax.hist(current, bins=bins, color='salmon', edgecolor='black')
        ax.set_title("Earthquake Depth Histogram")
        ax.set_xlabel("Depth (km)")
        ax.set_ylabel("Count")
        ax.set_xlim(0, 700)

    ani = animation.FuncAnimation(fig, update, frames=len(depths), interval=100, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_time_series_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/timeseries.gif"):
    if "Time" not in df.columns:
        return None

    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"])
    df["Date"] = df["Parsed_Time"].dt.date
    daily_counts = df.groupby("Date").size().sort_index()

    dates = daily_counts.index
    values = daily_counts.values
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

    ani = animation.FuncAnimation(fig, update, frames=len(dates), interval=300, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_location_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/locations.gif"):
    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        return None

    df = df.dropna(subset=["Latitude", "Longitude"])
    fig, ax = plt.subplots()
    ax.set_title("Earthquake Locations")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(df["Longitude"].min() - 5, df["Longitude"].max() + 5)
    ax.set_ylim(df["Latitude"].min() - 5, df["Latitude"].max() + 5)

    def update(i):
        ax.clear()
        ax.set_title("Earthquake Locations")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.scatter(df["Longitude"][:i+1], df["Latitude"][:i+1], color='orange', alpha=0.6)
        ax.set_xlim(df["Longitude"].min() - 5, df["Longitude"].max() + 5)
        ax.set_ylim(df["Latitude"].min() - 5, df["Latitude"].max() + 5)

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=100, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path