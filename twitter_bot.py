import configparser
import tweepy
import feedparser
import time
import os
import logging
import sys
from logging.handlers import RotatingFileHandler

# Set up logging
log_formatter = logging.Formatter('%(levelname)s - %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger('twitter_bot')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up Twitter API
consumer_key = config.get('twitter', 'consumer_key')
consumer_secret = config.get('twitter', 'consumer_secret')
access_token = config.get('twitter', 'access_token')
access_token_secret = config.get('twitter', 'access_token_secret')

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)

# RSS feed URL
rss_feed_url = 'https://note.com/coding/rss'
#rss_feed_url = 'http://localhost:5000/rss_feed.xml'

# Function to tweet new blog posts
def tweet_new_posts(last_entry_id):
    feed = feedparser.parse(rss_feed_url)
    new_entry = feed.entries[0]
    if new_entry.id != last_entry_id and "おつかれさまです" in new_entry.description:
        tweet_text = f"Blog を書きました: {new_entry.title}\n{new_entry.link}"
        try:
            #api.update_status(tweet_text)
            logger.info(f'Tweeted: {tweet_text}')
            return new_entry.id
        except tweepy.TweepError as error:
            logger.error(f'Tweet failed: {error.reason}')
            return last_entry_id
    else:
        return last_entry_id

def read_last_entry_id(filename):
    try:
        with open(filename, 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return None

def write_last_entry_id(filename, entry_id):
    with open(filename, 'w') as file:
        file.write(entry_id)

def main_loop():
    last_entry_id_filename = 'last_entry_id.txt'
    last_entry_id = read_last_entry_id(last_entry_id_filename)
    while True:
        try:
            new_entry_id = tweet_new_posts(last_entry_id)
            if new_entry_id != last_entry_id:
                write_last_entry_id(last_entry_id_filename, new_entry_id)
                last_entry_id = new_entry_id
            logger.info(f'Sleeping...')
            time.sleep(60 * 30)  # Wait 30 minutes before checking for new posts
        except Exception as error:
            logger.error(f'Unexpected error: {error}')
            time.sleep(60 * 5)  # Wait 5 minutes before trying again

if __name__ == '__main__':
    main_loop()

