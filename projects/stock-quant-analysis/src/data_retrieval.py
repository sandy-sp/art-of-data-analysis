import yfinance as yf

def fetch_data(ticker, period="1y", interval="1d"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)
