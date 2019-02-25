import praw
import datetime
import math
import boto3
import giphy_client
from giphy_client.rest import ApiException
from Account import Account
from praw.models import Comment
import os


class Reddit:
    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'], password=os.environ['REDDIT_PASSWORD'],
                         user_agent=os.environ['USER_AGENT'], username=os.environ['REDDIT_USERNAME'])
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                              endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")
    my_investments = dynamodb.Table('investement')
    data = dynamodb.Table('meme_data')
    collect_data = True

    def __init__(self):
        self.account = Account('bubulle099', self)

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

    def get_inbox(self):
        return self.reddit.inbox.all(limit=None)

    def get_unread(self):
        return self.reddit.inbox.unread(limit=None)

    def scan(self):
        retour = {'memes': [], 'invested': [], 'balance': self.account.balance}
        if self.account.balance > 100 or self.collect_data:
            for submission in self.reddit.subreddit('memeeconomy').new(limit=15):
                time_delta = (int(datetime.datetime.timestamp(datetime.datetime.today())) - submission.created_utc) / 60
                posted_at = datetime.datetime.fromtimestamp(submission.created_utc).strftime('%H:%M:%S')
                if time_delta > 10:
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
                        'flair': str(submission.author_flair_text), }
                if self.collect_data and 3 <= time_delta < 4:
                    self.data.put_item(Item=meme)
                retour['memes'].append(meme)

                if ratio >= 2 and investments >= 2 and submission.ups < 10 and self.account.balance > 100:
                    invested = self.already_invested(submission.id)
                    if not invested:
                        invest_amount = self.calculate_investement(ratio)
                        meme.update({'balancePercentage': str(invest_amount / self.account.balance * 100) + '%'})
                        submission.downvote()
                        invest_comment.reply('!invest {}'.format(invest_amount))
                        self.my_investments.put_item(Item={"id": submission.id})
                        self.account.balance -= invest_amount
                        retour['invested'].append(submission.id)
                        del meme['ratio']
                        del meme['id']
                        del meme['time_stamp']
                        submission.reply(
                            '[Beep Beep Boop]({}), Here are some stats:  \n{}'.format(self.get_gif(),
                                                                                      self.pretty_print(meme)))
        return retour

    def calculate_investement(self, ratio):
        invest_amount = math.ceil((self.account.balance / 5) * ratio)
        if invest_amount > self.account.balance or self.account.balance < 200 or invest_amount < self.account.net_worth / 100:
            invest_amount = self.account.balance
        if invest_amount < 100:
            invest_amount = 100
        # ALL IN NIBBA
        invest_amount = self.account.balance
        return invest_amount

    def pretty_print(self, meme):
        formated_meme = ''
        for key, value in meme.items():
                formated_meme += '{}: {}  \n'.format(key, value)
        return formated_meme

    def already_invested(self, sub_id):
        try:
            response = self.my_investments.get_item(Key={
                'id': sub_id
            })
            item = response['Item']
        except KeyError as e:
            item = None
        return item is not None

    def get_gif(self):
        api_instance = giphy_client.DefaultApi()
        api_key = 'crye2EEX88YGhcJkOOnx1TnVG0jBnreV'  # str | Giphy API Key.
        tag = 'wolf-of-wall-street'  # str | Filters results by specified tag. (optional)
        fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

        try:
            # Random Endpoint
            api_response = api_instance.gifs_random_get(api_key, tag=tag, fmt=fmt)
            return api_response.data._image_url
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)

    def upvote_invested_memes(self):
        unread_messages = []
        for item in self.reddit.inbox.unread(limit=None):
            if isinstance(item, Comment) and item.author.name == 'MemeInvestor_bot' and 'invested' in item.body:
                item.submission.upvote()
                unread_messages.append(item)
                item.delete()
        self.reddit.inbox.mark_read(unread_messages)
