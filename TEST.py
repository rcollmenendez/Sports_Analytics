import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Read data
# -------------------------

MLB = pd.read_excel('C:/Users/RCOLL/PycharmProjects/Sports Analytics/Data/Retrosheet MLB game log 2018.xlsx',
                    engine='openpyxl')
print(MLB.columns.tolist())
MLB

# Select columns and rename
MLB18 = MLB[['VisitingTeam', 'HomeTeam', 'VisitorRunsScored', 'HomeRunsScore', 'Date']]
MLB18 = MLB18.rename(columns={'VisitorRunsScored': 'VisR', 'HomeRunsScore': 'HomR'})

print(MLB18.columns.tolist())
MLB18.dtypes

# -------------------------
# Clean data
# -------------------------

# Change date datatype
MLB18['Date'] = pd.to_datetime(MLB18['Date'], format='%Y%m%d')
MLB18.dtypes

MLB18.head()
MLB18.describe()

# -------------------------
# Prepare data
# -------------------------
# Add the counter for the number of games won
MLB18['hwin'] = np.where(MLB18['HomR'] > MLB18['VisR'], 1, 0)
MLB18['awin'] = np.where(MLB18['HomR'] < MLB18['VisR'], 1, 0)
# Add counter for the number of games played
MLB18['count'] = 1

MLB18.head()

# Group df
MLBhome = MLB18.groupby('HomeTeam')['hwin', 'HomR', 'VisR', 'count'].sum().reset_index()
MLBhome = MLBhome.rename(columns={'HomeTeam': 'team', 'VisR': 'VisRh', 'HomR': 'HomRh', 'count': 'Gh'})
MLBhome

MLBaway = MLB18.groupby('VisitingTeam')['awin', 'HomR', 'VisR', 'count'].sum().reset_index()
MLBaway = MLBaway.rename(columns={'VisitingTeam': 'team', 'VisR': 'VisRa', 'HomR': 'HomRa', 'count': 'Ga'})
MLBaway

# Merge df
MLB18 = pd.merge(MLBhome, MLBaway, on='team')

# Now we create the total wins, games, played, runs scored and run conceded by summing the totals as home team and away team
MLB18['total_wins'] = MLB18['hwin'] + MLB18['awin']
MLB18['total_games'] = MLB18['Gh'] + MLB18['Ga']
# Total runs for the team will be the ones made when playing at home + the ones made as a visitor
MLB18['total_runs'] = MLB18['HomRh'] + MLB18['VisRa']
# Total runs against will be the ones the visitors made while playing as a visitor + the ones made when playing at home
MLB18['total_runs_a'] = MLB18['VisRh'] + MLB18['HomRa']

MLB18

# Win percentage
MLB18['win_pc'] = MLB18['total_wins'] / MLB18['total_games']
# Pythagorean Expectation
MLB18['pyth_pc'] = MLB18['total_runs']**2 / (MLB18['total_runs']**2 + MLB18['total_runs_a']**2)
MLB18

# Plot the relation between the win perc and the Pythagorean Expectation
sns.relplot(x="pyth_pc", y="win_pc", data=MLB18)

# -------------------------
# Analysis
# -------------------------

# Regression
pyth_lm = smf.ols(formula = 'win_pc ~ pyth_pc', data=MLB18).fit()
pyth_lm.summary()
