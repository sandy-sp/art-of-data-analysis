import matplotlib.pyplot as plt
import pandas as pd

def plot_wind_speed(hourly_df, output_path="reports/visualizations/wind_plot.png"):
    """Generates a line plot of hourly wind speed."""
    if hourly_df is not None and not hourly_df.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(hourly_df['time'], hourly_df['windspeed_10m'], marker='o', linestyle='-', linewidth=2)
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Wind Speed (km/h)")
        plt.title("Hourly Wind Speed Forecast")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"Hourly wind speed plot saved to: {output_path}")
    else:
        print("No hourly wind speed data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'windspeed_10m': [10, 15, 12]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_wind_speed(sample_hourly_df)