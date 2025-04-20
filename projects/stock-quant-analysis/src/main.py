import os
import pandas as pd
import subprocess
from datetime import datetime
from src.data.fetcher import fetch_data
from src.features.indicators import (
    add_moving_average, daily_returns, add_bollinger_bands,
    add_rsi, add_macd, add_ema_crossover, get_summary_metrics
)
from src.model.predictor import load_model, prepare_features
from src.viz.charts import plot_price, plot_candlestick
from plotly.graph_objs import Scatter, Figure


def process_ticker(ticker):
    # Train model for ticker
    subprocess.run(["python", "src/train/train_model.py", ticker], check=True)

    # Prepare data
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_ema_crossover(df)
    df.dropna(inplace=True)

    # Output folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"generated_reports/{ticker}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Save charts
    fig_price = plot_price(df, ticker)
    fig_price.write_image(f"{output_dir}/price.png")

    plot_candlestick(df, ticker, filename=f"{output_dir}/candlestick.png")

    model = load_model(ticker)
    X = prepare_features(df)
    preds = model.predict(X[-30:])

    pred_df = df[["Close"]].iloc[-30:].copy()
    pred_df["Predicted"] = preds

    fig_pred = Figure(data=[
        Scatter(x=pred_df.index, y=pred_df['Close'], name='Actual'),
        Scatter(x=pred_df.index, y=pred_df['Predicted'], name='Predicted')
    ])
    fig_pred.update_layout(title=f"{ticker} - Actual vs Predicted")
    fig_pred.write_image(f"{output_dir}/actual_vs_predicted.png")

    # Save summary CSV
    summary = get_summary_metrics(df)
    summary["Ticker"] = ticker
    pd.DataFrame([summary]).to_csv(f"{output_dir}/summary.csv", index=False)

    print(f"✅ Output saved to {output_dir}")


def run():
    user_input = input("📥 Enter one or more stock tickers (comma-separated): ")
    tickers = [t.strip().upper() for t in user_input.split(",") if t.strip()]
    if not tickers:
        print("⚠️ No tickers provided. Exiting.")
        return

    for ticker in tickers:
        try:
            print(f"🔍 Processing {ticker}...")
            process_ticker(ticker)
        except Exception as e:
            print(f"❌ Failed to process {ticker}: {e}")


if __name__ == "__main__":
    run()
