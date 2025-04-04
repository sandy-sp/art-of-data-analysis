import matplotlib.pyplot as plt
import pandas as pd

def plot_precipitation(hourly_df, output_path="reports/visualizations/precipitation_plot.png"):
    """Generates a bar chart of hourly precipitation."""
    if hourly_df is not None and not hourly_df.empty:
        plt.figure(figsize=(12, 6))
        plt.bar(hourly_df['time'], hourly_df['precipitation'], width=0.03) # Adjust width as needed
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Precipitation (mm)")
        plt.title("Hourly Precipitation Forecast")
        plt.grid(axis='y')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"Hourly precipitation plot saved to: {output_path}")
    else:
        print("No hourly precipitation data to plot.")

if __name__ == "__main__":
    # Sample usage for testing
    data = {
        'time': pd.to_datetime(['2025-04-04T00:00', '2025-04-04T01:00', '2025-04-04T02:00']),
        'precipitation': [0.0, 1.5, 0.2]
    }
    sample_hourly_df = pd.DataFrame(data)
    plot_precipitation(sample_hourly_df)