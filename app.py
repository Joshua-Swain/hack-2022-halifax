# Hack Sample Code
# This shows examples of logging in and using the subreddit, submission, redditor, ancd comments objects
# It is not implied that you need to collect these specific attributes of submissions or redditors, but are merely examples

# Imports
import praw
import pandas as pd
import numpy as np
import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Login and create Reddit instance
myClientIDvar = os.environ.get("CLIENT_ID")
myClientSecret = os.environ.get("CLIENT_SECRET")
myRedditUserName = os.environ.get("REDDIT_USERNAME")

reddit = praw.Reddit(client_id=myClientIDvar,
                     client_secret=myClientSecret, user_agent=myRedditUserName)

# Get Sample Dataframe of top 5 Posts' information
dfHeadings = {
    'Unique': [],
    'Sub': [],
    'Title': [],
    'URL': [],
    'Time': [],
    'Author': [],
    'Body': [],
    'IsSelfPost': []
}

dfPosts = pd.DataFrame(dfHeadings)
dfPosts['IsSelfPost'] = dfPosts['IsSelfPost'].astype('bool')
subredditName = 'christianity'

for indexPosts, submission in enumerate(reddit.subreddit(subredditName).hot(limit=5)):
    TempDict = {
        'Unique': submission.id,
        'Sub': subredditName,
        'Title': submission.title,
        'URL': 'https://reddit.com'+submission.permalink,
        'Time': str(datetime.datetime.fromtimestamp(submission.created_utc)),
        'Author': str(submission.author),
        'Body': submission.selftext,
        'IsSelfPost': submission.is_self
    }

    print(submission.is_self)
    dfPosts = dfPosts.append(
        TempDict, ignore_index=True)  # Append to dataframe
    print('Retrieved data for '+str(indexPosts+1)+' posts')

print(dfPosts)

# Get Sample Dataframe of author information
dfHeadingsAuthor = {
    'userName': [],
    'accountAge': [],
    'commentKarma': [],
    'linkKarma': [],
    'isMod': [],
    'numPosts': [],
    'avgCommentsToPost': []
}

dfAuthors = pd.DataFrame(dfHeadingsAuthor)
dfAuthors['isMod'] = dfAuthors['isMod'].astype('bool')

for indexAuthor, thisIndex in enumerate(dfPosts.index):
    # Get Entry Information
    thisSubmission = reddit.submission(id=dfPosts.loc[thisIndex, 'Unique'])
    thisAuthor = thisSubmission.author
    # Get Author Information
    TempDictAuthor = {}
    # Verifies that author exists and has not been suspended (as suspended accounts do not have most attributes)
    if ((thisSubmission.author is not None) and hasattr(thisAuthor, 'created_utc')):
        TempDictAuthor['userName'] = thisAuthor.name
        TempDictAuthor['accountAge'] = thisAuthor.created_utc
        TempDictAuthor['commentKarma'] = thisAuthor.comment_karma
        TempDictAuthor['linkKarma'] = thisAuthor.link_karma
        TempDictAuthor['isMod'] = thisAuthor.is_mod

        numPosts = 0
        numCommentsList = []

        # Get number of posts by the author in the past month and the average number of comments to it
        for thisAuthorPost in thisAuthor.submissions.top(time_filter="month"):
            numPosts = numPosts + 1
            numComments = 0
            for tempComment in thisAuthorPost.comments:
                # If tempComment does not have a is_submitter attribute, it is because it is a "More Comments" link
                if hasattr(tempComment, 'is_submitter'):
                    numComments = numComments + 1
                else:
                    numComments = np.nan  # For simplicity, just made this NaN as the summation is unknown unless clicking "More Comments", which is not part of this example code
            numCommentsList.append(numComments)

        TempDictAuthor['numPosts'] = numPosts
        TempDictAuthor['avgCommentsToPost'] = np.mean(numCommentsList)

    dfAuthors = dfAuthors.append(
        TempDictAuthor, ignore_index=True)  # Append to dataframe
    print('Retrieved data for '+str(indexAuthor+1)+' authors')
print(dfAuthors)

# Tasks:
# 1. Confirm retrieval of posts
# 2. Come up with
