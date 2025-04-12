import streamlit as st
import pandas as pd
import os

# Cache data to refresh every 60 seconds
@st.cache_data(ttl=60)
def load_data():
    """Load tweet data from CSV if it exists."""
    csv_file = "tweets_data.csv"
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    return None

# Set page title and description
st.title("Twitter Sentiment Analysis Dashboard")
st.write("Visualizes sentiment analysis of recent tweets from Twitter API (Free tier) saved in `tweets_data.csv`. Updates every minute.")

# Load data
df = load_data()

if df is not None:
    # Display raw tweet data
    st.subheader("Tweet Data")
    st.dataframe(df)
    
    # Show bar chart of sentiment distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)
    
    # Allow keyword filtering
    st.subheader("Filter Tweets by Keyword")
    keyword = st.text_input("Enter keyword to filter tweets (e.g., #AI, #Weather, #Travel ):")
    if keyword:
        filtered_df = df[df["text"].str.contains(keyword, case=False, na=False)]
        st.write(f"Showing tweets containing '{keyword}':")
        st.dataframe(filtered_df)
    else:
        st.write("Enter a keyword to filter the tweets. (e.g., #AI, #Weather, #Travel )")
else:
    st.error("No tweet data found. Run `python3 stream_tweets.py` locally to generate `tweets_data.csv` first.")