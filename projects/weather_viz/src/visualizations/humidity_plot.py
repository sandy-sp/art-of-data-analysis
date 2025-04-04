import matplotlib.pyplot as plt
import pandas as pd

def plot_humidity(hourly_df, output_path="reports/visualizations/humidity_plot.png"):
    """
    Generates a line plot of hourly relative humidity.
    """
    if hourly_df is not None and not hourly_df.empty:
        plt.figure(figsize=(12, 6))

        # Plot the hourly relative humidity
        plt.plot(hourly_df['time'], hourly_df['relativehumidity_2m'], marker='o', linestyle='-', color='green')

        # Add labels and title
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Relative Humidity (%)")
        plt.title("Hourly Relative Humidity Forecast")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        print(f"Hourly humidity plot saved to: {output_path}")
    else:
        print("No hourly humidity data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_humidity(sample_hourly_df)