import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

class MemeData:
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                              endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")
    my_investments = dynamodb.Table('investement')
    data = dynamodb.Table('meme_data')

    def add(self, meme):
        self.data.put_item(Item=meme)

    def get_similar(self, meme):
        feLoss = Key('investements').eq(meme['investements']) & Key('updoots').between(
            meme['updoots'] - 1, meme['updoots'] + 1) & Key('factor').between(0, round(Decimal(0.90), 2))
        feProfit = Key('investements').eq(meme['investements']) & Key('updoots').between(
            meme['updoots'] - 1, meme['updoots'] + 1) & Key('factor').between(1, 5)
        feBigProfit = Key('investements').eq(meme['investements']) & Key('updoots').between(
            meme['updoots'] - 1, meme['updoots'] + 1) & Key('factor').between(2, 5)
        response ={'loss':self.data.scan(FilterExpression=feLoss)['Items'],
                   'broke even':self.data.scan(FilterExpression=feProfit)['Items'],
                   'big profit':self.data.scan(FilterExpression=feBigProfit)['Items']}
        return response

    def get_data(self):
        fe =  Key('upvotes').gte(0) & Key('factor').gte(0)
        return self.data.scan(FilterExpression=fe)['Items']
