from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests

load_dotenv()

router = APIRouter(prefix="/news", tags=["News"])

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


@router.get("/")
def get_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=India&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    )


    response = requests.get(url)
    data = response.json()

    return {
        "articles": data.get("articles", [])
    }