#  %% Imports
import csv

def load_csv(_filename):
    with open('/Users/philippbolte/AfDTwitter/'+_filename, newline='') as f:       
        reader = csv.reader(f)
        data = list(reader)
        return data
def save_result(_filename, _data):
    with open('/Users/philippbolte/AfDTwitter/'+_filename, 'w', newline='') as file:
        for _connection in _data:
            file.write(_connection+"\n")

def transform_row(_entry, _add):
    return str(_entry)+";"+_add

#  %% Load follower
afd = load_csv('afd.csv')

# %% Get relevant users
afd_new = []
vips = []
for entry in afd:
    try:
        user = load_csv('users/'+entry[0]+".csv")
        if len(user) > 5000:
            afd_new.append(transform_row(entry[0], "afd"))
            vips.append(entry[0])
    except:
        print("Problem finding "+str(user)) # Probably deleted their accounts before scraping 2nd level followers 
        continue

# %%
# Check relations between vips
# ----------------------------------------------------------------
# Optimised version. Seems to be 20x faster and seems to produce 
# the same results in a test with a smaller data set
i = 1
for vip in vips: # Get a vip
    print("Doing "+str(vip)+" "+str(i)+"/"+str(len(vips)))
    file = load_csv('users/'+vip+".csv")
    file = [line[0] for line in file if line != []] # Restructure list
    for check in vips: # Check if the other vips are in the file
        if check in file:
            afd_new.append(transform_row(check, vip))
    i += 1

# %% Save result
print("Saving...")
save_result('afd_transformed_allover5k_optimised.csv', afd_new)
# %%
