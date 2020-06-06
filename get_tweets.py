# %%
# -*- coding: utf-8 -*-
import os
import csv
import tweepy
from dotenv import load_dotenv
load_dotenv()

#  %% Twitter Login
auth = tweepy.AppAuthHandler(os.getenv('API_KEY'), os.getenv('KEY_SECRET'))
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)


#  %% Adapted from https://gist.github.com/yanofsky/5436496
# -*- coding: utf-8 -*-

#initialize a list to hold all the tweepy Tweets
alltweets = []

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name='Die_Gruenen', count=200)
#save most recent tweets
alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1

#keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
	print("getting tweets before %s" % (oldest))

	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name='Die_Gruenen', count=200, max_id=oldest)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	print("...%s tweets downloaded so far" % (len(alltweets)))

#transform the tweepy tweets into a 2D array that will populate the csv
outtweets = [[tweet.id_str, tweet.created_at, tweet.text.replace('\n', ''), tweet.entities['hashtags'], tweet.retweet_count] for tweet in alltweets]

#write the csv
with open('Die_Gruenen_tweets.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'created_at', 'text', 'hashtags', 'retweets'])
    writer.writerows(outtweets)


# %%
print(alltweets[1].retweet_count)

# %%
