## How connections are analyzed
To analyze the connections between the followers of an account, I did the following:

1. Scrape followers of head account
2. Scrape followers of all follower of the head account and save a csv for each individual user.
3. Go through each csv and look for other users that follow the head account (see process_csv_optimised.py)

The result of those steps get saved into a final csv. The csvs for @AfD and @DieGruenen you can find in this folder.