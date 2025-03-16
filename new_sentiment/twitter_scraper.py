# twitter_scraper.py
# ==================================================
# 🐦 TWITTER SENTIMENT ANALYZER – CRYPTO TWEET MONITOR 🐦
# ==================================================

import os
import tweepy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from utils.logger import Logger

# Load API credentials securely
load_dotenv()
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

class TwitterScraper:
    def __init__(self):
        """Initialize Twitter API connection."""
        self.authenticated = self.authenticate()
        self.analyzer = SentimentIntensityAnalyzer()

    def authenticate(self):
        """Authenticate with Twitter API."""
        if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
            Logger.error("❌ Missing Twitter API credentials.")
            return False

        try:
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            Logger.info("✅ Twitter API Connected Successfully.")
            return True
        except Exception as e:
            Logger.error(f"❌ Twitter API Connection Failed: {e}")
            return False

    def fetch_crypto_tweets(self, query="#Bitcoin OR #Crypto OR #Ethereum", count=50):
        """
        Fetches the latest crypto-related tweets and analyzes sentiment.
        Args:
            query (str): Search query for tweets.
            count (int): Number of tweets to fetch.
        Returns:
            dict: Sentiment breakdown (Bullish, Bearish, Neutral).
        """
        if not self.authenticated:
            return {"bullish": 0, "bearish": 0, "neutral": 0}

        try:
            tweets = self.api.search_tweets(q=query, count=count, lang="en", tweet_mode="extended")
            sentiment_scores = [self.analyze_sentiment(tweet.full_text) for tweet in tweets]

            return {
                "bullish": sum(1 for s in sentiment_scores if s > 0.2),
                "bearish": sum(1 for s in sentiment_scores if s < -0.2),
                "neutral": sum(1 for s in sentiment_scores if -0.2 <= s <= 0.2)
            }
        except Exception as e:
            Logger.error(f"❌ Twitter Fetch Error: {e}")
            return {"bullish": 0, "bearish": 0, "neutral": 0}

# 🚀 TEST TWITTER SCRAPER
if __name__ == "__main__":
    scraper = TwitterScraper()
    sentiment = scraper.fetch_crypto_tweets()
    print(f"📊 Twitter Sentiment: {sentiment}")