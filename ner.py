import spacy

# Run once:
# python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str):
    """
    Extract important named entities from article text.
    """
    doc = nlp(text)

    allowed_labels = {
        "PERSON",
        "ORG",
        "GPE",
        "NORP",
        "EVENT"
    }

    entities = []

    for ent in doc.ents:
        if ent.label_ in allowed_labels:
            cleaned = ent.text.strip()

            if cleaned not in entities:
                entities.append(cleaned)

    return entities[:10]