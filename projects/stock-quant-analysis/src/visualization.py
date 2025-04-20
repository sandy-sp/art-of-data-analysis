import matplotlib.pyplot as plt

def plot_price(df, ticker):
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # Price + Bollinger Bands
    ax1.plot(df['Close'], label='Close', color='blue')
    if 'MA_20' in df.columns:
        ax1.plot(df['MA_20'], label='20-Day MA', color='orange')
    if 'BB_Upper' in df.columns:
        ax1.plot(df['BB_Upper'], label='Upper BB', linestyle='--', color='green')
    if 'BB_Lower' in df.columns:
        ax1.plot(df['BB_Lower'], label='Lower BB', linestyle='--', color='red')
    ax1.set_title(f"{ticker} Price & Bollinger Bands")
    ax1.legend()
    ax1.grid(True)

    # RSI
    if 'RSI' in df.columns:
        ax2.plot(df['RSI'], label='RSI', color='purple')
        ax2.axhline(70, color='red', linestyle='--')
        ax2.axhline(30, color='green', linestyle='--')
        ax2.set_title('Relative Strength Index (RSI)')
        ax2.legend()
        ax2.grid(True)

    plt.tight_layout()
    plt.show()
