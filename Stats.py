from joblib import load
import numpy
import copy


class Stats:
    def __init__(self,reddit):
        self.reddit = reddit

    clf = load('model.joblib')

    def post_stats(self, meme):
        prediction = self.predict(meme)[0].tolist()
        if prediction[1]>0.85:
            reply = "Beep Beep Boop  \nI'm {} sure this post will make profit ".format(
                str(round(prediction[1] * 100, 1)) + '%')
            self.reddit.submission(meme['id']).reply(reply)
        return prediction

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
