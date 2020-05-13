'''
README!
This is a mess, I know. Gonna refactor soon.
'''
#  %%
import pandas as pd
import csv
from bluebird import BlueBird 

head_account = 'AfD'

def get_followers(username):
    return BlueBird().get_followers(username)    

def save_result(_filename, _followers):
    with open('/Users/philippbolte/Desktop/WIM2/PredictiveAnalytics/PredAnaUebung1/TwintDemo/users/'+_filename+'.csv', 'w', newline='') as file:
        for _user in _followers:
            file.write(_user+"\n")

def load_csv():
    with open('/Users/philippbolte/Desktop/WIM2/PredictiveAnalytics/PredAnaUebung1/TwintDemo/afd_followers.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data

# Get followers of head account
followers = get_followers(head_account)
print("Got all follower of "+head_account)
save_result(head_account, followers)
print("Count:" + str(len(followers)))

# Get their followers
#  %%
start_time = time.time()
print("Now for its followers...")
followers = load_csv()
followers = followers[:5]
i = 1
for user in followers:
    print("Scraping "+user[0]+" ("+str(i)+"/"+str(len(followers))+")")
    save_result(user[0], get_followers(user[0]))
    i += 1



#  %%
'''
for user in followers:
    print("Scraping "+user+"...")
    user_followers = get_followers(user)
    save_result(user, user_followers)
    time.sleep(1)
print("--- %s seconds ---" % (time.time() - start_time))
'''



# %%
