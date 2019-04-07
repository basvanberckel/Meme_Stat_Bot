import praw
import datetime
import os
from MemeData import MemeData
from Stats import Stats


class Reddit:
    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'], password=os.environ['REDDIT_PASSWORD'],
                         user_agent=os.environ['USER_AGENT'], username=os.environ['REDDIT_USERNAME'])
    data = MemeData()
    collect_data = True
    stats = Stats(reddit)

    def get_investments(self, comment):
        cnt = 0
        comment.replies.replace_more(limit=100)
        for reply in comment.replies:
            if '!invest' in reply.body:
                cnt += 1
                for reply in reply.replies:
                    if reply.author.name == 'MemeInvestor_bot':
                        cnt += self.get_investments(reply)
        return cnt

    def scan(self):
        retour = []
        for submission in self.reddit.subreddit('memeeconomy').new(limit=15):
            time_delta = (int(datetime.datetime.timestamp(datetime.datetime.today())) - submission.created_utc) / 60
            posted_at = datetime.datetime.fromtimestamp(submission.created_utc).strftime('%H:%M:%S')
            if time_delta > 4:
                break
            investments = 0
            submission.comments.replace_more(limit=None)
            for comment in submission.comments:
                if comment.author.name == 'MemeInvestor_bot':
                    invest_comment = comment
                    investments = self.get_investments(invest_comment)
                    break
            ratio = investments / time_delta
            meme = {'id': str(submission.id), 'title': submission.title, 'updoots': submission.ups,
                    'investements': investments,
                    'time': posted_at, 'time_stamp': str(submission.created_utc), 'ratio': str(ratio),
                    'flair': str(submission.author_flair_text), 'upvotes': None}

            if self.collect_data and 3 <= time_delta < 4:
                #self.stats.post_stats(meme)
                self.data.add(meme)
            retour.append(meme)

        return retour
