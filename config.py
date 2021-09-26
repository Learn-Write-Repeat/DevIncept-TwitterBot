# tweepy-bots/bots/config.py
import tweepy
import logging
from decouple import config

logger = logging.getLogger()


def create_api():
    consumer_key = config("API_KEY")
    consumer_secret = config("API_SECRET_KEY")
    access_token = config("ACCESS_TOKEN")
    access_token_secret = config("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
