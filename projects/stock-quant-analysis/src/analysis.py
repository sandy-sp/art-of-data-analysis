def add_moving_average(df, window=20):
    df[f"MA_{window}"] = df['Close'].rolling(window=window).mean()
    return df

def daily_returns(df):
    df["Daily Return"] = df["Close"].pct_change()
    return df
