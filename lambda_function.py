import praw
import datetime
import requests
import math
import boto3
from praw.models import Comment


def get_account_info(account):
    return None
    headers = {'Content-Type': 'application/json'}
    api_url = 'https://memes.market/api/investor/{}'.format(account)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def exists(id, table):
    try:
        response = table.get_item(Key={
            'id': id
        })
        item = response['Item']
    except KeyError as e:
        item = None
    return item


def get_ranking(account_name):
    return None
    headers = {'Content-Type': 'application/json'}
    api_url = 'https://memes.market/api/investors/top?per_page=100'
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        ranking = json.loads(response.content.decode('utf-8'))
        for index, account in enumerate(ranking):
            if account['name'] == account_name:
                print('Rank: {} '.format(++index))
                return ++index
    else:
        return None


def get_balance(account,reddit):
    info = get_account_info(account)
    if info:
        return info['balance']
    else:
        for item in reddit.inbox.all(limit=None):
            if isinstance(item, Comment) and item.author.name == 'MemeInvestor_bot':
                message = item.body.split('**', 1)[-1].split('Meme',1)[0]
                balance = list(filter(str.isdigit, message))
                balance_str = ''
                for i in range(len(balance)):
                    balance_str += str(balance[i])
                try:
                    balance = int(balance_str)
                    return balance
                except ValueError:
                    print('no balance')

    return None


def get_net_worth(account):
    info = get_account_info(account)
    if info:
        return info['networth']
    else:
        return 700000


def get_investments(comment):
    cnt = 0
    comment.replies.replace_more(limit=100)
    for reply in comment.replies:
        if '!invest' in reply.body:
            cnt += 1
    return cnt


def upvote_invested_memes(reddit):
    unread_messages = []
    for item in reddit.inbox.unread(limit=None):
        if isinstance(item, Comment) and item.author.name == 'MemeInvestor_bot':
            item.submission.upvote()
            unread_messages.append(item)
            item.delete()
    reddit.inbox.mark_read(unread_messages)


def lambda_handler(event, context):
    # Create the Reddit instance from praw.ini Memeeco profile
    reddit = praw.Reddit('memeEco')
    balance = get_balance('bubulle099',reddit)
    net_worth = get_net_worth('bubulle099')
    retour = {'memes': [], 'invested': [], 'balance': balance}
    if balance and balance >= 100:
        invest = []
        dynamodb = boto3.resource('dynamodb',region_name='eu-west-1', endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")
        table = dynamodb.Table('investement')
        for submission in reddit.subreddit('memeeconomy').new(limit=15):
            time_delta = (int(datetime.datetime.timestamp(datetime.datetime.today())) - submission.created_utc) / 60
            for comment in submission.comments:
                if comment.author.name == 'MemeInvestor_bot':
                    invest_comment = comment
                    break
            try:
                invest_comment
            except NameError:
                print("No bot answer")
            else:
                investments = get_investments(invest_comment)
                ratio = investments / time_delta
                retour['memes'].append({'title':submission.title,'updoots':submission.ups,'ratio':ratio,'time':time_delta})
                if time_delta > 10:
                    break
                if ratio >= 1.6 and investments > 2 and submission.ups < 10:
                    item = exists(submission.id,table)
                    if item is None:
                        invest_amount = math.ceil((balance / 5) * ratio)
                        if invest_amount > balance or balance < 200 or invest_amount < net_worth / 100:
                            invest_amount = balance
                        if invest_amount < 100:
                            invest_amount = 100
                        submission.downvote()
                        invest_comment.reply('!invest {}'.format(invest_amount))
                        balance -= invest_amount
                        print('INVESTED')
                        table.put_item(Item={"id": submission.id})
                        retour['invested'].append(submission.id)
    upvote_invested_memes(reddit)
    return retour
