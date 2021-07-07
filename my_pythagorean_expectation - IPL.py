import pandas as pd
import numpy as np
import seaborn as sns

# -------------------------
# Read data
# -------------------------

# Load the datafile (this contains 6 variables:
#   - the date
#   - home team
#   - away team
#   - goals scored (FTHG)
#   - goals against (FTAG)
#   - result (H- home win, D- draw, A – away win)

EPL = pd.read_excel('C:/Users/RCOLL/PycharmProjects/Sports Analytics/Data/EPL2017-18.xlsx',
                    engine='openpyxl')
print(EPL.columns.tolist())

# Create a value for a home wins (win= 1, draw=0.5, loss= 0) and away wins and a count variable for each game (=1).
EPL['hwin'] = np.where(EPL['result'] == 'H', 1, np.where(EPL['result'] == 'D', 0.5, 0))
EPL['awin'] = np.where(EPL['result'] == 'A', 1, np.where(EPL['result'] == 'D', 0.5, 0))
EPL['count'] = 1

# Change data type - date columns
EPL['Date'] = pd.to_datetime(EPL['Date'], format='%Y%m%d')
EPL.dtypes
EPL['year'] = pd.DatetimeIndex(EPL['Date']).year

# Create a file for games played in 2017 (before date 20180000) and another one for games played in 2018
# (after date 20180000).

# Filter data for 2017
EPL17 = EPL[EPL['year'] == 2017]

# Select columns
EPL17_home = EPL17[['HomeTeam', 'hwin', 'count', 'FTHG', 'FTAG']]
# Group by HomeTeam
EPL17_home = EPL17_home.groupby('HomeTeam')['hwin', 'count', 'FTHG', 'FTAG'].sum().reset_index()
# Rename columns
EPL17_home = EPL17_home.rename(columns={'HomeTeam': 'team', 'count': 'hgames', 'FTHG': 'FTHGh', 'FTAG': 'FTAGh'})

# Repeat process for AwayTeam
EPL17_away = EPL17[['AwayTeam', 'awin', 'count', 'FTHG', 'FTAG']]
EPL17_away = EPL17_away.groupby('AwayTeam')['awin', 'count', 'FTHG', 'FTAG'].sum().reset_index()
EPL17_away = EPL17_away.rename(columns={'AwayTeam': 'team', 'count': 'agames', 'FTHG': 'FTHGa', 'FTAG': 'FTAGa'})

# Merge the HomeTeam and the AwayTeam df for 2017
EPL17 = pd.merge(EPL17_home, EPL17_away, on='team')
EPL17

# Create totals
EPL17['total_wins'] = EPL17['hwin'] + EPL17['awin']
EPL17['total_games'] = EPL17['hgames'] + EPL17['agames']
EPL17['total_goals'] = EPL17['FTHGh'] + EPL17['FTAGa']
EPL17['total_goals_a'] = EPL17['FTAGh'] + EPL17['FTHGa']
EPL17

# Create the wins percentage (wpc)
EPL17['wpc17'] = EPL17['total_wins'] / EPL17['total_games']
# Create the pythegorean expectation percentage
EPL17['pyth_pc17'] = EPL17['total_goals']**2 / (EPL17['total_goals']**2 + EPL17['total_goals_a']**2)
EPL17

# -------------------------
# Week 1 Quiz
# -------------------------

# Q2: Which team scored the highest number of goals while playing at home in the first half of the season?
print(EPL17.sort_values(by=['FTHGh'], ascending=False))
# Q3: Which team conceded the highest number of goals while playing away in the first half of the season?
print(EPL17.sort_values(by=['FTHGa'], ascending=False))
# Q4 & Q5: Which of the following teams had the smallest difference between their win percentage and Pythagorean expectation
# in the first half of the season?
EPL17['dif'] = abs(EPL17['wpc17'] - EPL17['pyth_pc17'])
print(EPL17.sort_values(by=['dif'], ascending=True))
# Q6: Which of the following teams had the highest value for away wins (awinvalue) for in the first half of the season?
print(EPL17[['team', 'awin']].sort_values(by=['awin'], ascending=False))
# Q8: What was the correlation between win percentage and the Pythagorean expectation in the first half of the season?
print(EPL17[['wpc17', 'pyth_pc17']].corr())

# Repeat process for 2018
EPL18 = EPL[EPL['year'] == 2018]

EPL18_home = EPL18[['HomeTeam', 'hwin', 'count', 'FTHG', 'FTAG']]
EPL18_home = EPL18_home.groupby('HomeTeam')['hwin', 'count', 'FTHG', 'FTAG'].sum().reset_index()
EPL18_home = EPL18_home.rename(columns={'HomeTeam': 'team', 'count': 'hgames', 'FTHG': 'FTHGh', 'FTAG': 'FTAGh'})

EPL18_away = EPL18[['AwayTeam', 'awin', 'count', 'FTHG', 'FTAG']]
EPL18_away = EPL18_away.groupby('AwayTeam')['awin', 'count', 'FTHG', 'FTAG'].sum().reset_index()
EPL18_away = EPL18_away.rename(columns={'AwayTeam': 'team', 'count': 'agames', 'FTHG': 'FTHGa', 'FTAG': 'FTAGa'})

EPL18 = pd.merge(EPL18_home, EPL18_away, on='team')
EPL18

# Create totals
EPL18['total_wins'] = EPL18['hwin'] + EPL18['awin']
EPL18['total_games'] = EPL18['hgames'] + EPL18['agames']
EPL18['total_goals'] = EPL18['FTHGh'] + EPL18['FTAGa']
EPL18['total_goals_a'] = EPL18['FTAGh'] + EPL18['FTHGa']
EPL18

EPL18['wpc18'] = EPL18['total_wins'] / EPL18['total_games']
EPL18['pyth_pc18'] = EPL18['total_goals']**2 / (EPL18['total_goals']**2 + EPL18['total_goals_a']**2)
EPL18


# -------------------------
# Week 1 Quiz
# -------------------------

# Q1: Total games played in 2018
total_games_2018 = EPL18['total_games'].sum() / 2
total_games_2018
# Q7: Which team had the largest gap between home points won (hwinvalue) and away points won (awinvalue) in the second
# half the season?
EPL18['gap'] = EPL18['hwin'] - EPL18['awin']
print(EPL18[['team', 'gap']].sort_values(by=['gap'], ascending=False))


EPL = pd.merge(EPL17, EPL18, on='team')

# -------------------------
# Week 1 Quiz
# -------------------------

# Q9: What was the correlation between win percentage in the first half of the season and the second half of the season?
print(EPL[['wpc17', 'wpc18']].corr())
# Q10: What was the correlation between win percentage in the second half of the season and the Pythagorean expectation
# in the first half of the season?
print(EPL[['pyth_pc17', 'wpc18']].corr())

# Is there any relation between the "wins" and the scores?
# Create a scatter plot with
sns.relplot(x="pyth_pc18", y="wpc18", data=EPL)
sns.relplot(x="pyth_pc17", y="wpc17", data=EPL)
