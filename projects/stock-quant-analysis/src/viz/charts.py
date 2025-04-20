import plotly.graph_objs as go
import plotly.subplots as sp

def plot_price(df, ticker):
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                           subplot_titles=(f"{ticker} Price with EMAs & Bollinger Bands", "RSI", "MACD"))

    # Price with EMAs & BB
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='black')), row=1, col=1)
    if 'EMA_9' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_9'], name='EMA 9', line=dict(dash='dash', color='orange')), row=1, col=1)
    if 'EMA_21' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_21'], name='EMA 21', line=dict(dash='dash', color='blue')), row=1, col=1)
    if 'BB_Upper' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='Upper BB', line=dict(dash='dot', color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='Lower BB', line=dict(dash='dot', color='red')), row=1, col=1)

    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')), row=2, col=1)
        fig.add_hline(y=70, line=dict(dash='dash', color='red'), row=2, col=1)
        fig.add_hline(y=30, line=dict(dash='dash', color='green'), row=2, col=1)

    # MACD
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='teal')), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal Line', line=dict(dash='dash', color='magenta')), row=3, col=1)
        fig.add_hline(y=0, line=dict(dash='dash', color='gray'), row=3, col=1)

    fig.update_layout(height=900, width=1000, showlegend=True)
    return fig


def plot_candlestick(df, ticker, filename=None):
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        )
    ])

    fig.update_layout(
        title=f"{ticker} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    if filename:
        fig.write_image(filename)

    return fig
