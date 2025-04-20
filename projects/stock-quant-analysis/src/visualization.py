import matplotlib.pyplot as plt

def plot_price(df, ticker):
    plt.figure(figsize=(12,6))
    plt.plot(df['Close'], label='Close Price')
    if "MA_20" in df.columns:
        plt.plot(df['MA_20'], label='20-Day MA')
    plt.title(f"{ticker} Stock Price")
    plt.legend()
    plt.grid(True)
    plt.show()
