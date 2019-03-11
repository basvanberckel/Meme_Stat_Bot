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
        prediction = self.ai.predict(meme)[0]
        reply = "I'm testing a new machine learning feature!  \n"
        if prediction[0] >= prediction[1]  and prediction[0] >= prediction[2]:
                reply += "I'm {} sure this post will not make a profit".format(str(round(prediction[0] * 100, 1)) + '%')
        elif prediction[1] >= prediction[0] and prediction[1] >= prediction[2]:
            reply += "I'm {} sure this post will make some profit".format(str(round(prediction[0] * 100, 1)) + '%')
        else:
            reply += "I'm {} sure this post will make a big profit".format(str(round(prediction[0] * 100, 1)) + '%')
