import praw
import os
from joblib import dump, load
#from AI import AI
import numpy
import copy


class Stats:
    reddit = praw.Reddit(client_id=os.environ['STAT_CLIENT_ID'],
                         client_secret=os.environ['STAT_CLIENT_SECRET'], password=os.environ['STAT_REDDIT_PASSWORD'],
                         user_agent=os.environ['USER_AGENT'], username=os.environ['STAT_REDDIT_USERNAME'])
    clf = load('model.joblib')
    #ai = AI()


    def post_stats(self, meme):
        submission = self.reddit.submission(meme['id'])
        prediction = self.predict(meme)[0].tolist()
        max_value = prediction.index(max(prediction))
        reply = "I'm testing a new machine learning feature!  \nI'm {} sure this post will ".format(str(round(prediction[max_value] * 100, 1)) + '%')
        print(prediction)
        if max_value == 0:
                reply += 'not make profit'
        elif max_value == 1:
            reply+= "make profit"
        #submission.reply(reply)

    def extract_primitive_meme(self, row):
        row.pop('flair', None)
        row.pop('upvotes', None)
        row.pop('time_stamp', None)
        row.pop('ratio', None)
        ftr = [3600, 60, 1]
        row['time'] = sum([a * b for a, b in zip(ftr, map(int, row['time'].split(':')))]) / (60 * 60)
        row.pop('time', None)
        row.pop('id', None)
        row.pop('title', None)
        return row

    def predict(self, meme):
        meme = self.extract_primitive_meme(copy.copy(meme))
        row = []
        for value in meme.values():
            row.append(float(value))
        row = numpy.array(row).reshape(1, -1)
        prediction = self.clf.predict_proba(row)
        return prediction
