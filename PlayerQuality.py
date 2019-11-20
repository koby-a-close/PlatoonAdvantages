# PlayerQuality.py
# Created 11/05/2019 by KAC

"""Looks at platoon advantages from pitcher and hitter quality. Confirming (or disputing) research done in The Book."""

# import warnings filter
from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=Warning)

# Load packages
import pandas as pd
import numpy as np
from prettytable import PrettyTable
from pybaseball import statcast

# Data directory
data_dir = '/Users/Koby/PycharmProjects/PlatoonAdvantages/Input/'

# Basic player info and dictionary between name and ID
player_info = pd.read_csv(data_dir + 'player_names.csv')
player_id = dict(zip(player_info.mlb_id, player_info.mlb_name))

# Qualified batter data and eliminating unneeded rows
df_qualified_batters = pd.read_csv(data_dir + '800PAData.csv')
df_qualified_batters = df_qualified_batters[['Name', 'wOBA']]
df_qualified_batters['Tag'] = np.nan
df_qualified_batters.Tag[(df_qualified_batters['wOBA'] > 0.348)] = 'Good'
df_qualified_batters.Tag[(df_qualified_batters['wOBA'] < 0.310)] = 'Bad'
df_qualified_batters.Tag[(df_qualified_batters['wOBA'] <= 0.348) & (df_qualified_batters['wOBA'] >= 0.310)] = 'Average'
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.Tag))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.Tag.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_Advanced.csv')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'FIP']]
df_qualified_pitchers['Tag'] = np.nan
df_qualified_pitchers.Tag[(df_qualified_pitchers['FIP'] > 4.69)] = 'Bad'
df_qualified_pitchers.Tag[(df_qualified_pitchers['FIP'] < 3.78)] = 'Good'
df_qualified_pitchers.Tag[(df_qualified_pitchers['FIP'] <= 4.69) & (df_qualified_pitchers['FIP'] >= 3.78)] = 'Average'
pitcher_tag = dict(zip(df_qualified_pitchers.Name, df_qualified_pitchers.Tag))
# print(df_qualified_pitchers.describe())
print("Number of Pitchers in Each Category: \n", df_qualified_pitchers.Tag.value_counts())

# Raw play by play data and eliminating non-BBIP events
df_raw = statcast(start_dt='2017-03-01', end_dt='2019-10-01')
df_raw = df_raw[['pitcher', 'batter', 'woba_value', 'woba_denom']]
df_raw = df_raw.dropna()
df_raw['pitcher_name'] = df_raw['pitcher'].map(player_id)
df_raw['batter_name'] = df_raw['batter'].map(player_id)
df_raw['pitcher_tag'] = df_raw['pitcher_name'].map(pitcher_tag)
df_raw['batter_tag'] = df_raw['batter_name'].map(batter_tag)
df_raw = df_raw.dropna()

# Splits data up by match ups, pitcher tendency is listed first
df_G_G = df_raw[(df_raw.pitcher_tag == 'Good') & (df_raw.batter_tag == 'Good')]
df_G_A = df_raw[(df_raw.pitcher_tag == 'Good') & (df_raw.batter_tag == 'Average')]
df_G_B = df_raw[(df_raw.pitcher_tag == 'Good') & (df_raw.batter_tag == 'Bad')]
df_A_G = df_raw[(df_raw.pitcher_tag == 'Average') & (df_raw.batter_tag == 'Good')]
df_A_A = df_raw[(df_raw.pitcher_tag == 'Average') & (df_raw.batter_tag == 'Average')]
df_A_B = df_raw[(df_raw.pitcher_tag == 'Average') & (df_raw.batter_tag == 'Bad')]
df_B_G = df_raw[(df_raw.pitcher_tag == 'Bad') & (df_raw.batter_tag == 'Good')]
df_B_A = df_raw[(df_raw.pitcher_tag == 'Bad') & (df_raw.batter_tag == 'Average')]
df_B_B = df_raw[(df_raw.pitcher_tag == 'Bad') & (df_raw.batter_tag == 'Bad')]

df_All_G = df_raw[(df_raw.batter_tag == 'Good')]
df_All_A = df_raw[(df_raw.batter_tag == 'Average')]
df_All_B = df_raw[(df_raw.batter_tag == 'Bad')]
df_G_All = df_raw[(df_raw.pitcher_tag == 'Good')]
df_A_All = df_raw[(df_raw.pitcher_tag == 'Average')]
df_B_All = df_raw[(df_raw.pitcher_tag == 'Bad')]

G_G_wOBA = round(np.sum(df_G_G.woba_value)/np.sum(df_G_G.woba_denom), 3)
G_A_wOBA = round(np.sum(df_G_A.woba_value)/np.sum(df_G_A.woba_denom), 3)
G_B_wOBA = round(np.sum(df_G_B.woba_value)/np.sum(df_G_B.woba_denom), 3)
A_G_wOBA = round(np.sum(df_A_G.woba_value)/np.sum(df_A_G.woba_denom), 3)
A_A_wOBA = round(np.sum(df_A_A.woba_value)/np.sum(df_A_A.woba_denom), 3)
A_B_wOBA = round(np.sum(df_A_B.woba_value)/np.sum(df_A_B.woba_denom), 3)
B_G_wOBA = round(np.sum(df_B_G.woba_value)/np.sum(df_B_G.woba_denom), 3)
B_A_wOBA = round(np.sum(df_B_A.woba_value)/np.sum(df_B_A.woba_denom), 3)
B_B_wOBA = round(np.sum(df_B_B.woba_value)/np.sum(df_B_B.woba_denom), 3)

All_G_wOBA = round(np.sum(df_All_G.woba_value)/np.sum(df_All_G.woba_denom), 3)
All_A_wOBA = round(np.sum(df_All_A.woba_value)/np.sum(df_All_A.woba_denom), 3)
All_B_wOBA = round(np.sum(df_All_B.woba_value)/np.sum(df_All_B.woba_denom), 3)
G_All_wOBA = round(np.sum(df_G_All.woba_value)/np.sum(df_G_All.woba_denom), 3)
A_All_wOBA = round(np.sum(df_A_All.woba_value)/np.sum(df_A_All.woba_denom), 3)
B_All_wOBA = round(np.sum(df_B_All.woba_value)/np.sum(df_B_All.woba_denom), 3)
All_All_wOBA = round(np.sum(df_raw.woba_value)/np.sum(df_raw.woba_denom), 3)

t = PrettyTable(['Batter | Pitcher', 'Good', 'Average', 'Bad', 'All'])
t.add_row(['Good', G_G_wOBA, A_G_wOBA, B_G_wOBA, All_G_wOBA])
t.add_row(['Average', G_A_wOBA, A_A_wOBA, B_A_wOBA, All_A_wOBA])
t.add_row(['Bad', G_B_wOBA, A_B_wOBA, B_B_wOBA, A_B_wOBA])
t.add_row(['All', G_All_wOBA, A_All_wOBA, B_All_wOBA, All_All_wOBA])
print(t)

data = t.get_string()
with open('PlayerQuality.txt', 'w') as info:
    info.write(data)

