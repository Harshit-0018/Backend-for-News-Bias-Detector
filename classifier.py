import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = os.path.join("app", "models", "bias_model")

LABEL_MAP = {
    0: "Left",
    1: "Center",
    2: "Right"
}

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()


def extract_important_phrases(text: str):
    raw_sentences = re.split(r'[.!?]', text)

    phrases = []

    for sentence in raw_sentences:
        cleaned = sentence.strip()

        cleaned = re.sub(r'\|+', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned)

        if len(cleaned) < 30:
            continue

        if cleaned not in phrases:
            phrases.append(cleaned)

    return phrases[:5]


def predict_bias(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][prediction].item()

    important_phrases = extract_important_phrases(text)

    return (
        LABEL_MAP[prediction],
        round(confidence, 4),
        important_phrases
    )