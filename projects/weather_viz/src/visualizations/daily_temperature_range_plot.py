import matplotlib.pyplot as plt
import pandas as pd

def plot_daily_temperature_range(daily_df, output_path="reports/visualizations/daily_temperature_range_plot.png"):
    """
    Generates a line plot of daily temperature range (min-max).
    """
    if daily_df is not None and not daily_df.empty:
        plt.figure(figsize=(12, 6))

        # Plot the daily maximum and minimum temperatures
        plt.plot(daily_df['time'], daily_df['temperature_2m_max'], label='Max Temperature', marker='o', linestyle='-', color='red')
        plt.plot(daily_df['time'], daily_df['temperature_2m_min'], label='Min Temperature', marker='o', linestyle='-', color='blue')

        # Add labels and title
        plt.xlabel("Time (Daily)")
        plt.ylabel("Temperature (°C)")
        plt.title("Daily Temperature Range")
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.legend()  # Show the legend to distinguish max and min
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        print(f"Daily temperature range plot saved to: {output_path}")
    else:
        print("No daily temperature range data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04', '2025-04-05', '2025-04-06']),
        'temperature_2m_max': [15, 18, 16],
        'temperature_2m_min': [5, 7, 6]
    }
    sample_daily_df = pd.DataFrame(data)
    plot_daily_temperature_range(sample_daily_df)