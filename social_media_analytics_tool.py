import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import os

# Twitter/X API credentials (replace with your own)
API_KEY = "7rGaR54S2qbrrhDBkPEXHGdnf"
API_SECRET = "bXI35pkTnar0lzWCAhlAauhw6MOfTf4KYjDOTZ59L2SytR1e4B"
ACCESS_TOKEN = "1563914171053670401-XRSnYHXskZg1B87CvmxiBaa7UYXWBA"
ACCESS_TOKEN_SECRET = "SP2oXnbAVHTkf4dabmWEzYWviEyPW4PnJI8yqZO1mrp0f"

# Initialize Tweepy client
def authenticate_twitter():
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    except Exception as e:
        print(f"Error authenticating Twitter API: {e}")
        return None

# Fetch recent tweets based on a keyword
def fetch_tweets(api, keyword, count=100):
    try:
        tweets = api.search_tweets(q=keyword, count=count, lang="en", tweet_mode="extended")
        return tweets
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# Perform sentiment analysis using TextBlob
def analyze_sentiment(tweet):
    try:
        analysis = TextBlob(tweet)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return "Positive"
        elif polarity == 0:
            return "Neutral"
        else:
            return "Negative"
    except:
        return "Unknown"

# Generate analytics report
def generate_report(tweets, keyword):
    data = []
    for tweet in tweets:
        try:
            text = tweet.full_text
            sentiment = analyze_sentiment(text)
            data.append({
                "Tweet": text,
                "User": tweet.user.screen_name,
                "Created_At": tweet.created_at,
                "Retweets": tweet.retweet_count,
                "Favorites": tweet.favorite_count,
                "Sentiment": sentiment
            })
        except AttributeError:
            continue

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"social_media_report_{keyword}_{timestamp}.csv"
    df.to_csv(output_file, index=False)
    print(f"Report saved as {output_file}")

    # Generate visualizations
    plt.figure(figsize=(10, 6))
    
    # Sentiment distribution
    sns.countplot(x="Sentiment", data=df, order=["Positive", "Neutral", "Negative"])
    plt.title(f"Sentiment Analysis for '{keyword}'")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.savefig(f"sentiment_distribution_{keyword}_{timestamp}.png")
    plt.close()
    
    # Engagement metrics
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Retweets"], bins=20, color="blue", label="Retweets")
    sns.histplot(df["Favorites"], bins=20, color="orange", label="Favorites")
    plt.title(f"Engagement Metrics for '{keyword}'")
    plt.xlabel("Count")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig(f"engagement_metrics_{keyword}_{timestamp}.png")
    plt.close()

def main():
    # Authenticate with Twitter API
    api = authenticate_twitter()
    if not api:
        return
    
    # User input for keyword
    keyword = input("Enter a keyword or hashtag to analyze (e.g., #Python): ")
    count = 100  # Number of tweets to fetch
    
    # Fetch and analyze tweets
    tweets = fetch_tweets(api, keyword, count)
    if not tweets:
        print("No tweets found or an error occurred.")
        return
    
    # Generate report and visualizations
    generate_report(tweets, keyword)
    print("Analytics report and visualizations generated successfully.")

if __name__ == "__main__":
    main()