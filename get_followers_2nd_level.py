import csv
from bluebird import BlueBird

bb = BlueBird()

def get_followers(username):
    return bb.get_followers(username)

def save_result(_filename, _followers):
    with open('/home/philipp/tw-scraper/gruene/users/'+_filename+'.csv', 'w', newline='') as file:
        for _user in _followers:
            file.write(_user+"\n")

def load_csv():
    with open('/home/philipp/tw-scraper/gruene/gruene1.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data


print("Now for its followers...")
followers = load_csv() # containing all usernames that follow the head account
i = 1
for user in followers:
    try:
        print("Scraping "+user[0]+" ("+str(i)+"/"+str(len(followers))+")")
        save_result(user[0], get_followers(user[0]))
    except: 
        save_result(user[0], [''])
        print('Error with user...') # Most of the time the user deletet their account
    i += 1