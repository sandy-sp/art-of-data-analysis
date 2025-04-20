from src.data_retrieval import fetch_data
from src.analysis import add_moving_average, daily_returns
from src.visualization import plot_price

def run():
    ticker = "AAPL"
    df = fetch_data(ticker)
    df = add_moving_average(df)
    df = daily_returns(df)
    plot_price(df, ticker)

if __name__ == "__main__":
    run()
