import praw
import os
from MemeData import MemeData


class Stats:
    reddit = praw.Reddit(client_id=os.environ['STAT_CLIENT_ID'],
                              client_secret=os.environ['STAT_CLIENT_SECRET'], password=os.environ['STAT_REDDIT_PASSWORD'],
                              user_agent=os.environ['USER_AGENT'], username=os.environ['STAT_REDDIT_USERNAME'])
    data = MemeData()
    def post_stats(self,meme):
        submission = self.reddit.submission(meme['id'])
        similar = self.data.get_similar(meme)
        size = len(similar['loss']) + len(similar['broke even'])
        if size > 0:
            self.reddit.submission(submission.id).reply(
                'Found {} similar memes  \n {}% turned into a loss  \n {}% of them at least broke even  \n {}% made good profit'.format(
                    size,
                    round(len(similar['loss']) / size * 100, 1),
                    round(len(similar['broke even']) / size * 100, 1),
                    round(len(similar['big profit']) / size * 100, 1)))
        print('found {} posts at {} investements and {} updoots'.format(size, meme['investements'],
                                                                        meme['updoots']))
