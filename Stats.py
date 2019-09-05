from MemeData import MemeData


class Stats:
    def __init__(self, reddit):
        self.reddit = reddit
        self.data = MemeData()

    def post_stats(self, meme):
        submission = self.reddit.submission(meme['id'])
        similar = self.data.get_similar(meme)
        size = len(similar['loss']) + len(similar['broke even'])
        if size > 0:
            reply = 'Found {} similar submissions  \n\n {}% turned into a loss  \n\n {}% of them at least broke even  \n\n {}% made good profit'.format(
                size,
                round(len(similar['loss']) / size * 100, 1),
                round(len(similar['broke even']) / size * 100, 1),
                round(len(similar['big profit']) / size * 100, 1))
            self.reddit.submission(submission.id).reply(
                reply + '  \n\n[source code](https://github.com/Caribosaurus/Meme_Stat_Bot)')
        print('found {} posts at {} investements and {} updoots'.format(size, meme['investements'],
                                                                        meme['updoots']))
