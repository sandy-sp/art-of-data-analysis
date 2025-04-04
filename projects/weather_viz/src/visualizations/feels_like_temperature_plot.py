import matplotlib.pyplot as plt
import pandas as pd

def plot_feels_like_temperature(hourly_df, output_path="reports/visualizations/feels_like_temperature_plot.png"):
    """
    Generates a line plot of hourly "feels like" temperature (heat index).
    """
    if hourly_df is not None and not hourly_df.empty and 'feels_like_temperature_2m' in hourly_df:
        plt.figure(figsize=(12, 6))

        # Plot the hourly "feels like" temperature
        plt.plot(hourly_df['time'], hourly_df['feels_like_temperature_2m'], marker='o', linestyle='-', color='purple')

        # Add labels and title
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Feels Like Temperature (°C)")
        plt.title("Hourly Feels Like Temperature Forecast")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        print(f"Hourly 'feels like' temperature plot saved to: {output_path}")
    else:
        print("No 'feels like' temperature data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'feels_like_temperature_2m': [15, 17, 16]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_feels_like_temperature(sample_hourly_df)