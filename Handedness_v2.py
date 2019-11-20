# BB-KRate.py
# Created 11/05/2019 by KAC

"""Looks at platoon advantages from BB and K rate. Confirming (or disputing) research done in The Book."""

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
df_qualified_batters = pd.merge(left=df_qualified_batters, right=player_info, how='left', left_on='Name', right_on='mlb_name')
df_qualified_batters = df_qualified_batters[['Name', 'bats']]
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.bats))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.bats.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_Advanced.csv')
df_qualified_pitchers = pd.merge(left=df_qualified_pitchers, right=player_info, how='left', left_on='Name', right_on='mlb_name')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'throws']]
pitcher_tag = dict(zip(df_qualified_pitchers.Name, df_qualified_pitchers.throws))
# print(df_qualified_pitchers.describe())
print("Number of Pitchers in Each Category: \n", df_qualified_pitchers.throws.value_counts())

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
df_L_L = df_raw[(df_raw.pitcher_tag == 'L') & (df_raw.batter_tag == 'L')]
df_L_R = df_raw[(df_raw.pitcher_tag == 'L') & (df_raw.batter_tag == 'R')]
df_L_S = df_raw[(df_raw.pitcher_tag == 'L') & (df_raw.batter_tag == 'S')]
df_R_L = df_raw[(df_raw.pitcher_tag == 'R') & (df_raw.batter_tag == 'L')]
df_R_R = df_raw[(df_raw.pitcher_tag == 'R') & (df_raw.batter_tag == 'R')]
df_R_S = df_raw[(df_raw.pitcher_tag == 'R') & (df_raw.batter_tag == 'S')]


L_L_wOBA = round(np.sum(df_L_L.woba_value)/np.sum(df_L_L.woba_denom), 3)
L_R_wOBA = round(np.sum(df_L_R.woba_value)/np.sum(df_L_R.woba_denom), 3)
L_S_wOBA = round(np.sum(df_L_S.woba_value)/np.sum(df_L_S.woba_denom), 3)
R_L_wOBA = round(np.sum(df_R_L.woba_value)/np.sum(df_R_L.woba_denom), 3)
R_R_wOBA = round(np.sum(df_R_R.woba_value)/np.sum(df_R_R.woba_denom), 3)
R_S_wOBA = round(np.sum(df_R_S.woba_value)/np.sum(df_R_S.woba_denom), 3)

n_L_L = np.sum(df_L_L.woba_denom)
n_L_R = np.sum(df_L_R.woba_denom)
n_L_S = np.sum(df_L_S.woba_denom)
n_R_L = np.sum(df_R_L.woba_denom)
n_R_R = np.sum(df_R_R.woba_denom)
n_R_S = np.sum(df_R_S.woba_denom)
n_total = n_L_L + n_L_R + n_L_S + n_R_L + n_R_R + n_R_S

perc_L_L = n_L_L/n_total
perc_L_R = n_L_R/n_total
perc_L_S = n_L_S/n_total
perc_R_L = n_R_L/n_total
perc_R_R = n_R_R/n_total
perc_R_S = n_R_S/n_total

# Creates a table to visualize the data like in The Book
t = PrettyTable(['Batter | Pitcher', 'Left', 'Right', "Hitter's Platoon Advantage"])
t.add_row(['Left', L_L_wOBA, R_L_wOBA, round((R_L_wOBA - L_L_wOBA), 3)])
t.add_row(['Right', L_R_wOBA, R_R_wOBA, round((L_R_wOBA - R_R_wOBA), 3)])
t.add_row(['Switch', L_S_wOBA, R_S_wOBA, 'N/A'])
t.add_row(["Pitcher's Platoon Advantage", round((L_R_wOBA - L_L_wOBA), 3), round((R_L_wOBA - R_R_wOBA), 3), 'N/A'])
print(t)

data = t.get_string()
with open('Handedness.txt', 'w') as info:
    info.write(data)

