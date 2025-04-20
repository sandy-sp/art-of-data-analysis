import os
import sys
import papermill as pm

def run_training(ticker):
    ticker = ticker.upper()

    # Define artifact paths
    notebook_path = "src/notebooks/stock_predictor_papermill.ipynb"
    output_notebook = f"artifacts/notebooks/output_{ticker}.ipynb"
    model_path = f"artifacts/models/trained_model_{ticker}.pkl"

    # Ensure directories exist
    os.makedirs("artifacts/notebooks", exist_ok=True)
    os.makedirs("artifacts/models", exist_ok=True)

    # Run Papermill
    print(f"🚀 Running training for {ticker}...")
    pm.execute_notebook(
        notebook_path,
        output_notebook,
        parameters={"ticker": ticker}
    )
    print(f"✅ Notebook saved: {output_notebook}")
    print(f"📦 Model expected at: {model_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a stock ticker (e.g., python train_model.py AAPL)")
        sys.exit(1)

    run_training(sys.argv[1])
