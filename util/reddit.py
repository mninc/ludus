import praw
import json

with open("config.json") as f:
    config = json.load(f)

reddit = praw.Reddit(client_id=config["reddit_id"],
                     client_secret=config["reddit_secret"],
                     user_agent=config["reddit_user_agent"])
