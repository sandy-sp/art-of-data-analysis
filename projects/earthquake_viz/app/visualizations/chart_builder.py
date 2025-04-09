import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

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

def create_location_scatter_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/quake_locations.gif", max_frames=60):
    """Creates an animated location scatter map using Latitude and Longitude."""
    df = df.dropna(subset=["Latitude", "Longitude", "Magnitude"])
    df = df.sort_values("Time")  # Ensure chronological order if needed

    lat = df["Latitude"].values
    lon = df["Longitude"].values
    mag = df["Magnitude"].values

    total = len(df)
    step = max(1, total // max_frames)
    frames = list(range(0, total, step))
    interval = max(50, 10000 // len(frames))

    fig, ax = plt.subplots(figsize=(8, 6))

    lat_pad = 2
    lon_pad = 2
    lat_min, lat_max = lat.min() - lat_pad, lat.max() + lat_pad
    lon_min, lon_max = lon.min() - lon_pad, lon.max() + lon_pad

    def update(i):
        ax.clear()
        ax.set_title("Earthquake Locations Over Time")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim(lon_min, lon_max)
        ax.set_ylim(lat_min, lat_max)
        ax.grid(True)

        ax.scatter(lon[:i+1], lat[:i+1], 
                   s=mag[:i+1]**2,  # Magnitude as size
                   c='orange', alpha=0.6, edgecolors='black')

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_spiral_timeline(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/spiral_timeline.gif", max_frames=60):
    """Creates a spiral animation where angle = time, radius = magnitude, color = depth."""
    df = df.dropna(subset=["Time", "Magnitude", "Depth (km)"])
    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"])

    df = df.sort_values("Parsed_Time")
    mag = df["Magnitude"].values
    depth = df["Depth (km)"].values

    # Normalize for spiral
    total = len(df)
    step = max(1, total // max_frames)
    frames = list(range(0, total, step))
    interval = max(50, 10000 // len(frames))

    angles = np.linspace(0, 4 * np.pi, total)  # 2 full spiral turns
    radii = mag * 5  # Stretch radius
    colors = cm.get_cmap("YlOrRd")(mcolors.Normalize(vmin=min(depth), vmax=max(depth))(depth))

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    def update(i):
        ax.clear()
        ax.set_title("Spiral Earthquake Timeline", va='bottom')
        ax.set_rticks([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_facecolor("black")

        ax.scatter(angles[:i+1], radii[:i+1], 
                   c=colors[:i+1], 
                   s=mag[:i+1]**2, 
                   alpha=0.8, edgecolors='white', linewidth=0.5)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_shockwave_map_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/shockwave.gif", max_frames=60):
    """
    Creates an animated shockwave map where each earthquake emits an expanding ripple.
    Circle size is based on magnitude, and it fades out after a few frames.
    """
    import numpy as np

    df = df.dropna(subset=["Latitude", "Longitude", "Magnitude", "Time"])
    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"]).sort_values("Parsed_Time")

    lat = df["Latitude"].values
    lon = df["Longitude"].values
    mag = df["Magnitude"].values
    total = len(df)

    # Limit number of earthquakes shown if needed
    step = max(1, total // max_frames)
    indices = list(range(0, total, step))
    interval = max(50, 10000 // len(indices))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Shockwave Earthquake Animation")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    lat_margin = 2
    lon_margin = 2
    ax.set_xlim(lon.min() - lon_margin, lon.max() + lon_margin)
    ax.set_ylim(lat.min() - lat_margin, lat.max() + lat_margin)
    ax.grid(True)

    shockwaves = []

    def update(i):
        ax.clear()
        ax.set_title("Shockwave Earthquake Animation")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim(lon.min() - lon_margin, lon.max() + lon_margin)
        ax.set_ylim(lat.min() - lat_margin, lat.max() + lat_margin)
        ax.grid(True)

        # Add the current quake as a new ripple
        shockwaves.append({
            "x": lon[indices[i]],
            "y": lat[indices[i]],
            "mag": mag[indices[i]],
            "radius": 0,
            "alpha": 1.0
        })

        # Animate all active shockwaves
        next_waves = []
        for wave in shockwaves:
            radius = wave["radius"]
            alpha = wave["alpha"]
            if alpha > 0:
                circle = plt.Circle((wave["x"], wave["y"]),
                                    radius=radius,
                                    edgecolor='orange',
                                    facecolor='none',
                                    lw=2,
                                    alpha=alpha)
                ax.add_patch(circle)
                wave["radius"] += wave["mag"] * 0.2  # expand based on magnitude
                wave["alpha"] -= 0.05  # fade out
                next_waves.append(wave)
        shockwaves[:] = next_waves

    ani = animation.FuncAnimation(fig, update, frames=len(indices), interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

def create_depth_strip_chart_animation(df: pd.DataFrame, output_path=f"{OUTPUT_DIR}/depth_strip.gif", max_frames=60):
    """
    Creates an animated horizontal strip chart of earthquakes across depth layers over time.
    Y-axis: Depth category (shallow, intermediate, deep)
    X-axis: Time
    """
    df = df.dropna(subset=["Time", "Depth (km)", "Magnitude"])
    df["Parsed_Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df = df.dropna(subset=["Parsed_Time"]).sort_values("Parsed_Time")

    # Categorize depth
    def categorize_depth(depth):
        if depth < 70:
            return "Shallow (<70km)"
        elif depth < 300:
            return "Intermediate (70–300km)"
        else:
            return "Deep (>300km)"

    df["Depth_Category"] = df["Depth (km)"].apply(categorize_depth)

    categories = ["Shallow (<70km)", "Intermediate (70–300km)", "Deep (>300km)"]
    y_positions = {cat: i for i, cat in enumerate(categories)}

    total = len(df)
    step = max(1, total // max_frames)
    frames = list(range(0, total, step))
    interval = max(50, 10000 // len(frames))

    times = df["Parsed_Time"].values
    magnitudes = df["Magnitude"].values
    categories_seq = df["Depth_Category"].values
    y_vals = [y_positions[c] for c in categories_seq]

    fig, ax = plt.subplots(figsize=(10, 4))

    def update(i):
        ax.clear()
        ax.set_title("Earthquake Depth Strip Over Time")
        ax.set_xlabel("Time")
        ax.set_yticks(list(y_positions.values()))
        ax.set_yticklabels(list(y_positions.keys()))
        ax.set_xlim(times[0], times[-1])
        ax.set_ylim(-0.5, len(categories) - 0.5)
        ax.grid(True, axis='x', linestyle='--', alpha=0.3)

        ax.scatter(times[:i+1], [y_positions[c] for c in categories_seq[:i+1]],
                   s=magnitudes[:i+1]**2,
                   color='purple', alpha=0.6, edgecolors='black')

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, repeat=False)
    ani.save(output_path, writer='pillow')
    plt.close()
    return output_path

