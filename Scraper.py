import pandas as pd

# reads NFL table from teamrankings.com into pandas dataframe
def df(tag, link):
    data = pd.read_html(link)
    data = data[0].dropna() # format single list into dataframe with columns
    data = data.drop(['Rank'], axis=1)

    for col in data.drop(['Team'], axis=1).columns: #Rename every column except 'Team'
        data.rename({col: tag + col.replace(" ", "")}, axis=1, inplace=True)
    
    return data

OffPPP_df = df('OffPPP', 'https://www.teamrankings.com/nfl/stat/points-per-game?date=2019-12-29')
DefPPP_df = df('DefPPP', 'https://www.teamrankings.com/nfl/stat/opponent-points-per-game?date=2019-12-29')

print(OffPPP_df)
print(DefPPP_df)

'''
# Offensive PPP

tag = 'OffPPP'

OffPPP_df = pd.read_html("https://www.teamrankings.com/nfl/stat/points-per-game?date=2019-12-29")
OffPPP_df = OffPPP_df[0].dropna() # format single list into dataframe with columns
OffPPP_df = OffPPP_df.drop(['Rank'], axis=1)

for col in OffPPP_df.drop(['Team'], axis=1).columns: # Rename every column except 'Team'
    OffPPP_df.rename({col: tag + col.replace(" ", "")}, axis=1, inplace=True)

# Defensive PPP

tag = 'DefPPP'

DefPPP_df = pd.read_html("https://www.teamrankings.com/nfl/stat/opponent-points-per-game?date=2019-12-29")
DefPPP_df = DefPPP_df[0].dropna()
DefPPP_df = DefPPP_df.drop(['Rank'], axis=1)

for col in DefPPP_df.drop(['Team'], axis=1).columns: # Rename every column except 'Team'
    DefPPP_df.rename({col: tag + col.replace(" ", "")}, axis=1, inplace=True)

print(OffPPP_df)
print(DefPPP_df)
'''