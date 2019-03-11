import praw
import os
from AI import AI


class Stats:
    reddit = praw.Reddit(client_id=os.environ['STAT_CLIENT_ID'],
                              client_secret=os.environ['STAT_CLIENT_SECRET'], password=os.environ['STAT_REDDIT_PASSWORD'],
                              user_agent=os.environ['USER_AGENT'], username=os.environ['STAT_REDDIT_USERNAME'])
    ai = AI()

    def post_stats(self,meme):
        submission = self.reddit.submission(meme['id'])
        prediction = self.ai.predict(meme)
        print(prediction)
        #submission.reply(prediction)
