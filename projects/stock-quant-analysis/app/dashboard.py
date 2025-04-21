import sys
import types

# Workaround to avoid torch.classes error
class FakeModule(types.ModuleType):
    __path__ = []  # Prevents Streamlit's watcher from scanning it

sys.modules['torch.classes'] = FakeModule('torch.classes')

import streamlit as st
import pandas as pd
from src.data.fetcher import fetch_data
from src.features.indicators import (
    add_moving_average, daily_returns, add_bollinger_bands,
    add_rsi, add_macd, add_ema_crossover, get_summary_metrics
)
from src.viz.charts import plot_price, plot_candlestick
from src.model.predictor import load_model, prepare_series
import os
import shutil
import papermill as pm
from datetime import datetime
from plotly.graph_objs import Scatter, Figure

def main():
    st.set_page_config(page_title="Stock Quant Dashboard", layout="wide")

    st.title("📊 Stock Quantitative Analysis")
    st.markdown(
        "⚠️ **Note**: The data fetched using `yfinance` may be delayed by up to 1–3 days. "
        "This is a known limitation of free Yahoo Finance and reflects delayed market data. "
    )

    if st.button("🔁 Reset"):
        try:
            shutil.rmtree("artifacts")
            st.success("✅ artifacts/ folder deleted.")
        except FileNotFoundError:
            st.info("ℹ️ artifacts/ folder does not exist.")
        except Exception as e:
            st.error(f"❌ Failed to delete artifacts/: {e}")

    tickers_input = st.text_input(
        "Enter stock tickers",
        placeholder="e.g. AAPL, TSLA, MSFT",
        help="Separate multiple tickers with commas (no spaces)"
    )

    tab1, tab2 = st.tabs([
        "📈 Technical Analysis",
        "🤖 ML Predictions"
    ])

    with tab1:
        time_range = st.selectbox(
            "Select time range for analysis",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"],
            index=3,
            help="Defines how much historical data is pulled"
        )
        if st.button("Run Analysis"):
            tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
            summary_data = []
            for ticker in tickers:
                try:
                    st.subheader(f"📈 {ticker} Analysis")
                    df = fetch_data(ticker, period=time_range)
                    df = add_moving_average(df)
                    df = daily_returns(df)
                    df = add_bollinger_bands(df)
                    df = add_rsi(df)
                    df = add_macd(df)
                    df = add_ema_crossover(df)

                    candle_fig = plot_candlestick(df, ticker)
                    st.plotly_chart(candle_fig, use_container_width=True)

                    fig = plot_price(df, ticker)
                    st.plotly_chart(fig, use_container_width=True)

                    metrics = get_summary_metrics(df)
                    summary_data.append({"Ticker": ticker, **metrics})
                except Exception as e:
                    st.error(f"Failed to process {ticker}: {e}")

            if summary_data:
                st.subheader("📋 Summary Table")
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df)

                st.session_state["summary_df"] = summary_df
                csv = summary_df.to_csv(index=False).encode('utf-8')
                st.download_button("📅 Download CSV Summary", data=csv, file_name="stock_summary.csv", mime="text/csv")

    with tab2:
        st.subheader("📉 Predict Next-Day Close")
        if not tickers_input.strip():
            st.warning("Please enter a ticker symbol above first.")
            return

        pred_ticker = tickers_input.strip().split(",")[0].upper()

        if st.button("Predict"):
            try:
                import time

                model_path = f"artifacts/models/transformer_{pred_ticker}.pt"
                if not os.path.exists(model_path):
                    st.info(f"📓 Training model for {pred_ticker}...")

                    os.makedirs("artifacts/notebooks", exist_ok=True)
                    pm.execute_notebook(
                        "src/notebooks/stock_predictor_papermill.ipynb",
                        f"artifacts/notebooks/output_{pred_ticker}.ipynb",
                        parameters={"ticker": pred_ticker}
                    )

                    # Wait until model folder is available
                    timeout = 300  # seconds
                    poll_interval = 5
                    waited = 0
                    while not os.path.exists(model_path) and waited < timeout:
                        time.sleep(poll_interval)
                        waited += poll_interval

                    if not os.path.exists(model_path):
                        st.error(f"❌ Model training for {pred_ticker} timed out.")
                        return

                    st.success("✅ Model trained and ready.")

                model, scaler = load_model(pred_ticker)
                df = fetch_data(pred_ticker)
                df = df.reset_index()
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df = df.dropna(subset=["Date"])
                df["Date"] = df["Date"].dt.tz_localize(None)

                from darts import TimeSeries
                series = TimeSeries.from_dataframe(df, time_col="Date", value_cols="Close", fill_missing_dates=True, freq="D")
                series_scaled = scaler.transform(series)

                forecast = model.predict(n=30)
                forecast_actual = scaler.inverse_transform(forecast)
                actual = series[-30:]

                pred_df = actual.pd_dataframe().copy(deep=True) if hasattr(actual, "pd_dataframe") else actual.to_dataframe().copy(deep=True)
                pred_df["Predicted"] = forecast_actual.values().squeeze()

                st.metric(label="📊 Predicted Next Close", value=f"${forecast_actual.values()[-1][0]:.2f}", delta="vs last close")

                st.subheader("📊 Actual vs Predicted")
                fig = Figure(data=[
                    Scatter(x=pred_df.index, y=pred_df['Close'], name='Actual'),
                    Scatter(x=pred_df.index, y=pred_df['Predicted'], name='Predicted')
                ])
                fig.update_layout(title=f"{pred_ticker} - Actual vs Predicted")
                st.plotly_chart(fig, use_container_width=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{pred_ticker}_predictions_{timestamp}.csv"
                pred_csv = pred_df.reset_index().to_csv(index=False).encode("utf-8")
                st.download_button("📅 Download Predictions CSV", data=pred_csv, file_name=filename, mime="text/csv")

            except Exception as e:
                st.error(f"Prediction failed: {e}")

if __name__ == "__main__":
    main()
