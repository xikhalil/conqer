# news_scraper.py
# ==================================================
# 📰 CRYPTO NEWS SCRAPER – FETCHES LATEST HEADLINES 📰
# ==================================================

import os
import requests
import json
import time
from dotenv import load_dotenv
from custom_logging.logger import Logger


# Load API key securely
load_dotenv()
API_KEY = os.getenv("CRYPTO_NEWS_API_KEY")
CACHE_FILE = "cache/news_cache.json"

class NewsScraper:
    def __init__(self):
        """Initialize news scraper with caching."""
        self.api_url = "https://cryptonews-api.com/api/v1"
        self.cache_expiry = 300  # Cache news for 5 minutes

    def _read_cache(self):
        """Reads cached news data if available."""
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as file:
                    data = json.load(file)
                    if time.time() - data["timestamp"] < self.cache_expiry:
                        return data["news"]
        except Exception as e:
            Logger.error(f"❌ Cache Read Error: {e}")
        return None

    def _write_cache(self, news_data):
        """Writes news data to cache."""
        try:
            with open(CACHE_FILE, "w") as file:
                json.dump({"timestamp": time.time(), "news": news_data}, file)
        except Exception as e:
            Logger.error(f"❌ Cache Write Error: {e}")

    def fetch_news(self):
        """
        Fetches the latest cryptocurrency news headlines.
        Returns:
            list: List of latest news headlines & summaries.
        """
        cached_news = self._read_cache()
        if cached_news:
            return cached_news

        if not API_KEY:
            Logger.error("❌ Missing API Key for Crypto News API.")
            return []

        try:
            response = requests.get(f"{self.api_url}/category?section=general&items=10&apikey={API_KEY}", timeout=5)
            response.raise_for_status()
            news_data = response.json()

            if "data" not in news_data:
                Logger.warning("⚠️ No news data received.")
                return []

            articles = [{"title": article["title"], "summary": article["text"], "url": article["news_url"]}
                        for article in news_data["data"]]

            self._write_cache(articles)  # Cache fetched news
            return articles

        except requests.exceptions.RequestException as e:
            Logger.error(f"❌ News Fetch Error: {e}")
            return []

# 🚀 FETCH NEWS
if __name__ == "__main__":
    scraper = NewsScraper()
    latest_news = scraper.fetch_news()
    for news in latest_news[:5]:  # Display top 5 news articles
        print(f"📰 {news['title']} - {news['summary']} ({news['url']})")
