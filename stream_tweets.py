import tweepy
from dotenv import load_dotenv
import os
import time
from transformers import pipeline
import csv
from datetime import datetime, timedelta
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Hugging Face sentiment analysis pipeline with DistilBERT
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# File to store last API fetch timestamp
LAST_FETCH_FILE = "last_fetch.json"

# Save live tweets to CSV with sentiment data
def save_to_csv(tweets):
    filename = "tweets_data.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["timestamp", "author_id", "created_at", "text", "sentiment", "confidence"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for tweet in tweets:
            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "author_id": tweet["author_id"],
                "created_at": tweet["created_at"],
                "text": tweet["text"],
                "sentiment": tweet["sentiment"],
                "confidence": tweet["confidence"]
            })

# Check if 15 minutes have passed since last fetch (Free tier limit)
def can_fetch_now():
    if not os.path.exists(LAST_FETCH_FILE):
        return True
    with open(LAST_FETCH_FILE, 'r') as f:
        last_fetch = datetime.fromisoformat(json.load(f)["last_fetch"])
    return datetime.now() - last_fetch >= timedelta(minutes=15)

# Update last fetch timestamp
def update_last_fetch():
    with open(LAST_FETCH_FILE, 'w') as f:
        json.dump({"last_fetch": datetime.now().isoformat()}, f)

# Main function to fetch and process tweets
def main():
    # Load Twitter API Bearer Token
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("Error: TWITTER_BEARER_TOKEN not found in .env")
        return
    
    # Initialize Tweepy client for Twitter API v2
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Prompt user for search keyword
    keyword = input("Enter a keyword to search (e.g., #AI): ")
    print(f"Searching recent tweets for: {keyword}")
    
    if can_fetch_now():
        try:
            # Fetch recent tweets (Free tier: 10 tweets min, 1 request/15 min)
            tweets = client.search_recent_tweets(
                query=keyword,
                max_results=10,
                tweet_fields=["author_id", "created_at"]
            )
            if tweets.data:
                tweet_data = []
                for tweet in tweets.data:
                    # Analyze sentiment for each tweet
                    sentiment = sentiment_analyzer(tweet.text)[0]
                    tweet_info = {
                        "author_id": tweet.author_id,
                        "created_at": tweet.created_at.isoformat(),
                        "text": tweet.text,
                        "sentiment": sentiment["label"],
                        "confidence": sentiment["score"]
                    }
                    tweet_data.append(tweet_info)
                    print(f"Tweet from @{tweet.author_id} at {tweet.created_at}: {tweet.text}")
                    print(f"Sentiment: {sentiment['label']} (Confidence: {sentiment['score']:.2f})")
                save_to_csv(tweet_data)
                print(f"Saved {len(tweet_data)} live tweets to tweets_data.csv")
                update_last_fetch()
            else:
                print("No tweets found for this keyword.")
        except tweepy.errors.TooManyRequests:
            print("Error: 429 Too Many Requests - Free tier allows only 1 request every 15 minutes.")
            print("Displaying mock data for testing (not saved)...")
            time.sleep(2)
            mock_tweets_raw = [
                {"author_id": "123", "created_at": "2025-04-10T10:00:00Z", "text": "This is a test output"},
                {"author_id": "456", "created_at": "2025-04-10T10:01:00Z", "text": f"Learning about {keyword} is amazing!"}
            ]
            for tweet in mock_tweets_raw:
                sentiment = sentiment_analyzer(tweet["text"])[0]
                print(f"Tweet from @{tweet['author_id']} at {tweet['created_at']}: {tweet['text']}")
                print(f"Sentiment: {sentiment['label']} (Confidence: {sentiment['score']:.2f})")
        except tweepy.errors.TweepyException as e:
            print(f"Error: {e}")
    else:
        print("Cannot fetch yet - less than 15 minutes since last fetch.")
        print("Displaying mock data for testing (not saved)...")
        time.sleep(2)
        mock_tweets_raw = [
            {"author_id": "123", "created_at": "2025-04-10T10:00:00Z", "text": "This is a test output"},
            {"author_id": "456", "created_at": "2025-04-10T10:01:00Z", "text": f"Learning about {keyword} is amazing!"}
        ]
        for tweet in mock_tweets_raw:
            sentiment = sentiment_analyzer(tweet["text"])[0]
            print(f"Tweet from @{tweet['author_id']} at {tweet['created_at']}: {tweet['text']}")
            print(f"Sentiment: {sentiment['label']} (Confidence: {sentiment['score']:.2f})")

if __name__ == "__main__":
    main()