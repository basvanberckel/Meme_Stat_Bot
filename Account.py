from praw.models import Comment
import requests
import json


class Account:
    info = None

    def __init__(self, name, reddit):
        self.reddit = reddit
        self.name = name
        self.net_worth = self.get_net_worth()
        self.balance = self.get_balance()

    def get_balance(self):
        info = self.get_account_info()
        if info:
            return info['balance']
        else:
            for item in self.reddit.get_inbox():
                if isinstance(item, Comment) and item.author.name == 'MemeInvestor_bot':
                    if 'balance is' in item.body:
                        message = item.body.split('**', 1)[-1].split('Meme', 1)[0]
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

    def get_net_worth(self):
        info = self.get_account_info()
        if info:
            return info['networth']
        else:
            return 2 * 10 ^ 11

    def get_account_info(self):
        return None
        if self.info is None:
            headers = {'Content-Type': 'application/json'}
            api_url = 'https://memes.market/api/investor/{}'.format(self.name)
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                self.info = json.loads(response.content.decode('utf-8'))
        return self.info
