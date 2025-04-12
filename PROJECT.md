# Project Overview: Real-Time Sentiment Analysis Dashboard

## Objective
Build a portfolio project demonstrating skills in Python, API integration, machine learning, data visualization, and cloud deployment by creating a dashboard that analyzes tweet sentiment in near real-time using the Twitter API Free tier.

## Technologies Used
- **Python 3.9**: Core programming language.
- **Tweepy**: Access Twitter API v2 (Free tier, 1 request/15 min, 10 tweets/request).
- **Transformers (Hugging Face)**: Sentiment analysis with DistilBERT.
- **Streamlit**: Web-based dashboard for visualization.
- **Pandas**: Data handling for CSV processing.
- **Streamlit Community Cloud**: Free-tier deployment.
- **Git/GitHub**: Version control and hosting.

## Features
- Fetches recent tweets for a user-specified keyword.
- Analyzes sentiment (positive/negative) using DistilBERT.
- Saves live tweet data to `tweets_data.csv`, respects API rate limits with a 15-minute fetch interval.
- Displays mock data when rate-limited for testing.
- Visualizes data with a Streamlit dashboard (table, bar chart, keyword filter), auto-refreshing every minute.
- Deployed live for public access.

## Challenges Overcome
- Navigated Twitter API Free tier constraints (limited requests, minimum 10 tweets).
- Optimized dependency management to balance local functionality (`transformers`, `torch`) with lightweight cloud deployment.
- Implemented periodic fetching and caching to simulate real-time updates without exceeding API limits.

## Future Enhancements
- Integrate advanced NLP models for deeper sentiment insights.
- Add user authentication for personalized dashboards.
- Deploy on AWS for scalability with CI/CD pipelines.

## Links
- GitHub: https://github.com/Dar3071/Real-Time-Sentiment-Analysis-Dashboard
- Live Demo: [https://real-time-sentiment-analysis-dashboard-pmik2nhfgbrfkksnqyhpv6.streamlit.app/]

Developed by [Deon Rennie, Github.comDar3071], April 2025, using VS Code on macOS.