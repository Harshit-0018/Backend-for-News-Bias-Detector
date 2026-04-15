from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.prediction import TextRequest, URLRequest, PredictionResponse
from app.services.classifier import predict_bias
from app.services.sentiment import get_sentiment
from app.services.ner import extract_entities
from app.services.scraper import extract_article_text

router = APIRouter(tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict_news(data: TextRequest):
    try:
        text = data.text.strip()

        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        bias, confidence, phrases = predict_bias(text)
        sentiment = get_sentiment(text)
        entities = extract_entities(text)

        return PredictionResponse(
            bias=bias,
            confidence=confidence,
            sentiment=sentiment,
            entities=entities,
            important_phrases=phrases
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-url", response_model=PredictionResponse)
def analyze_news_url(data: URLRequest):
    try:
        article_text = extract_article_text(data.url)

        if not article_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract article text from URL"
            )

        bias, confidence, phrases = predict_bias(article_text)
        sentiment = get_sentiment(article_text)
        entities = extract_entities(article_text)

        return PredictionResponse(
            bias=bias,
            confidence=confidence,
            sentiment=sentiment,
            entities=entities,
            important_phrases=phrases
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))