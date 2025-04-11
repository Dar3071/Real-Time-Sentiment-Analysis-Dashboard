import streamlit as st
import pandas as pd
import os

# Title and description
st.title("Twitter Sentiment Analysis Dashboard")
st.write("Visualizes sentiment analysis of recent tweets from Twitter API (Free tier) saved in `tweets_data.csv`.")

# Check if CSV exists
csv_file = "tweets_data.csv"
if os.path.exists(csv_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Display raw data
    st.subheader("Tweet Data")
    st.dataframe(df)
    
    # Sentiment distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)
    
    # Filter by keyword (optional)
    st.subheader("Filter Tweets by Keyword")
    keyword = st.text_input("Enter keyword to filter tweets (e.g., #AI):")
    if keyword:
        filtered_df = df[df["text"].str.contains(keyword, case=False, na=False)]
        st.write(f"Showing tweets containing '{keyword}':")
        st.dataframe(filtered_df)
    else:
        st.write("Enter a keyword to filter the tweets.")
else:
    st.error("No tweet data found. Run `python3 stream_tweets.py` to generate `tweets_data.csv` first.")