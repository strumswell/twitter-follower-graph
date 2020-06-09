# %%
# -*- coding: utf-8 -*-
import os
import csv
import tweepy
from dotenv import load_dotenv
load_dotenv()

def load_csv(_filename):
    with open('/Users/philippbolte/Documents/FollowerNetworkTwitter/data/tweets/'+_filename, newline='') as f:       
        reader = csv.reader(f)
        data = list(reader)
        return data

#  %% Twitter Login
auth = tweepy.AppAuthHandler(os.getenv('API_KEY'), os.getenv('KEY_SECRET'))
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)

#  %% Adapted from https://gist.github.com/yanofsky/5436496
# -*- coding: utf-8 -*-
influential_users_by_party = [{'AfD': load_csv('AfD_cluster/influential_users.csv')},{'Die_Gruenen': load_csv('Die_Gruenen_cluster/influential_users.csv')}]

for influential_user in influential_users_by_party:
	party = list(influential_user.keys())[0]
	users = list(influential_user.values())[0]
	for user in users:
		print('Getting tweets of: ' + user[0])
		#initialize a list to hold all the tweepy Tweets
		alltweets = []

		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name=user[0], count=200)
		#save most recent tweets
		alltweets.extend(new_tweets)

		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print("getting tweets before %s" % (oldest))

			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name=user[0], count=200, max_id=oldest)

			#save most recent tweets
			alltweets.extend(new_tweets)

			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1

			print("...%s tweets downloaded so far" % (len(alltweets)))

		#transform the tweepy tweets into a 2D array that will populate the csv
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text.replace('\n', ''), tweet.entities['hashtags'], tweet.retweet_count] for tweet in alltweets]

		#write the csv
		with open('/Users/philippbolte/Documents/FollowerNetworkTwitter/data/tweets/'+party+'_cluster/'+user[1]+'/'+user[0]+'_tweets.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerow(['id', 'created_at', 'text', 'hashtags', 'retweets'])
			writer.writerows(outtweets)


# %%
