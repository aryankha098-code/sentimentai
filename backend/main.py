from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
import math
import random
from datetime import datetime, timedelta
from collections import Counter

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Lightweight NLP (no heavy dependencies) ───────────────────────────────

POSITIVE_WORDS = {
    "great", "good", "excellent", "amazing", "wonderful", "fantastic", "love",
    "best", "happy", "joy", "beautiful", "awesome", "perfect", "brilliant",
    "outstanding", "superb", "delightful", "pleased", "impressed", "enjoy",
    "recommend", "satisfied", "helpful", "friendly", "reliable", "fast",
    "easy", "clean", "smooth", "efficient", "innovative", "impressive",
    "thrilled", "excited", "glad", "grateful", "thankful", "positive",
    "success", "win", "gain", "benefit", "improve", "boost", "strong",
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "poor", "worst", "hate",
    "disappointed", "frustrating", "annoying", "useless", "broken", "slow",
    "difficult", "confusing", "expensive", "waste", "problem", "issue",
    "error", "fail", "failed", "never", "avoid", "boring", "ugly",
    "disgusting", "pathetic", "mediocre", "inferior", "inadequate",
    "disaster", "regret", "unhappy", "angry", "upset", "annoyed",
}

NEGATION_WORDS = {"not", "no", "never", "neither", "nor", "barely", "hardly", "scarcely"}

INTENSIFIERS = {"very", "really", "extremely", "absolutely", "incredibly", "so", "quite", "super"}

EMOTION_LEXICON = {
    "joy":      ["happy", "joy", "delight", "love", "wonderful", "fantastic", "excited", "thrilled", "great", "amazing"],
    "anger":    ["angry", "furious", "rage", "hate", "annoying", "frustrating", "terrible", "awful", "disgusting"],
    "sadness":  ["sad", "unhappy", "disappointed", "depressed", "regret", "sorry", "miss", "loss", "unfortunate"],
    "fear":     ["afraid", "scared", "worried", "anxious", "nervous", "concern", "risk", "danger", "uncertain"],
    "surprise": ["surprised", "shocked", "unexpected", "sudden", "wow", "incredible", "unbelievable", "amazing"],
    "trust":    ["reliable", "trustworthy", "honest", "confident", "secure", "safe", "dependable", "loyal"],
}


def tokenize(text: str) -> List[str]:
    return re.findall(r'\b\w+\b', text.lower())


def analyze_sentiment(text: str) -> dict:
    tokens = tokenize(text)
    if not tokens:
        return {"label": "neutral", "score": 0.5, "confidence": 0.0}

    pos_score = 0.0
    neg_score = 0.0
    negated = False

    for i, token in enumerate(tokens):
        # Check negation window
        if token in NEGATION_WORDS:
            negated = True
            continue
        if i > 0 and tokens[i - 1] not in NEGATION_WORDS:
            negated = False

        multiplier = 1.5 if (i > 0 and tokens[i - 1] in INTENSIFIERS) else 1.0

        if token in POSITIVE_WORDS:
            if negated:
                neg_score += multiplier
            else:
                pos_score += multiplier

        elif token in NEGATIVE_WORDS:
            if negated:
                pos_score += multiplier * 0.5
            else:
                neg_score += multiplier

    total = pos_score + neg_score
    if total == 0:
        compound = 0.0
    else:
        compound = (pos_score - neg_score) / (total + 1)

    # Normalize to [-1, 1]
    compound = max(-1.0, min(1.0, compound))

    if compound >= 0.1:
        label = "positive"
        score = 0.5 + compound * 0.5
    elif compound <= -0.1:
        label = "negative"
        score = 0.5 - abs(compound) * 0.5
    else:
        label = "neutral"
        score = 0.5

    confidence = min(0.99, abs(compound) + 0.3 * math.log(1 + total))

    return {
        "label": label,
        "score": round(score, 4),
        "compound": round(compound, 4),
        "confidence": round(min(confidence, 0.99), 4),
        "pos": round(pos_score / (total + 1e-9), 4),
        "neg": round(neg_score / (total + 1e-9), 4),
    }


def detect_emotions(text: str) -> dict:
    tokens = set(tokenize(text))
    scores = {}
    for emotion, words in EMOTION_LEXICON.items():
        hits = len(tokens.intersection(set(words)))
        scores[emotion] = round(hits / (len(words) * 0.3 + 1), 4)

    total = sum(scores.values()) or 1
    normalized = {e: round(v / total, 4) for e, v in scores.items()}
    return normalized


def extract_keywords(text: str, top_n: int = 8) -> List[dict]:
    tokens = tokenize(text)
    stopwords = {"the", "a", "an", "is", "it", "in", "on", "at", "to", "for",
                 "of", "and", "or", "but", "this", "that", "with", "was", "are",
                 "be", "been", "have", "has", "had", "do", "does", "did", "will",
                 "would", "could", "should", "may", "might", "can", "i", "you",
                 "he", "she", "we", "they", "my", "your", "our", "their"}
    meaningful = [t for t in tokens if t not in stopwords and len(t) > 2]
    counts = Counter(meaningful)
    keywords = []
    for word, count in counts.most_common(top_n):
        if word in POSITIVE_WORDS:
            sentiment = "positive"
        elif word in NEGATIVE_WORDS:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        keywords.append({"word": word, "count": count, "sentiment": sentiment})
    return keywords


def generate_trend_data(days: int = 14) -> List[dict]:
    """Generate simulated historical trend data."""
    trend = []
    base_pos = 0.55
    for i in range(days):
        date = (datetime.now() - timedelta(days=days - i)).strftime("%Y-%m-%d")
        drift = random.gauss(0, 0.05)
        base_pos = max(0.2, min(0.9, base_pos + drift))
        trend.append({
            "date": date,
            "positive": round(base_pos, 3),
            "negative": round((1 - base_pos) * random.uniform(0.5, 0.8), 3),
            "neutral": round(random.uniform(0.05, 0.2), 3),
            "volume": random.randint(20, 200),
        })
    return trend


# ─── Models ───────────────────────────────────────────────────────────────

class TextInput(BaseModel):
    text: str
    source: Optional[str] = "manual"

class BatchInput(BaseModel):
    texts: List[str]
    source: Optional[str] = "batch"


# ─── Routes ───────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "service": "Sentiment Analysis API"}


@app.post("/analyze")
def analyze_single(payload: TextInput):
    if not payload.text.strip():
        raise HTTPException(400, "Text cannot be empty")

    sentiment = analyze_sentiment(payload.text)
    emotions = detect_emotions(payload.text)
    keywords = extract_keywords(payload.text)

    word_count = len(payload.text.split())
    reading_time = max(1, word_count // 200)

    return {
        "id": f"ana_{int(datetime.now().timestamp())}",
        "text": payload.text[:500],
        "sentiment": sentiment,
        "emotions": emotions,
        "keywords": keywords,
        "metadata": {
            "word_count": word_count,
            "char_count": len(payload.text),
            "reading_time_sec": reading_time,
            "source": payload.source,
            "analyzed_at": datetime.now().isoformat(),
        }
    }


@app.post("/analyze/batch")
def analyze_batch(payload: BatchInput):
    if not payload.texts:
        raise HTTPException(400, "Texts list cannot be empty")
    if len(payload.texts) > 50:
        raise HTTPException(400, "Max 50 texts per batch")

    results = []
    label_counts = Counter()

    for i, text in enumerate(payload.texts):
        if not text.strip():
            continue
        sentiment = analyze_sentiment(text)
        emotions = detect_emotions(text)
        label_counts[sentiment["label"]] += 1
        results.append({
            "index": i,
            "text": text[:200],
            "sentiment": sentiment,
            "emotions": emotions,
        })

    total = len(results) or 1
    summary = {
        "total": len(results),
        "positive": label_counts["positive"],
        "negative": label_counts["negative"],
        "neutral": label_counts["neutral"],
        "positive_pct": round(label_counts["positive"] / total * 100, 1),
        "negative_pct": round(label_counts["negative"] / total * 100, 1),
        "neutral_pct": round(label_counts["neutral"] / total * 100, 1),
        "avg_confidence": round(
            sum(r["sentiment"]["confidence"] for r in results) / total, 4
        ),
    }

    return {"summary": summary, "results": results, "source": payload.source}


@app.get("/trends")
def get_trends(days: int = 14):
    return {"days": days, "data": generate_trend_data(days)}


@app.get("/demo/samples")
def get_samples():
    samples = [
        "The product quality is absolutely amazing! Best purchase I've made this year.",
        "Customer service was terrible. I waited 3 hours and got no help at all.",
        "It's okay, nothing special. Does what it's supposed to do.",
        "I'm so frustrated with the slow delivery. Never ordering again!",
        "Incredible experience from start to finish. Highly recommend to everyone.",
        "The interface is confusing and the app crashes constantly. Very disappointed.",
        "Good value for money. The build quality is solid and shipping was fast.",
        "Outstanding support team! They resolved my issue within minutes.",
    ]
    return {"samples": samples}


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
