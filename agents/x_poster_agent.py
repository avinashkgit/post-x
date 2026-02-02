import tweepy

class XPosterAgent:
    def __init__(self, bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def post(self, text):
        try:
            self.client.create_tweet(text=text)
            print("Posted:", text)
            return True
        except Exception as e:
            print("Error posting:", e)
            return False