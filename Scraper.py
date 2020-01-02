import pandas as pd
import numpy as np
from sys import exit

NUM_COLUMNS = 15

# function that reads NFL table from teamrankings.com into pandas dataframe
def df(tag, link):
    data = pd.read_html(link)
    data = data[0].dropna() # format single list into dataframe with columns
    data = data.drop(['Rank'], axis=1)

    for col in data.drop(['Team'], axis=1).columns: #Rename every column except 'Team'
        data.rename({col: tag + col.replace(" ", "")}, axis=1, inplace=True)
    
    return data

# Read in CSV
scores_df = pd.read_csv('nfl-games.csv')

if len(scores_df.columns) != NUM_COLUMNS:
    print('Invalid number of columns in CSV, should contain') 
    print('Week, Day, Date, Year, Time,')
    print('Winner/tie, Location, Loser/tie, Boxscore, PtsW,')
    print('PtsL, YdsW, TOW, YdsL, TOL')
    exit()

# Preprocessing
scores_df = scores_df.drop(['Boxscore', 'YdsW', 'TOW', 'YdsL', 'TOL'], axis=1) # drop unused information

# Home/Away preprocessing
scores_df.loc[scores_df['Location'] == '@', 'HomeTeam'] = scores_df['Loser/tie']
scores_df.loc[scores_df['Location'] == '@', 'AwayTeam'] = scores_df['Winner/tie']
scores_df.loc[scores_df['Location'].isnull(), 'HomeTeam'] = scores_df['Winner/tie']
scores_df.loc[scores_df['Location'].isnull(), 'AwayTeam'] = scores_df['Loser/tie']
scores_df.loc[scores_df['Location'] == '@', 'PtsHome'] = scores_df['PtsL']
scores_df.loc[scores_df['Location'] == '@', 'PtsAway'] = scores_df['PtsW']
scores_df.loc[scores_df['Location'].isnull(), 'PtsHome'] = scores_df['PtsW']
scores_df.loc[scores_df['Location'].isnull(), 'PtsAway'] = scores_df['PtsL']
scores_df = scores_df.drop(['Winner/tie', 'Location', 'Loser/tie', 'PtsW', 'PtsL'], axis=1)

# Date preprocessing
scores_df[['Month', 'MonthDay']] = scores_df['Date'].str.split(expand=True) # split <month> <day> into 2 columns
months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
    'September':9, 'October':10, 'November':11, 'December':12} # dictionary to convert string to number
scores_df['Month'] = scores_df['Month'].map(months) # convert months to numbers
scores_df['DateCode'] = scores_df['Year'].astype(str) + '-' + scores_df['Month'].astype(str) + '-' + scores_df['MonthDay'].astype(str)
scores_df = scores_df.drop(['Date', 'Month', 'MonthDay'], axis=1)



print(scores_df)

'''
# Read in teamrankings tables
OffPPG_df = df('OffPPG', 'https://www.teamrankings.com/nfl/stat/points-per-game?date=2019-12-29')
DefPPG_df = df('DefPPG', 'https://www.teamrankings.com/nfl/stat/opponent-points-per-game?date=2019-12-29')

data = OffPPG_df.set_index('Team').join(DefPPG_df.set_index('Team'))

print(data)
'''