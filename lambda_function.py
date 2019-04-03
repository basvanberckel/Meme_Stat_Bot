from Reddit import Reddit

def lambda_handler(event, context):
    red = Reddit()
    return red.scan()


if __name__ == "__main__":
    print(lambda_handler(None, None))
