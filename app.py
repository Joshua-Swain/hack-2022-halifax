# This shows examples of logging in and using the subreddit, submission, redditor, and comments objects
# It is not implied that you need to collect these specific attributes of submissions or redditors, but are merely examples

from RedditBrowser import RedditBrowser
from Analyzer import Analyzer

import praw
import pandas as pd
import numpy as np

import datetime
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Login and create Reddit instance
reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USERNAME"))

browser = RedditBrowser(reddit)
SUBREDDIT = 'christianity'

# Get Sample Dataframe of top 5 Posts' information
posts = browser.retrieve_posts(SUBREDDIT)
# Get Sample Dataframe of author information
authors = browser.retrieve_authors(posts)
scores = Analyzer.score_authors()
labels = Analyzer.interpret_scores()
