import tweepy
import time

# Replace these with your own credentials
API_KEY = 'AGpHvvvOakjeD35MFVvaCV92w'
API_SECRET_KEY = 'APRJL8yZHeYN7w9mBHqIEhReupBXJprnCvaDjl6EiiZGiweUIo'
ACCESS_TOKEN = '1696145368311037952-6jrKeVviJAtRMVsKLatH52ZhZYsLu5'
ACCESS_TOKEN_SECRET = 'kn3wgwPBZFCEz6gOuCrzA8bRoVvvMeCZxZq6J2lE3677E'

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Verify authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print(f"Error during authentication: {e}")

# Function to create a tweet
def create_tweet():
    try:
        api.update_status("Hello, world! This is my first tweet from my Twitter bot.")
        print("Tweeted successfully!")
    except Exception as e:
        print(f"Error while tweeting: {e}")

# Function to check mentions and reply
def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            print(f"Answering to {tweet.user.name}")
            try:
                api.update_status(
                    status=f"@{tweet.user.screen_name} Thanks for the mention!",
                    in_reply_to_status_id=tweet.id,
                )
            except Exception as e:
                print(f"Error while replying: {e}")
    return new_since_id

# Function to retweet tweets with a specific hashtag
def retweet_hashtag(api, hashtag):
    for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, lang="en").items(10):
        try:
            tweet.retweet()
            print(f"Retweeted: {tweet.text}")
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Initial tweet
create_tweet()

# Monitoring mentions and retweeting hashtags
SINCE_ID = 1
HASHTAG = "#YourHashtag"

while True:
    SINCE_ID = check_mentions(api, ["hello"], SINCE_ID)
    retweet_hashtag(api, HASHTAG)
    time.sleep(60)
