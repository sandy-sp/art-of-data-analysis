import papermill as pm
import sys
import os

def run_training(ticker):
    notebook = "notebooks/stock_predictor_papermill.ipynb"
    output = f"notebooks/output_{ticker}.ipynb"
    
    print(f"🚀 Running training for {ticker}...")
    pm.execute_notebook(
        notebook,
        output,
        parameters={"ticker": ticker}
    )
    print(f"✅ Training complete: {output}")
    print(f"📁 Model saved to: src/model/trained_model_{ticker}.pkl")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a stock ticker (e.g., python train_model.py AAPL)")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    run_training(ticker)
