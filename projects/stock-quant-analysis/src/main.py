import os
import pandas as pd
import subprocess
from datetime import datetime
from src.data.fetcher import fetch_data
from src.features.indicators import (
    add_moving_average, daily_returns, add_bollinger_bands,
    add_rsi, add_macd, add_ema_crossover, get_summary_metrics
)
from src.model.predictor import load_model, prepare_series
from src.viz.charts import plot_price, plot_candlestick
from plotly.graph_objs import Scatter, Figure


def process_ticker(ticker):
    # Train model if needed
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

    # Output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"artifacts/reports/{ticker}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Charts
    fig_price = plot_price(df, ticker)
    fig_price.write_image(f"{output_dir}/price.png")

    plot_candlestick(df, ticker, filename=f"{output_dir}/candlestick.png")

    # Predictions
    model, scaler = load_model(ticker)
    series = prepare_series(df)
    series_scaled = scaler.transform(series)

    forecast = model.predict(n=30)
    forecast_actual = scaler.inverse_transform(forecast)
    actual = series[-30:]

    pred_df = actual.pd_dataframe().copy(deep=True) if hasattr(actual, "pd_dataframe") else actual.to_dataframe().copy(deep=True)
    pred_df["Predicted"] = forecast_actual.values().squeeze()

    fig_pred = Figure(data=[
        Scatter(x=pred_df.index, y=pred_df['Close'], name='Actual'),
        Scatter(x=pred_df.index, y=pred_df['Predicted'], name='Predicted')
    ])
    fig_pred.update_layout(title=f"{ticker} - Actual vs Predicted")
    fig_pred.write_image(f"{output_dir}/actual_vs_predicted.png")

    # Save summary
    summary = get_summary_metrics(df)
    summary["Ticker"] = ticker
    pd.DataFrame([summary]).to_csv(f"{output_dir}/summary.csv", index=False)

    print(f"✅ Reports saved to {output_dir}")


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
