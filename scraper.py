import requests
from bs4 import BeautifulSoup


def extract_article_text(url: str):
    """
    Scrapes article text from a news URL.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    article_text = " ".join(
        paragraph.get_text(strip=True)
        for paragraph in paragraphs
    )

    return article_text