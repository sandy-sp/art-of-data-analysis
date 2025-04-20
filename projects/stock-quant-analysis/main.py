from src.data_retrieval import fetch_data
from src.visualization import plot_price
from src.analysis import (
    add_moving_average, daily_returns, add_bollinger_bands, add_rsi
)

def run():
    ticker = "AAPL"
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    plot_price(df, ticker)

if __name__ == "__main__":
    run()
