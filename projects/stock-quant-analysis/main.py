from src.data_retrieval import fetch_data
from src.analysis import (
    add_moving_average, daily_returns, add_bollinger_bands, add_rsi,
    add_macd, add_ema_crossover, get_summary_metrics
)
from src.visualization import plot_price, plot_candlestick
import pandas as pd

def run():
    ticker = "AAPL"
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_ema_crossover(df)

    # Plot + Save
    plot_price(df, ticker)
    plot_candlestick(df, ticker, filename=f"reports/figures/{ticker}_candlestick.png")

    # Summary to CSV
    summary = get_summary_metrics(df)
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(f"reports/{ticker}_summary.csv", index=False)

    print(f"✅ Report exported for {ticker}")


if __name__ == "__main__":
    run()
