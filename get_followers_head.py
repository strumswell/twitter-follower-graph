import csv
from bluebird import BlueBird 

head_account = 'AfD'

def get_followers(username):
    return BlueBird().get_followers(username)    

def save_result(_filename, _followers):
    with open('/Users/philippbolte/AfDTwitter/'+_filename+".csv",'w', newline='') as file:
        i = 1
        for _user in _followers:
            print(str(i)+ ": " + _user)
            file.write(_user+"\n")
            i += 1

followers = get_followers(head_account)
print("Got all follower of "+head_account)
save_result(head_account, followers)