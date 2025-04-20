# 📊 Stock Quant Analysis

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular Python project for **quantitative stock analysis and forecasting**, combining:
- 📈 Technical analysis with indicators
- 🤖 Machine learning for next-day price prediction
- 🌐 Streamlit UI for exploration
- 💻 CLI for automated batch processing
- 📓 Papermill-backed model training notebooks

---

## 🧱 Project Structure

```
stock-quant-analysis/
├── app/                  # Streamlit dashboard UI
├── src/                 
│   ├── data/             # Data fetching (yfinance)
│   ├── features/         # Feature engineering (MA, RSI, etc.)
│   ├── model/            # Model loading & prediction
│   ├── viz/              # Charting utilities
│   ├── notebooks/        # Papermill-compatible notebooks
│   ├── train/            # CLI-based model training
│   └── main.py           # CLI tool entry point
├── tests/                # Unit tests (planned)
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
└── app.py                # Streamlit launcher
```

---

## 🚀 Features

- 📉 **Technical Indicators**: MA, EMA, RSI, MACD, Bollinger Bands
- 🧠 **ML Forecasting**: Predicts next-day closing price using Random Forest
- 📊 **Visualizations**: Multi-panel indicators, candlestick, prediction chart
- 📤 **Exports**: PNG charts & CSV summaries by ticker + datetime
- 🧪 **Automated Training**: Notebook execution via Papermill

---

## 🧪 Usage

### 1. ⚙️ Environment Setup

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
```

Or use Conda:
```bash
conda create -n stock-quant python=3.9
conda activate stock-quant
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

### 2. 📊 Run Streamlit Dashboard
```bash
streamlit run app.py
```

### 3. 🖥️ Run CLI Tool for Batch Analysis
```bash
python src/main.py
```
You'll be prompted to enter one or more stock tickers. This will:
- Train models if not already trained
- Generate plots & predictions
- Save results under `generated_reports/TICKER_TIMESTAMP/`

---

## 🧠 Machine Learning

- Model: `RandomForestRegressor`
- Features: MA(20), RSI(14), MACD, EMA(9/21), Bollinger Bands
- Target: Next-day `Close` price
- Trained using: `src/notebooks/stock_predictor_papermill.ipynb`

---

## 📤 Sample Output Structure
```
generated_reports/
└── AAPL_20250420_150212/
    ├── price.png
    ├── candlestick.png
    ├── actual_vs_predicted.png
    └── summary.csv
```

---

## 📓 Notebooks

Training is fully automated via:
```bash
src/notebooks/stock_predictor_papermill.ipynb
```
Run by both the dashboard and CLI pipeline using `papermill`.

---

## 🤝 Contributing

Contributions welcome via issues or pull requests. Ideas:
- Add more indicators
- Try other models (XGBoost, LSTM)
- Improve visualizations or caching

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

