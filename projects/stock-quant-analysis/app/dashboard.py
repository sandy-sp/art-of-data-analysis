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
from src.model.predictor import load_model, prepare_features  # Added import

def main():
    st.set_page_config(page_title="Stock Quant Dashboard", layout="wide")

    st.title("📊 Stock Quantitative Analysis")
    st.markdown("💡 Tip: For best viewing, switch to wide layout or dark mode in settings (⚙️ top-right)")

    tickers_input = st.text_input(
        "Enter stock tickers",
        placeholder="e.g. AAPL, TSLA, MSFT",
        help="Separate multiple tickers with commas (no spaces)"
    )

    tab1, tab2, tab3 = st.tabs([
        "📈 Technical Analysis",
        "🤖 ML Predictions",
        "📋 Summary & Export"
    ])

    with tab1:
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

                    fig = plot_price(df, ticker)
                    st.pyplot(fig)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                        plot_candlestick(df, ticker, filename=tmpfile.name)
                        st.image(tmpfile.name, caption=f"{ticker} Candlestick Chart")

                    summary = get_summary_metrics(df)
                    summary["Ticker"] = ticker
                    summaries.append(summary)
                except Exception as e:
                    st.error(f"Failed to process {ticker}: {e}")

            if summaries:
                summary_df = pd.DataFrame(summaries)
                st.session_state["summary_df"] = summary_df  # store in session for reuse
                st.subheader("📋 Summary Table")
                st.dataframe(summary_df)

    with tab2:
        st.subheader("📉 Predict Next-Day Close")
        pred_ticker = st.text_input(
            "Enter stock ticker for prediction",
            placeholder="e.g. AAPL",
            help="Only one ticker at a time"
        )

        if st.button("Predict"):
            try:
                model = load_model()
                df = fetch_data(pred_ticker)
                df = add_moving_average(df)
                df = add_bollinger_bands(df)
                df = add_rsi(df)
                df = add_macd(df)
                df = add_ema_crossover(df)
                df.dropna(inplace=True)

                X = prepare_features(df)
                X_test = X.iloc[-30:]
                preds = model.predict(X_test)

                st.metric(label="📊 Predicted Next Close", value=f"${preds[-1]:.2f}", delta="vs last close")

                pred_df = df[["Close"]].iloc[-30:].copy()
                pred_df["Predicted"] = preds
                st.subheader("📊 Actual vs Predicted")
                st.line_chart(pred_df)

                pred_csv = pred_df.reset_index().to_csv(index=False).encode("utf-8")
                st.download_button("📅 Download Predictions CSV", data=pred_csv, file_name=f"{pred_ticker}_predictions.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

    with tab3:
        if "summary_df" in st.session_state:
            st.subheader("📋 Export Summary")
            st.dataframe(st.session_state["summary_df"])

            csv = st.session_state["summary_df"].to_csv(index=False).encode('utf-8')
            st.download_button("📅 Download CSV Summary", data=csv, file_name="stock_summary.csv", mime="text/csv")
        else:
            st.info("Run analysis first to see summary table here.")

if __name__ == "__main__":
    main()
