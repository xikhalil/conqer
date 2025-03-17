# sentiment_analysis.py
# ==================================================
# 📊 SENTIMENT ANALYSIS – MARKET TREND DETECTOR 📊
# ==================================================

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from custom_logging.logger import Logger


class SentimentAnalyzer:
    def __init__(self):
        """Initialize Sentiment Analyzer with VADER."""
        self.analyzer = SentimentIntensityAnalyzer()
        Logger.info("✅ Sentiment Analyzer Ready.")

    def analyze_text(self, text):
        """
        Analyzes sentiment of given text.
        Args:
            text (str): The input text (e.g., news or tweet).
        Returns:
            float: Sentiment score (-1 to +1).
        """
        blob_score = TextBlob(text).sentiment.polarity
        vader_score = self.analyzer.polarity_scores(text)["compound"]

        # Weighted average of both sentiment scores
        return round((blob_score + vader_score) / 2, 3)

    def determine_market_sentiment(self, articles):
        """
        Determines overall market sentiment based on multiple news articles.
        Args:
            articles (list): List of news articles or tweets.
        Returns:
            str: "BULLISH", "BEARISH", or "NEUTRAL".
        """
        if not articles:
            return "NEUTRAL"

        sentiment_scores = [self.analyze_text(article["summary"]) for article in articles]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

        if avg_sentiment > 0.2:
            return "BULLISH"
        elif avg_sentiment < -0.2:
            return "BEARISH"
        return "NEUTRAL"

# 🚀 TEST SENTIMENT ANALYSIS
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    sample_news = [{"summary": "Bitcoin prices are rising with strong institutional support."},
                   {"summary": "Market is uncertain as investors remain cautious."}]

    market_sentiment = analyzer.determine_market_sentiment(sample_news)
    print(f"📊 Market Sentiment: {market_sentiment}")
