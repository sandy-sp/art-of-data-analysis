import matplotlib.pyplot as plt
import mplfinance as mpf

def plot_price(df, ticker):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    # Price + EMAs
    ax1.plot(df['Close'], label='Close', color='black')
    if 'EMA_9' in df.columns:
        ax1.plot(df['EMA_9'], label='EMA 9', linestyle='--', color='orange')
    if 'EMA_21' in df.columns:
        ax1.plot(df['EMA_21'], label='EMA 21', linestyle='--', color='blue')
    if 'BB_Upper' in df.columns:
        ax1.plot(df['BB_Upper'], label='Upper BB', linestyle=':', color='green')
        ax1.plot(df['BB_Lower'], label='Lower BB', linestyle=':', color='red')
    ax1.set_title(f"{ticker} Price with EMAs & Bollinger Bands")
    ax1.legend()
    ax1.grid(True)

    # RSI
    if 'RSI' in df.columns:
        ax2.plot(df['RSI'], label='RSI', color='purple')
        ax2.axhline(70, color='red', linestyle='--')
        ax2.axhline(30, color='green', linestyle='--')
        ax2.set_title('RSI')
        ax2.legend()
        ax2.grid(True)

    # MACD
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        ax3.plot(df['MACD'], label='MACD', color='teal')
        ax3.plot(df['MACD_Signal'], label='Signal Line', color='magenta', linestyle='--')
        ax3.axhline(0, color='gray', linestyle='--')
        ax3.set_title('MACD')
        ax3.legend()
        ax3.grid(True)

    plt.tight_layout()
    return fig

def plot_candlestick(df, ticker, filename=None):
    df_candle = df.copy()
    df_candle.index.name = 'Date'
    df_candle = df_candle[['Open', 'High', 'Low', 'Close', 'Volume']]

    mpf.plot(
        df_candle,
        type='candle',
        mav=(9, 21),
        volume=True,
        title=f'{ticker} Candlestick Chart',
        style='yahoo',
        savefig=filename if filename else None
    )
