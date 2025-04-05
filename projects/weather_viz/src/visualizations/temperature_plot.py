import matplotlib.pyplot as plt
import pandas as pd

def plot_hourly_temperature(hourly_df, output_path="reports/visualizations/hourly_temperature.png"):
    """Generates a line plot of hourly temperature."""
    if hourly_df is not None and not hourly_df.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(hourly_df['time'], hourly_df['temperature_2m'], marker='o', linestyle='-', linewidth=2)
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Temperature (°C)")
        plt.title("Hourly Temperature Forecast")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path) # Save the plot to the specified path
        plt.close() # Close the plot to free up memory
        print(f"Hourly temperature plot saved to: {output_path}")
    else:
        print("No hourly temperature data to plot.")

if __name__ == "__main__":
    # This is a sample usage for testing (replace with actual data if needed)
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_hourly_temperature(sample_hourly_df)