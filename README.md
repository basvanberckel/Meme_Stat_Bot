### Praw.ini

create a praw.ini looking like so.

```
[DEFAULT]
# A boolean to indicate whether or not to check for package updates.
check_for_updates=False

# Object to kind mappings
comment_kind=t1
message_kind=t4
redditor_kind=t2
submission_kind=t3
subreddit_kind=t5
trophy_kind=t6

# The URL prefix for OAuth-related requests.
oauth_url=https://oauth.reddit.com

# The URL prefix for regular requests.
reddit_url=https://www.reddit.com

# The URL prefix for short URLs.
short_url=https://redd.it

[memeEco]
client_id=YOUR CLIENT ID
client_secret=YOUR SECRET
password=ACCOUNT PASSWORD
username=ACCOUNT NAME
user_agent= A NAME
```