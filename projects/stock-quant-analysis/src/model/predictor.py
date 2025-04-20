import os
import joblib

def load_model(ticker, base_dir="artifacts/models"):
    path = os.path.join(base_dir, f"trained_model_{ticker}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at: {path}")
    return joblib.load(path)

def prepare_features(df):
    return df[[
        "MA_20", "BB_Upper", "BB_Lower", "RSI",
        "MACD", "MACD_Signal", "EMA_9", "EMA_21"
    ]]
