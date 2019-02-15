import praw
import datetime
import math
import boto3
import giphy_client
from giphy_client.rest import ApiException
from Account import Account


class Reddit:
    reddit = praw.Reddit('memeEco')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                              endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")
    my_investments = dynamodb.Table('investement')

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
        for submission in self.reddit.subreddit('memeeconomy').new(limit=15):
            time_delta = (int(datetime.datetime.timestamp(datetime.datetime.today())) - submission.created_utc) / 60
            investments = 0
            submission.comments.replace_more(limit=None)
            for comment in submission.comments:
                if comment.author.name == 'MemeInvestor_bot':
                    invest_comment = comment
                    investments = self.get_investments(invest_comment)
                    break
            ratio = investments / time_delta
            meme = {'title': submission.title, 'updoots': submission.ups, 'investements': investments,
                    'time': time_delta, 'ratio': ratio, 'balance': self.account.balance}
            retour['memes'].append(meme)
            if time_delta > 10:
                break
            if ratio >= 2 and investments >= 2 and submission.ups < 10:
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
                    submission.reply(
                        '[Beep Beep Boop]({}), Here are some stats:  \n{}'.format(self.get_gif(), self.pretty_print(meme)))
        return retour

    def calculate_investement(self, ratio):
        invest_amount = math.ceil((self.account.balance / 5) * ratio)
        if invest_amount > self.account.balance or self.account.balance < 200 or invest_amount < self.account.net_worth / 100:
            invest_amount = self.account.balance
        if invest_amount < 100:
            invest_amount = 100
        return invest_amount

    def pretty_print(self, meme):
        formated_meme = ''
        for key, value in meme.items():
            if key == 'time':
                formated_meme += 'posted {} minute(s) ago  \n'.format(value)
            else:
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
