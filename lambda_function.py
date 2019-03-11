from Reddit import Reddit
from AI import AI


def lambda_handler(event, context):
    #ai =AI()
    red = Reddit()
    red.upvote_invested_memes()
    return red.scan()


if __name__ == "__main__":
    print(lambda_handler(None, None))
