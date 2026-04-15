import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABEL_MAP = {
    0: "Left",
    1: "Center",
    2: "Right"
}


def extract_important_phrases(text: str):
    keywords = [
        "government",
        "president",
        "congress",
        "election",
        "policy",
        "democrat",
        "republican",
        "media"
    ]

    phrases = []

    for sentence in text.split("."):
        for keyword in keywords:
            if keyword.lower() in sentence.lower():
                cleaned = sentence.strip()

                if cleaned and cleaned not in phrases:
                    phrases.append(cleaned)

                break

    return phrases[:5]


def predict_bias(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)
    prediction = torch.argmax(probs, dim=1).item()
    confidence = probs[0][prediction].item()

    bias = LABEL_MAP.get(prediction, "Center")

    return bias, round(confidence, 4), extract_important_phrases(text)