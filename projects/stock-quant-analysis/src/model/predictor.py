import joblib

def load_model(path="src/model/trained_model.pkl"):
    return joblib.load(path)

def prepare_features(df):
    return df[[
        "MA_20", "BB_Upper", "BB_Lower", "RSI",
        "MACD", "MACD_Signal", "EMA_9", "EMA_21"
    ]]
