"""
Twitter posting functionality - minimal implementation from X.ipynb
"""
import tweepy
import os
import csv
from datetime import datetime
from .config import (
    BEARER_TOKEN,
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
    CSV_FILE
)


# Initialize Twitter API client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)


def post_tweet(text):
    """Post a tweet with the given text"""
    try:
        response = client.create_tweet(text=text)
        print(f"✅ Tweet posted! ID: {response.data['id']}")
        return response.data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def load_post_history():
    """Load previously posted tweets from CSV"""
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row['text'] for row in reader]
    except FileNotFoundError:
        return []


def save_post(topic, text):
    """Save posted tweet to CSV"""
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'topic', 'text'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'topic': topic,
            'text': text
        })
