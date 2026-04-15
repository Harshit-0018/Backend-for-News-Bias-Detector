from typing import List
from pydantic import BaseModel, HttpUrl


class TextRequest(BaseModel):
    text: str


class URLRequest(BaseModel):
    url: HttpUrl


class PredictionResponse(BaseModel):
    bias: str
    confidence: float
    sentiment: str
    entities: List[str]
    important_phrases: List[str]