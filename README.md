#  SentimentAI — NLP Sentiment Analysis Dashboard

A production-grade sentiment analysis platform with a FastAPI ML backend and a
professional dark-mode React dashboard. Built to demonstrate real NLP engineering
to clients.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Real-time NLP** | Lexicon-based analyzer with negation handling & intensifier weighting |
| **Emotion Detection** | 6-emotion wheel: joy, anger, sadness, fear, surprise, trust |
| **Keyword Extraction** | Sentiment-tagged keyword highlighting |
| **Batch Analysis** | Process up to 50 texts at once with aggregate statistics |
| **Trend Dashboard** | 14-day historical sentiment chart |
| **Export** | One-click JSON export of all results |
| **Demo Mode** | Works fully offline when API is unavailable |
| **REST API** | Fully documented at `/docs` (Swagger UI) |

---

## 🗂 Project Structure

```
sentiment-dashboard/
├── backend/
│   ├── main.py              # FastAPI app — NLP pipeline & REST endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Full React/Vanilla JS dashboard (zero build tools)
├── ml_notebook.ipynb        # Jupyter notebook — ML deep dive & visualizations
├── start.sh                 # One-command startup (Mac/Linux)
├── start.bat                # One-command startup (Windows)
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Run (Mac/Linux)
```bash
chmod +x start.sh
./start.sh
```

### Run (Windows)
```
Double-click start.bat
```

### Manual Start
```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
python -m http.server 3000
```

Then open **http://localhost:3000**

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | Analyze a single text |
| `POST` | `/analyze/batch` | Analyze up to 50 texts |
| `GET` | `/trends` | Get 14-day trend data |
| `GET` | `/demo/samples` | Load sample texts |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive API docs (Swagger) |

### Example Request
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing!"}'
```

### Example Response
```json
{
  "sentiment": {
    "label": "positive",
    "score": 0.847,
    "compound": 0.694,
    "confidence": 0.912
  },
  "emotions": {
    "joy": 0.512,
    "trust": 0.231,
    "surprise": 0.157,
    "anger": 0.0,
    "sadness": 0.0,
    "fear": 0.1
  },
  "keywords": [
    {"word": "amazing", "count": 1, "sentiment": "positive"},
    {"word": "product", "count": 1, "sentiment": "neutral"}
  ],
  "metadata": {
    "word_count": 6,
    "char_count": 38,
    "analyzed_at": "2024-01-15T14:32:11"
  }
}
```

---

## 🧪 ML Notebook

Open `ml_notebook.ipynb` in Jupyter to explore:

- Full NLP pipeline breakdown
- Dataset visualization (distribution, confusion matrix, scatter plots)
- Feature engineering (8 engineered features)
- Feature importance analysis
- 30-day trend simulation

```bash
pip install jupyter matplotlib pandas numpy
jupyter notebook ml_notebook.ipynb
```

---

## 🛠 Tech Stack

**Backend**
- FastAPI — high-performance async Python API
- Pydantic — data validation & serialization
- Uvicorn — ASGI server

**Frontend**
- Vanilla JS with Chart.js — zero build tools, instant startup
- CSS custom properties for full dark-mode theming
- Syne + DM Sans + DM Mono fonts

**ML / NLP**
- Custom lexicon-based NLP engine
- Negation-aware tokenization
- Intensifier weighting
- Emotion wheel detection

---

## 📈 Extending the Project

### Add a real ML model
```python
# In backend/main.py, swap analyze_sentiment() with:
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return {"label": result["label"].lower(), "score": result["score"], ...}
```

### Add a database
```bash
pip install sqlalchemy aiosqlite
# Store every analysis in SQLite for real trend data
```

### Deploy
```bash
# Backend (Railway / Render / EC2)
uvicorn main:app --host 0.0.0.0 --port $PORT

# Frontend — upload frontend/index.html to Netlify, Vercel, or S3
```

---

## 📝 License

MIT — free for commercial and personal use.

---

*Built with FastAPI + Chart.js · Designed for client demos*
