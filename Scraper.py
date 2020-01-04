import pandas as pd
import numpy as np
from sys import exit

NUM_COLUMNS = 15 # number of columns required in csv file
LINK_PREFIX = 'https://www.teamrankings.com/nfl/stat/' # link prefix for data scrape automation
STATS = ['points-per-game', 'opponent-points-per-game', 'turnover-margin-per-game'] # stats to use in model
FIRST_WEEK = 8 # first week to start using scores for model

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

# Preprocessing unused columns
scores_df = scores_df.drop(['Boxscore', 'YdsW', 'TOW', 'YdsL', 'TOL'], axis=1)

# Take out games from certain weeks
scores_df = scores_df[scores_df['Week'] >= FIRST_WEEK]

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

# Team name preprocessing (change sports-reference team name to teamrankings.com team name)
teamnames_2003_2015 = {'Arizona Cardinals':'Arizona', 'Atlanta Falcons':'Atlanta', 'Baltimore Ravens':'Baltimore', 'Buffalo Bills':'Buffalo',
    'Carolina Panthers':'Carolina', 'Chicago Bears':'Chicago', 'Cincinnati Bengals':'Cincinnati', 'Cleveland Browns':'Cleveland',
    'Dallas Cowboys':'Dallas', 'Denver Broncos':'Denver', 'Detroit Lions':'Detroit', 'Green Bay Packers':'Green Bay',
    'Houston Texans':'Houston', 'Indianapolis Colts':'Indianapolis', 'Jacksonville Jaguars':'Jacksonville', 'Kansas City Chiefs':'Kansas City',
    'Miami Dolphins':'Miami', 'Minnesota Vikings':'Minnesota', 'New England Patriots':'New England', 'New Orleans Saints':'New Orleans',
    'New York Giants':'NY Giants', 'New York Jets':'NY Jets', 'Oakland Raiders':'Oakland', 'Philadelphia Eagles':'Philadelphia',
    'Pittsburgh Steelers':'Pittsburgh', 'San Diego Chargers':'LA Chargers', 'San Francisco 49ers':'San Francisco', 'Seattle Seahawks':'Seattle',
    'St. Louis Rams':'LA Rams', 'Tampa Bay Buccaneers':'Tampa Bay', 'Tennessee Titans':'Tennessee', 'Washington Redskins':'Washington'}
teamnames_2016 = teamnames_2003_2015.copy()
teamnames_2016.pop('St. Louis Rams')
teamnames_2016['Los Angeles Rams'] = 'LA Rams'
teamnames_2017_2019 = teamnames_2016.copy()
teamnames_2017_2019.pop('San Diego Chargers')
teamnames_2017_2019['Los Angeles Chargers'] = 'LA Chargers'
scores_df = scores_df.replace(teamnames_2003_2015)
scores_df = scores_df.replace(teamnames_2016)
scores_df = scores_df.replace(teamnames_2017_2019)

# Date preprocessing to get codes
scores_df[['Month', 'MonthDay']] = scores_df['Date'].str.split(expand=True) # split <month> <day> into 2 columns
months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
    'September':9, 'October':10, 'November':11, 'December':12} # dictionary to convert string to number
scores_df['Month'] = scores_df['Month'].map(months) # convert months to numbers
scores_df['DateCode'] = scores_df['Year'].astype(str) + '-' + scores_df['Month'].astype(str) + '-' + scores_df['MonthDay'].astype(str)
scores_df = scores_df.drop(['Date', 'Month', 'MonthDay'], axis=1)

# Array of datecodes that need to be scraped
DATECODES = scores_df['DateCode'].unique()

# Create dataframes for each date
counter = 1
date_dfs = {}
for date in DATECODES:
    for i in range(len(STATS)):
        link = LINK_PREFIX + STATS[i] + '?date=' + date
        stat_df = df(STATS[i], link)
        if i == 0:
            date_dfs[date] = stat_df
        else:
            date_dfs[date] = date_dfs[date].join(stat_df.set_index('Team'), on='Team')
        print('{}/{}'.format(counter, len(DATECODES) * len(STATS)))
        counter += 1