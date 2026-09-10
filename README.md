# 🛡️ Promise Guard

**AI-powered commitment tracking and risk assessment system** that analyzes corporate promises, pledges, and commitments to extract key details, evaluate sentiment, and predict fulfillment risk.

Promise Guard processes text from press releases, speeches, earnings calls, and corporate documents to identify commitments made by entities, extract deadlines, assess delivery confidence, and flag high-risk promises using machine learning models.

## Stack

- **Language:** Python
- **Framework / Runtime:** Streamlit (interactive dashboard)
- **Notable Libraries:** 
  - pandas – data processing and manipulation
  - plotly – interactive data visualizations
  - scikit-learn – machine learning models (TF-IDF vectorization, Random Forest classification)
  - transformers – sentiment analysis with RoBERTa

## How It's Organized

```
.
├── app.py                              Streamlit dashboard with two modules
├── promise_guard.ipynb                 Jupyter notebook with full pipeline
├── config/                             JSON configuration files
│   ├── extraction_config.json           Patterns for entity, action, deadline extraction
│   ├── sentiment_config.json            RoBERTa sentiment model config
│   ├── risk_model_config.json           Random Forest classifier parameters
│   ├── promise_patterns.json            Promise detection patterns
│   ├── promise_tracking_config.json     Promise tracking thresholds
│   └── pipeline_config.json             End-to-end pipeline settings
├── models/                             Pre-trained ML models (joblib serialized)
│   ├── promise_tfidf_vectorizer.joblib  TF-IDF text vectorizer
│   ├── promise_classifier.joblib        Promise classification model
│   └── promiseguard_risk_model.joblib   Risk prediction model
├── data/                               Processed datasets
│   └── promiseguard_clean.csv           12-month training dataset (~30k records)
└── outputs/                            Generated predictions and reports
```

### How It Fits Together

The system operates as two integrated pipelines:

1. **Neural Engine (Real-time Analysis):** Accepts user text input and runs three processing modes—**[EXTRACT]** to parse entity, commitment, and deadline; **[SENTIMENT]** to score the tone (-1.0 to +1.0) for ambition/hesitancy; and **[RISK]** to flag conditional language and predict delivery feasibility using radar charts and confidence scores.

2. **Global Telemetry (Exploratory Dashboard):** Visualizes historical promise data across entities and categories using treemaps, scatter plots, and timelines. Filters by entity and risk level. Shows metrics like active promises, average confidence, high-risk count, and delayed status.

The text analysis in app.py uses lightweight regex-based NLP for extraction (date patterns, entity detection, commitment rules) and word-list sentiment scoring. The pre-trained models in `/models/` provide more sophisticated classification and risk scoring for batch processing via the Jupyter notebook.

## How to Run It

### Prerequisites
- Python 3.8+
- Required packages: `streamlit`, `pandas`, `plotly`, `scikit-learn`, `transformers`

### Install Dependencies
```bash
pip install streamlit pandas plotly scikit-learn transformers
```

### Run the Streamlit Dashboard
```bash
streamlit run app.py
```

This launches an interactive web interface on `http://localhost:8501` with:
- **[01] NEURAL ENGINE**: Paste text → choose Extract/Sentiment/Risk → Execute to analyze a single commitment
- **[02] GLOBAL TELEMETRY**: Browse pre-loaded dataset with filters and summary charts

### Run the Jupyter Notebook
```bash
jupyter notebook promise_guard.ipynb
```

Explore the full pipeline including data loading, model training, feature engineering, and batch predictions on the dataset in `data/promiseguard_clean.csv`.

## Try Asking

- **How does the sentiment analysis distinguish between ambitious promises and hesitant language?** Look at the `analyze_text()` function in `app.py` (lines 110-159) to see the word lists and scoring logic.
- **What features does the Random Forest risk model use to predict promise fulfillment?** Check `config/risk_model_config.json` for the 10-feature set including account_mrr, broken_promise_rate, and overdue_rate.
- **How can I retrain the models on new corporate data?** The Jupyter notebook contains the full training pipeline; load your CSV, run feature engineering, and serialize new models to `/models/` with joblib.
