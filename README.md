<div align="center">

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/NLP-Custom_Engine-7C6CFA?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-34D399?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Production_Ready-34D399?style=for-the-badge"/>

<br/><br/>

# 🧠 SentimentAI

### Real-time NLP Sentiment Analysis Dashboard

**Analyze text sentiment, detect emotions, extract keywords, and visualize trends —
powered by a custom NLP engine and a professional FastAPI + JavaScript frontend.**

[🚀 Quick Start](#-quick-start) · [📡 API Docs](#-api-reference) · [🧪 ML Notebook](#-ml-notebook) · [🤝 Contributing](#-contributing)

<br/>

</div>

---

## 📸 Dashboard Preview

```
┌──────────────────────────────────────────────────────────────────┐
│  🧠 SentimentAI          [Text Analyzer] [Batch] [Trends]        │
├──────────────┬───────────────────────────────────────────────────┤
│              │  ┌───────────────────────────────────────────┐    │
│  ◈ Analyze   │  │ Input Text                  LIVE ANALYSIS │    │
│  ◫ Batch     │  │ ┌───────────────────────────────────────┐ │    │
│  ◬ Trends    │  │ │ Enter text to analyze...              │ │    │
│              │  │ └───────────────────────────────────────┘ │    │
│  History     │  │           [ Analyze Sentiment → ]         │    │
│  ─────────── │  └───────────────────────────────────────────┘    │
│  ✅ Great... │                                                    │
│  ❌ Terri... │  Sentiment    Score     Confidence    Words        │
│  ➖ It's ... │  Positive     0.857     99%           12           │
│              │                                                    │
│  ● API Live  │  [Sentiment Result]      [Emotion Profile]        │
└──────────────┴───────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description 
|---|---
| **Real-time Sentiment** | Positive / Negative / Neutral classification with compound scoring 
| **Emotion Detection** | 6-axis wheel — joy, anger, sadness, fear, surprise, trust 
| **Keyword Extraction** | Sentiment-tagged keywords with frequency counts 
| **Batch Processing** | Analyze up to 50 texts at once with aggregate statistics 
| **Trend Dashboard** | 14-day historical sentiment chart with volume bars 
| **Analysis History** | Click-to-reload past analyses from the sidebar 
| **JSON Export** | One-click structured export of all results 
| **Offline Demo Mode** | Frontend works without the backend — great for client demos 
| **Swagger UI** | Auto-generated interactive API docs at `/docs` 

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Browser / Client                       │
│                  frontend/index.html                      │
│        (Vanilla JS + Chart.js + CSS Custom Properties)   │
└───────────────────────┬──────────────────────────────────┘
                        │ HTTP REST (JSON)
                        ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI Backend  :8000                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │                  NLP Pipeline                      │  │
│  │  Tokenizer → Negation Handler → Intensifier Weight │  │
│  │  → Lexicon Scoring → Emotion Detection             │  │
│  │  → Keyword Extraction → Confidence Scoring         │  │
│  └────────────────────────────────────────────────────┘  │
│  Routes: /analyze  /analyze/batch  /trends  /health      │
└──────────────────────────────────────────────────────────┘
```

---

## 🗂 Project Structure

```
sentimentai/
├── 📁 backend/
│   ├── main.py              # FastAPI app + full NLP engine
│   └── requirements.txt     # Python dependencies (3 packages only)
│
├── 📁 frontend/
│   └── index.html           # Complete dashboard — zero build tools needed
│
├── 📁 .github/
│   ├── workflows/ci.yml     # GitHub Actions — auto test on push
│   └── ISSUE_TEMPLATE/      # Bug report & feature request templates
│
├── 📓 ml_notebook.ipynb     # ML deep-dive: EDA, charts, feature importance
├── 🐧 start.sh              # One-command startup (Mac / Linux)
├── 🪟 start.bat             # One-command startup (Windows)
├── 🤝 CONTRIBUTING.md       # Contribution guidelines
├── 📄 LICENSE               # MIT License
└── 📖 README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python **3.9+**
- pip

### One-command startup

**Mac / Linux**
```bash
git clone https://github.com/YOUR_USERNAME/sentimentai.git
cd sentimentai
chmod +x start.sh && ./start.sh
```

**Windows**
```bash
git clone https://github.com/YOUR_USERNAME/sentimentai.git
cd sentimentai
start.bat
```

### Manual startup

```bash
# Terminal 1 — Backend API
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
python -m http.server 3000
```

Then open **[http://localhost:3000](http://localhost:3000)** 🎉

> **No backend?** No problem — the dashboard has a built-in demo mode and runs fully offline.

---

## 📡 API Reference

**Base URL:** `http://localhost:8000`  
**Interactive Docs:** `http://localhost:8000/docs`

### `POST /analyze` — Single text analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing!"}'
```

<details>
<summary>📄 Full Response</summary>

```json
{
  "id": "ana_1705329131",
  "text": "This product is absolutely amazing!",
  "sentiment": {
    "label": "positive",
    "score": 0.857,
    "compound": 0.714,
    "confidence": 0.99,
    "pos": 0.857,
    "neg": 0.0
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
    { "word": "amazing", "count": 1, "sentiment": "positive" },
    { "word": "product", "count": 1, "sentiment": "neutral" }
  ],
  "metadata": {
    "word_count": 6,
    "char_count": 38,
    "source": "dashboard",
    "analyzed_at": "2024-01-15T14:32:11"
  }
}
```
</details>

### `POST /analyze/batch` — Batch analysis (up to 50 texts)

```bash
curl -X POST http://localhost:8000/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great product!", "Terrible service.", "It is okay."]}'
```

<details>
<summary>📄 Full Response</summary>

```json
{
  "summary": {
    "total": 3,
    "positive": 1,  "positive_pct": 33.3,
    "negative": 1,  "negative_pct": 33.3,
    "neutral":  1,  "neutral_pct":  33.3,
    "avg_confidence": 0.821
  },
  "results": [ "..." ]
}
```
</details>

### All Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | Analyze a single text |
| `POST` | `/analyze/batch` | Analyze up to 50 texts |
| `GET` | `/trends?days=14` | 14-day historical trend data |
| `GET` | `/demo/samples` | 8 built-in sample texts |
| `GET` | `/health` | Service health check |
| `GET` | `/docs` | Swagger UI — interactive docs |

---

## 🧪 ML Notebook

`ml_notebook.ipynb` is a standalone ML walkthrough — ideal for client presentations or learning.

**What's inside:**

- 📊 **Dataset EDA** — 22-sample labeled corpus with class distribution
- 🔬 **NLP Pipeline** — tokenizer, negation handling, intensifier weighting
- 📈 **6-panel Analytics** — confusion matrix, compound distribution, confidence boxplots, word heatmap
- ⚙️ **Feature Engineering** — 8 hand-crafted NLP features (pos/neg hits, caps ratio, intensifiers...)
- 🎯 **Feature Importance** — Pearson correlation analysis (SHAP-style bar chart)
- 📉 **Trend Simulation** — 30-day volume-weighted sentiment timeline
- 🌐 **Live API Demo** — test the running backend from within the notebook

```bash
pip install jupyter matplotlib pandas numpy
jupyter notebook ml_notebook.ipynb
```

---

## 🛠 Tech Stack

**Backend**

| Library | Version | Purpose |
|---|---|---|
| FastAPI | 0.111 | High-performance async REST API |
| Uvicorn | 0.29 | ASGI production server |
| Pydantic | 2.7 | Data validation & serialization |

**Frontend**

| Tool | Purpose |
|---|---|
| Vanilla JS (ES6+) | Core logic, API calls, state management |
| Chart.js 4.4 | Interactive trend charts |
| CSS Custom Properties | Dark-mode theming system |
| Syne · DM Sans · DM Mono | Typography |

**NLP Engine**

| Technique | Implementation |
|---|---|
| Tokenization | Regex word-boundary tokenizer |
| Negation handling | 4-token sliding window |
| Intensifier weighting | 1.5× multiplier (very / really / extremely...) |
| Compound scoring | Normalized to [-1, 1] |
| Emotion detection | 6-class lexicon with softmax normalization |
| Confidence | Log-scaled hit density + compound magnitude |

---

## 🔌 Extending the Project

<details>
<summary>🤗 Swap in a HuggingFace Transformer model</summary>

```python
# backend/main.py
from transformers import pipeline

_pipe = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text: str) -> dict:
    result = _pipe(text[:512])[0]
    label  = result["label"].lower()
    score  = result["score"] if label == "positive" else 1 - result["score"]
    return {
        "label": label,
        "score": round(score, 4),
        "confidence": round(result["score"], 4),
        "compound": round(score * 2 - 1, 4),
    }
```
</details>

<details>
<summary>🗄 Add SQLite persistence for real trend data</summary>

```bash
pip install sqlalchemy aiosqlite
```

```python
# Store every /analyze result in a database
# Query it in /trends for real historical data
```
</details>

<details>
<summary>🌐 Deploy for free</summary>

```bash
# Backend — Railway or Render (free tier)
uvicorn main:app --host 0.0.0.0 --port $PORT

# Frontend — drag frontend/index.html to Netlify Drop
# https://app.netlify.com/drop
# Done in 30 seconds, free forever
```
</details>

---

## 🤝 Contributing

All contributions are welcome — from fixing a typo to adding a new model.

```bash
# 1. Fork → Clone
git clone https://github.com/YOUR_USERNAME/sentimentai.git

# 2. Branch
git checkout -b feature/your-feature-name

# 3. Change → Commit
git commit -m "feat: describe your change"

# 4. Push → Pull Request
git push origin feature/your-feature-name
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

**Good first issues:**
- 🌍 Add multilingual lexicon support
- 🧪 Write unit tests for the NLP engine
- 🌗 Add light/dark mode toggle
- 📥 Add CSV import for batch mode
- 🐦 Add Twitter/Reddit live stream integration

---

## 📄 License

Distributed under the **MIT License** — free for personal and commercial use.
See [LICENSE](LICENSE) for full text.

---

## 👤 Author

Built by **[Your Name]** — Data Scientist & ML Engineer available for freelance work.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourhandle)
[![Upwork](https://img.shields.io/badge/Upwork-Hire_Me-6FDA44?style=flat-square&logo=upwork)](https://upwork.com/freelancers/yourprofile)
[![Fiverr](https://img.shields.io/badge/Fiverr-Order_Now-1DBF73?style=flat-square&logo=fiverr)](https://fiverr.com/yourusername)

---

<div align="center">

**⭐ Star this repo if it helped you — it keeps the project alive! ⭐**

</div>
