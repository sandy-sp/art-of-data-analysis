import matplotlib.pyplot as plt
import pandas as pd

def plot_hourly_temperature(hourly_df, output_path="reports/visualizations/hourly_temperature.png"):
    """Generates a line plot of hourly temperature with weather icons."""
    if hourly_df is not None and not hourly_df.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(hourly_df['time'], hourly_df['temperature_2m'], marker='o', linestyle='-', linewidth=2)
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Temperature (°C)")
        plt.title("Hourly Temperature Forecast with Weather Icons")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')

        # Add weather icons to the plot
        if 'weather_icon' in hourly_df:
            for i, row in hourly_df.iterrows():
                plt.annotate(row['weather_icon'],
                             xy=(row['time'], row['temperature_2m']),
                             xytext=(0, 5),  # Offset the icon slightly above the data point
                             textcoords='offset points',
                             ha='center',
                             fontsize=12)  # Adjust fontsize as needed

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"Hourly temperature plot with weather icons saved to: {output_path}")
    else:
        print("No hourly temperature data to plot.")

if __name__ == "__main__":
    # This is a sample usage for testing (replace with actual data if needed)
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11],
        'weather_icon': ["☀️", "☁️", "🌧️"]  # Sample icons
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_hourly_temperature(sample_hourly_df)