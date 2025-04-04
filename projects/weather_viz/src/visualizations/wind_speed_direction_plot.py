import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_wind_speed_and_direction(hourly_df, output_path="reports/visualizations/wind_speed_direction_plot.png"):
    """
    Generates a plot combining hourly wind speed and direction using vectors.
    """
    if hourly_df is not None and not hourly_df.empty and 'windspeed_10m' in hourly_df and 'winddirection_10m' in hourly_df:
        plt.figure(figsize=(12, 6))

        # Convert wind direction from degrees to radians
        wind_direction_radians = np.radians(hourly_df['winddirection_10m'])

        # Create x and y components of the wind vectors
        u = hourly_df['windspeed_10m'] * np.cos(wind_direction_radians)
        v = hourly_df['windspeed_10m'] * np.sin(wind_direction_radians)

        # Plot the wind vectors using quiver
        plt.quiver(hourly_df['time'], np.zeros(len(hourly_df)), u, v,
                   scale=50,  # Adjust scale as needed to control vector size
                   angles='xy',  # Use 'xy' for plotting wind vectors correctly
                   width=0.003,  # Adjust width for vector thickness
                   headwidth=3,   # Adjust headwidth for vector head size
                   headlength=5)  # Adjust headlength for vector head size

        # Add labels and title
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Wind Speed and Direction")
        plt.title("Hourly Wind Speed and Direction")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        print(f"Wind speed and direction plot saved to: {output_path}")
    else:
        print("Insufficient data to plot wind speed and direction.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'windspeed_10m': [5, 10, 8],
        'winddirection_10m': [0, 90, 180]  # N, E, S
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_wind_speed_and_direction(sample_hourly_df)