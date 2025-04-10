import tweepy
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Main function
def main():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("Error: TWITTER_BEARER_TOKEN not found in .env")
        return
    
    # Initialize Tweepy Client for v2 API
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Get keyword from user
    keyword = input("Enter a keyword to search (e.g., #AI): ")
    print(f"Searching recent tweets for: {keyword}")
    
    try:
        # Search recent tweets (Free tier: 1 request/15 min)
        tweets = client.search_recent_tweets(
            query=keyword,
            max_results=10,  # Small batch to conserve quota
            tweet_fields=["author_id", "created_at"]
        )
        if tweets.data:
            for tweet in tweets.data:
                print(f"Tweet from @{tweet.author_id} at {tweet.created_at}: {tweet.text}")
        else:
            print("No tweets found for this keyword.")
    except tweepy.errors.TooManyRequests:
        print("Error: 429 Too Many Requests - Free tier allows only 1 request every 15 minutes.")
        print("Waiting 15 minutes or use mock data. Retrying in 5 seconds with mock data for testing...")
        time.sleep(2)  # Short delay for demo; real wait would be 900s
        # Mock tweets for testing
        mock_tweets = [
            {"author_id": "123", "created_at": "2025-04-10T10:00:00Z", "text": f"This is a test output"},
            {"author_id": "456", "created_at": "2025-04-10T10:01:00Z", "text": f"Learning about {keyword} is amazing!"}
        ]
        for tweet in mock_tweets:
            print(f"Tweet from @{tweet['author_id']} at {tweet['created_at']}: {tweet['text']}")
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()