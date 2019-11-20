# PlayerQuality.py
# Created 11/05/2019 by KAC

"""Looks at platoon advantages from spray chart tendencies. New metric based on research in The Book."""

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
df_qualified_batters = pd.read_csv(data_dir + '800PAData_BattedBall.csv')
df_qualified_batters = df_qualified_batters[['Name', 'Hard%', 'Soft%']]
df_qualified_batters = df_qualified_batters.rename(columns={'Hard%': 'Hard', 'Soft%': 'Soft'})
df_qualified_batters['Tag'] = np.nan
df_qualified_batters.Tag[(df_qualified_batters['Hard'] > 0.39)] = 'Hard'
df_qualified_batters.Tag[(df_qualified_batters['Soft'] > 0.19) & (df_qualified_batters['Hard'] < 0.39)] = 'Soft'
df_qualified_batters = df_qualified_batters.fillna('Neutral')
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.Tag))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.Tag.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_BattedBall.csv')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'Hard%', 'Soft%']]
df_qualified_pitchers = df_qualified_pitchers.rename(columns={'Hard%': 'Hard', 'Soft%': 'Soft'})
df_qualified_pitchers['Tag'] = np.nan
df_qualified_pitchers.Tag[(df_qualified_pitchers['Hard'] > 0.37)] = 'Hard'
df_qualified_pitchers.Tag[(df_qualified_pitchers['Soft'] > 0.20) & (df_qualified_pitchers['Hard'] < 0.37)] = 'Soft'
df_qualified_pitchers = df_qualified_pitchers.fillna('Neutral')
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
df_H_H = df_raw[(df_raw.pitcher_tag == 'Hard') & (df_raw.batter_tag == 'Hard')]
df_H_N = df_raw[(df_raw.pitcher_tag == 'Hard') & (df_raw.batter_tag == 'Neutral')]
df_H_S = df_raw[(df_raw.pitcher_tag == 'Hard') & (df_raw.batter_tag == 'Soft')]
df_N_H = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Hard')]
df_N_N = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Neutral')]
df_N_S = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Soft')]
df_S_H = df_raw[(df_raw.pitcher_tag == 'Soft') & (df_raw.batter_tag == 'Hard')]
df_S_N = df_raw[(df_raw.pitcher_tag == 'Soft') & (df_raw.batter_tag == 'Neutral')]
df_S_S = df_raw[(df_raw.pitcher_tag == 'Soft') & (df_raw.batter_tag == 'Soft')]

H_H_wOBA = round(np.sum(df_H_H.woba_value)/np.sum(df_H_H.woba_denom), 3)
H_N_wOBA = round(np.sum(df_H_N.woba_value)/np.sum(df_H_N.woba_denom), 3)
H_S_wOBA = round(np.sum(df_H_S.woba_value)/np.sum(df_H_S.woba_denom), 3)
N_H_wOBA = round(np.sum(df_N_H.woba_value)/np.sum(df_N_H.woba_denom), 3)
N_N_wOBA = round(np.sum(df_N_N.woba_value)/np.sum(df_N_N.woba_denom), 3)
N_S_wOBA = round(np.sum(df_N_S.woba_value)/np.sum(df_N_S.woba_denom), 3)
S_H_wOBA = round(np.sum(df_S_H.woba_value)/np.sum(df_S_H.woba_denom), 3)
S_N_wOBA = round(np.sum(df_S_N.woba_value)/np.sum(df_S_N.woba_denom), 3)
S_S_wOBA = round(np.sum(df_S_S.woba_value)/np.sum(df_S_S.woba_denom), 3)

t = PrettyTable(['Batter | Pitcher', 'Hard', 'Neutral', 'Soft'])
t.add_row(['Hard', H_H_wOBA, N_H_wOBA, S_H_wOBA])
t.add_row(['Neutral', H_N_wOBA, N_N_wOBA, S_N_wOBA])
t.add_row(['Soft', H_S_wOBA, N_S_wOBA, S_S_wOBA])
print(t)

data = t.get_string()
with open('Hard-SoftRate.txt', 'w') as info:
    info.write(data)

