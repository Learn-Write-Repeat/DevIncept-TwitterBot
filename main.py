# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
from time import sleep


# class FavRetweetListener(tweepy.StreamListener):
#     def __init__(self, api):
#         self.api = api
#         self.me = api.me()

#     def on_status(self, tweet):
#         logger.info(f"Processing tweet id {tweet.id}")
#         if tweet.in_reply_to_status_id is not None or \
#                 tweet.user.id == self.me.id:
#             # This tweet is a reply or I'm its author so, ignore it
#             return
#         if not tweet.favorited:
#             # Mark it as Liked, since we have not done it yet
#             try:
#                 tweet.favorite()
#             except Exception:
#                 logger.error("Error on fav", exc_info=True)

#     def on_error(self, status):
#         logger.error(status)


def get_tweets(api, search_keywords):
    # Exclude retweets from search to avoid repeats
    tweets = tweepy.Cursor(api.search,
                           q=search_keywords + " -filter:retweets",
                           count=100,
                           result_type="mixed",
                           monitor_rate_limit=True,
                           wait_on_rate_limit=True,
                           lang="en").items()
    return tweets


def like_tweets_now(api, tweets):
    for tweet in tweets:
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.user.id != api.me().id or tweet.in_reply_to_status_id is not None:
            if not tweet.favorited:
                # Mark it as Liked, since we have not done it yet
                try:
                    tweet.favorite()
                except Exception:
                    logger.error("Error on fav", exc_info=True)
            else:
                logger.info("Has been favorited previously")
        sleep(100)


def main(keywords):
    api = create_api()
    tweets = get_tweets(api, keywords)
    like_tweets_now(api, tweets)


if __name__ == "__main__":
    main("devincept")
