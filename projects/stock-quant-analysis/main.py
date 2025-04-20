from src.data_retrieval import fetch_data
from src.analysis import (
    add_moving_average, daily_returns, add_bollinger_bands, add_rsi,
    add_macd, add_ema_crossover, get_summary_metrics
)
from src.visualization import plot_price, plot_candlestick
import pandas as pd
import os

def process_ticker(ticker):
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_ema_crossover(df)

    os.makedirs("reports/figures", exist_ok=True)

    # Save plots
    plot_price(df, ticker)
    plot_candlestick(df, ticker, filename=f"reports/figures/{ticker}_candlestick.png")

    return get_summary_metrics(df)

def run():
    user_input = input("📥 Enter one or more stock tickers (comma-separated): ")
    tickers = [t.strip().upper() for t in user_input.split(",") if t.strip()]

    if not tickers:
        print("⚠️ No tickers provided. Exiting.")
        return

    all_summaries = []
    for ticker in tickers:
        try:
            print(f"🔍 Processing {ticker}...")
            summary = process_ticker(ticker)
            summary["Ticker"] = ticker
            all_summaries.append(summary)
        except Exception as e:
            print(f"❌ Failed to process {ticker}: {e}")

    if all_summaries:
        summary_df = pd.DataFrame(all_summaries)
        os.makedirs("reports", exist_ok=True)
        summary_df.to_csv("reports/stock_summary.csv", index=False)
        print("✅ Summary CSV saved to: reports/stock_summary.csv")

if __name__ == "__main__":
    run()
