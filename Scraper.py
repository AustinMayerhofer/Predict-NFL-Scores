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

data = OffPPP_df.set_index('Team').join(DefPPP_df.set_index('Team'))
print(data)