from textblob import TextBlob


def get_sentiment(text: str):
    """
    Returns Positive, Negative or Neutral sentiment.
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    if polarity < -0.1:
        return "Negative"

    return "Neutral"