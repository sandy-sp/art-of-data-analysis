def add_moving_average(df, window=20):
    df[f"MA_{window}"] = df['Close'].rolling(window=window).mean()
    return df

def daily_returns(df):
    df["Daily Return"] = df["Close"].pct_change()
    return df

def add_bollinger_bands(df, window=20, num_std=2):
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    df['BB_Upper'] = rolling_mean + (rolling_std * num_std)
    df['BB_Lower'] = rolling_mean - (rolling_std * num_std)
    return df

def add_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def add_macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['EMA_fast'] = df['Close'].ewm(span=fast_period, adjust=False).mean()
    df['EMA_slow'] = df['Close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    return df

def add_ema_crossover(df, short_window=9, long_window=21):
    df[f'EMA_{short_window}'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df[f'EMA_{long_window}'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    return df

