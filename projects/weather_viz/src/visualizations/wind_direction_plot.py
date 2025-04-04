import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_wind_direction_rose(hourly_df, output_path="reports/visualizations/wind_direction_rose.png"):
    """
    Generates a wind rose plot from hourly wind direction and wind speed data.
    """
    if hourly_df is not None and not hourly_df.empty:
        # Prepare data for the wind rose
        wind_directions = hourly_df['winddirection_10m'].values
        wind_speeds = hourly_df['windspeed_10m'].values

        # Define bins for wind directions (16 compass points)
        bins = np.arange(-11.25, 360, 22.5)
        counts = np.histogram(wind_directions, bins=bins)[0]

        # Create the wind rose plot
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, polar=True)

        # Plotting the wind rose
        theta = np.radians(bins[:-1])
        width = np.radians(22.5)  # Width of each bin
        bars = ax.bar(theta, counts, width=width, bottom=0.0)

        # Customize the plot
        ax.set_theta_zero_location("N")  # Set North as the starting point
        ax.set_theta_direction(-1)  # Clockwise wind directions
        ax.set_title("Hourly Wind Direction Rose")

        # Set the tick locations and labels explicitly
        ax.set_xticks(np.arange(0, 360, 45))  # Set tick locations
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])  # Set tick labels

        plt.savefig(output_path)
        plt.close()
        print(f"Wind direction rose plot saved to: {output_path}")
    else:
        print("No wind direction data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00', '2025-04-04T03:00']),
        'winddirection_10m': [0, 90, 180, 270],  # N, E, S, W
        'windspeed_10m': [5, 10, 8, 12]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_wind_direction_rose(sample_hourly_df)