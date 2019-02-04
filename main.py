#!/usr/bin/env python
import praw
import datetime
import json
import requests
import math
from praw.models import Comment


def get_account_info(account):
    headers = {'Content-Type': 'application/json'}
    api_url = 'https://memes.market/api/investor/{}'.format(account)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_ranking(account_name):
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


def get_balance(account):
    info = get_account_info(account)
    if info:
        return info['balance']
    return None

def get_net_worth(account):
    info = get_account_info(account)
    if info:
        return info['networth']
    return None


def get_investments(comment):
    cnt = 0
    comment.replies.replace_more(limit=100)
    for reply in invest_comment.replies:
        if '!invest' in reply.body:
            cnt += 1
    return cnt


def upvote_invested_memes():
    unread_messages = []
    for item in reddit.inbox.unread(limit=None):
        if isinstance(item, Comment) and item.author.name == 'MemeInvestor_bot':
            item.submission.upvote()
            unread_messages.append(item)
            item.delete()
    reddit.inbox.mark_read(unread_messages)


if __name__ == '__main__':
    # Create the Reddit instance
    reddit = praw.Reddit('memeEco')
    with open('data.json') as f:
        data = json.load(f)
    subreddit = reddit.subreddit('memeeconomy')
    now = int(datetime.datetime.timestamp(datetime.datetime.today()))
    balance = get_balance('bubulle099')
    if not balance:
        balance = data['balance']
    net_worth = get_net_worth('bubulle099')
    if not net_worth:
        net_worth= data['_Net_worth']
    print('balance: {}'.format(balance))
    if balance and balance >= 100:
        invest = []
        for submission in subreddit.new(limit=50):
            print(submission.title)
            date = submission.created_utc
            time_delta = (now - date)/60
            votes = submission.ups
            for comment in submission.comments:
                if comment.author.name == 'MemeInvestor_bot':
                    invest_comment = comment
                    break
            try :
                invest_comment
            except NameError:
                print("     No bot answer")
            else:
                investments = get_investments(invest_comment)
                ratio = investments/time_delta
                invest_amount = math.ceil((balance/5) * ratio)
                print('     updoots: {}\n     investements:{}\n     ratio: {} \n     time:{}'.format(submission.ups, investments, ratio, time_delta))
                if time_delta > 10:
                    break
                if invest_amount > balance or balance < 200 or invest_amount < net_worth/100:
                    invest_amount = balance
                if invest_amount < 100:
                    invest_amount = 100
                if submission.id not in data['invested'] and ratio >= 1.4 and votes < 10:
                    submission.downvote()
                    invest_comment.reply('!invest {}'.format(invest_amount))
                    print('invested {}'.format(invest_amount))
                    data['invested'].append(submission.id)
                    balance -= invest_amount
                    invest.append(submission)
                    with open('data.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4, sort_keys=True)
        #data['_Ranking'] = get_ranking('bubulle099')
        data['_Net_worth'] = net_worth
        data['_Last_Scan'] = str(datetime.datetime.now())

    upvote_invested_memes()
    data['balance'] = balance
    print('invested in: {}'.format(invest))
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)