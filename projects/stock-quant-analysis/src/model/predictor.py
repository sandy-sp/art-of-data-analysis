import joblib

def load_model(ticker, base_path="src/model"):
    path = f"{base_path}/trained_model_{ticker}.pkl"
    return joblib.load(path)

def prepare_features(df):
    return df[[
        "MA_20", "BB_Upper", "BB_Lower", "RSI",
        "MACD", "MACD_Signal", "EMA_9", "EMA_21"
    ]]
