import praw
import os
from AI import AI


class Stats:
    reddit = praw.Reddit(client_id=os.environ['STAT_CLIENT_ID'],
                         client_secret=os.environ['STAT_CLIENT_SECRET'], password=os.environ['STAT_REDDIT_PASSWORD'],
                         user_agent=os.environ['USER_AGENT'], username=os.environ['STAT_REDDIT_USERNAME'])
    ai = AI()

    def post_stats(self, meme):
        submission = self.reddit.submission(meme['id'])
        prediction = self.ai.predict(meme)[0].tolist()
        max_value = prediction.index(max(prediction))
        reply = "I'm testing a new machine learning feature!  \n I'm {} sure this post will ".format(str(round(prediction[max_value] * 100, 1)) + '%')
        if max is 0:
                reply += 'not make a profit'
        elif max is 1:
            reply += "make some profit"
        else:
            reply += "make huge profit"
        submission.reply(reply)
