import streamlit as st
import pandas as pd
from src.data.fetcher import fetch_data
from src.features.indicators import (
    add_moving_average, daily_returns, add_bollinger_bands,
    add_rsi, add_macd, add_ema_crossover, get_summary_metrics
)
from src.viz.charts import plot_price, plot_candlestick
import os
import tempfile

st.set_page_config(page_title="Stock Quant Dashboard", layout="wide")

st.title("📊 Stock Quantitative Analysis")
tickers_input = st.text_input("Enter stock tickers (comma-separated):", "AAPL, MSFT")

if st.button("Run Analysis"):
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    summaries = []

    for ticker in tickers:
        try:
            st.subheader(f"📈 {ticker} Analysis")
            df = fetch_data(ticker)
            df = add_moving_average(df)
            df = daily_returns(df)
            df = add_bollinger_bands(df)
            df = add_rsi(df)
            df = add_macd(df)
            df = add_ema_crossover(df)

            # Show interactive charts
            st.pyplot(plot_price(df, ticker))  # Plot inline
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                plot_candlestick(df, ticker, filename=tmpfile.name)
                st.image(tmpfile.name, caption=f"{ticker} Candlestick Chart")

            # Collect summary
            summary = get_summary_metrics(df)
            summary["Ticker"] = ticker
            summaries.append(summary)
        except Exception as e:
            st.error(f"Failed to process {ticker}: {e}")

    if summaries:
        summary_df = pd.DataFrame(summaries)
        st.subheader("📋 Summary Table")
        st.dataframe(summary_df)

        csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Summary", data=csv, file_name="stock_summary.csv", mime="text/csv")
