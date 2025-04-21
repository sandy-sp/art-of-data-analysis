from darts.models import TransformerModel
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
import os
import joblib

def load_model(ticker):
    model_path = f"artifacts/models/transformer_{ticker}.pt"
    scaler_path = f"artifacts/models/scaler_{ticker}.pkl"
    model = TransformerModel.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def prepare_series(df):
    return TimeSeries.from_dataframe(df.reset_index(), time_col="Date", value_cols="Close")
