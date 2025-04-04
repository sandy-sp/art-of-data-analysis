import matplotlib.pyplot as plt
import pandas as pd

def plot_temperature_and_humidity(hourly_df, output_path="reports/visualizations/temperature_humidity_plot.png"):
    """
    Generates a plot combining hourly temperature and relative humidity.
    """
    if hourly_df is not None and not hourly_df.empty and 'temperature_2m' in hourly_df and 'relativehumidity_2m' in hourly_df:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot temperature on the primary y-axis (left)
        color = 'tab:red'
        ax1.plot(hourly_df['time'], hourly_df['temperature_2m'], marker='o', linestyle='-', color=color, label='Temperature')
        ax1.set_xlabel("Time (Hourly)")
        ax1.set_ylabel("Temperature (°C)", color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Create a second y-axis for humidity (right)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.plot(hourly_df['time'], hourly_df['relativehumidity_2m'], marker='o', linestyle='--', color=color, label='Humidity')
        ax2.set_ylabel("Relative Humidity (%)", color=color)  # we already handled the x-label with ax1
        ax2.tick_params(axis='y', labelcolor=color)

        # Add a title and legend
        plt.title("Hourly Temperature and Relative Humidity")
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95)) # Added legend

        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels

        plt.savefig(output_path)
        plt.close()
        print(f"Temperature and humidity plot saved to: {output_path}")
    else:
        print("Insufficient data to plot temperature and humidity.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'temperature_2m': [10, 12, 11],
        'relativehumidity_2m': [60, 65, 70]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_temperature_and_humidity(sample_hourly_df)