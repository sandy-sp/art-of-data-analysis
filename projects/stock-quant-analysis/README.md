# 📊 Stock Quant Analysis

A modular Streamlit-powered dashboard for performing quantitative stock analysis and making next-day price predictions using machine learning.

---

## 🚀 Features

- 📈 **Technical Analysis**: Moving averages, Bollinger Bands, RSI, MACD, and EMA crossovers
- 🤖 **ML Predictions**: Trained Random Forest model predicts next-day closing price
- 📊 **Charts**: Interactive line charts and candlestick visualizations
- 📋 **Summary Table**: Key metrics and exportable CSV summaries
- 📥 **Download Support**: CSV export for summary stats and prediction comparisons

---

## 🧱 Architecture

```
stock-quant-analysis/
├── app/                  # Streamlit dashboard logic
├── notebooks/            # Jupyter notebook for model training
├── src/                  # Core logic
│   ├── data/             # Data retrieval
│   ├── features/         # Feature engineering
│   ├── model/            # Model load and predict
│   ├── viz/              # Charting utilities
├── tests/                # Unit tests
├── app.py                # Entry point
├── requirements.txt      # Python dependencies
```

---

## 🧪 Usage

### 1. 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### 2. 🚦 Run the app
```bash
streamlit run app.py
```

---

## 🧠 Machine Learning
- Model: `RandomForestRegressor`
- Target: next-day `Close` price
- Features: MA, RSI, MACD, EMA, Bollinger Bands
- Trained using `notebooks/stock_predictor.ipynb`

---

## 🤝 Contributing
Pull requests are welcome. Please open issues to report bugs or suggest enhancements.

---

## 📄 License
MIT License

