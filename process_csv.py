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

#  %% Load
afd = load_csv('afd.csv')

# %% Transorm
afd_new = []
vips = []
for entry in afd:
    try:
        user = load_csv('users/'+entry[0]+".csv")
        if len(user) > 5000:
            afd_new.append(transform_row(entry[0], "afd"))
            vips.append(entry[0])
    except:
        print("Problem finding "+str(user))
        continue

# %%
# Nehme vip raus
i = 1
for vip in vips:
    print("Doing "+str(vip)+" "+str(i)+"/"+str(len(vips)))
    for check in vips:
        file = load_csv('users/'+check+".csv")
        #print("|____ Doing "+check)
        try:
            for line in file:
                if vip == line[0]:
                    afd_new.append(transform_row(vip, check))
                    #print(vip+" in "+check+".csv")
        except:
            continue
    i+=1

print("Saving...")
save_result('afd_transformed.csv', afd_new)
# %%
