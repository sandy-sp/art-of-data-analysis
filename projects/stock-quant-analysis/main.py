from src.data_retrieval import fetch_data
from src.visualization import plot_price
from src.analysis import (
    add_moving_average, daily_returns, add_bollinger_bands, add_rsi,
    add_macd, add_ema_crossover
)

def run():
    ticker = "AAPL"
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    df = add_bollinger_bands(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_ema_crossover(df)
    plot_price(df, ticker)

if __name__ == "__main__":
    run()
