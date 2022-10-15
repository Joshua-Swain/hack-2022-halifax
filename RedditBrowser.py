import praw
import pandas as pd
import numpy as np
from  datetime import datetime

class RedditBrowser:

    POST_COLUMNS = {
        'Unique': [],
        'Sub': [],
        'Title': [],
        'URL': [],
        'Time': [],
        'Author': [],
        'Body': [],
        'IsSelfPost': []
    }

    AUTHOR_COLUMNS = {
        'userName': [],
        'accountAge': [],
        'commentKarma': [],
        'linkKarma': [],
        'isMod': [],
        'numPosts': [],
        'avgCommentsToPost': []
    }

    def __init__(self, reddit):
        self.reddit = reddit

    def retrieve_posts(self, subreddit):
        posts_df = pd.DataFrame(self.POST_COLUMNS)
        posts_df['IsSelfPost'] = posts_df['IsSelfPost'].astype('bool')

        for i, post in enumerate(self.reddit.subreddit(subreddit).hot(limit=5)):
            post_data = {
                'Unique': post.id,
                'Sub': subreddit,
                'Title': post.title,
                'URL': 'https://reddit.com' + post.permalink,
                'Time': str(datetime.fromtimestamp(post.created_utc)),
                'Author': str(post.author),
                'Body': post.selftext,
                'IsSelfPost': post.is_self
            }

            print(post.is_self)
            posts_df = posts_df.append(
                post_data, ignore_index=True)
            print('Retrieved data for ' + str(i + 1) + ' posts')

        print(posts_df)
        return posts_df

    def retrieve_authors(self, posts_df):
        authors_df = pd.DataFrame(self.AUTHOR_COLUMNS)
        authors_df['isMod'] = authors_df['isMod'].astype('bool')

        for i, thisIndex in enumerate(posts_df.index):
            # Get Entry Information
            submission = self.reddit.submission(id=posts_df.loc[thisIndex, 'Unique'])
            author = submission.author
            # Get Author Information
            author_data = {}
            # Verifies that author exists and has not been suspended (as suspended accounts do not have most attributes)
            if ((submission.author is not None) and hasattr(author, 'created_utc')):
                author_data['userName'] = author.name
                author_data['accountAge'] = author.created_utc
                author_data['commentKarma'] = author.comment_karma
                author_data['linkKarma'] = author.link_karma
                author_data['isMod'] = author.is_mod

                numPosts = 0
                numCommentsList = []

                # Get number of posts by the author in the past month and the average number of comments to it
                for thisAuthorPost in author.submissions.top(time_filter="month"):
                    numPosts = numPosts + 1
                    numComments = 0
                    for comment in thisAuthorPost.comments:
                        # If tempComment does not have a is_submitter attribute, it is because it is a "More Comments" link
                        if hasattr(comment, 'is_submitter'):
                            numComments = numComments + 1
                        else:
                            numComments = np.nan  # For simplicity, just made this NaN as the summation is unknown unless clicking "More Comments", which is not part of this example code
                    numCommentsList.append(numComments)

                author_data['numPosts'] = numPosts
                author_data['avgCommentsToPost'] = np.mean(numCommentsList)

            authors_df = authors_df.append(
                author_data, ignore_index=True)  # Append to dataframe
            print('Retrieved data for '+str(i+1)+' authors')

        print(authors_df)
        return authors_df