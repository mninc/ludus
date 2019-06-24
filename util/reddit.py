import praw
import json

with open("config_reddit.json") as f:
    config = json.load(f)

reddit = praw.Reddit(client_id=config["id"],
                     client_secret=config["secret"],
                     user_agent=config["user_agent"])

