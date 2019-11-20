# GB-FBRate.py
# Created 11/05/2019 by KAC

"""Looks at platoon advantages from GB and FB rate. Confirming (or disputing) research done in The Book."""

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
df_qualified_batters = df_qualified_batters[['Name', 'GB/FB']]
df_qualified_batters['Tag'] = np.nan
df_qualified_batters.Tag[(df_qualified_batters['GB/FB'] > 1.46)] = 'GB'
df_qualified_batters.Tag[(df_qualified_batters['GB/FB'] < 0.94)] = 'FB'
df_qualified_batters.Tag[(df_qualified_batters['GB/FB'] <= 1.46) & (df_qualified_batters['GB/FB'] >= 0.94)] = 'N'
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.Tag))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.Tag.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_BattedBall.csv')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'GB/FB']]
df_qualified_pitchers['Tag'] = np.nan
df_qualified_pitchers.Tag[(df_qualified_pitchers['GB/FB'] > 1.55)] = 'GB'
df_qualified_pitchers.Tag[(df_qualified_pitchers['GB/FB'] < 1.02)] = 'FB'
df_qualified_pitchers.Tag[(df_qualified_pitchers['GB/FB'] <= 1.55) & (df_qualified_pitchers['GB/FB'] >= 1.02)] = 'N'
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
df_FB_FB = df_raw[(df_raw.pitcher_tag == 'FB') & (df_raw.batter_tag == 'FB')]
df_FB_N = df_raw[(df_raw.pitcher_tag == 'FB') & (df_raw.batter_tag == 'N')]
df_FB_GB = df_raw[(df_raw.pitcher_tag == 'FB') & (df_raw.batter_tag == 'GB')]
df_N_FB = df_raw[(df_raw.pitcher_tag == 'N') & (df_raw.batter_tag == 'FB')]
df_N_N = df_raw[(df_raw.pitcher_tag == 'N') & (df_raw.batter_tag == 'N')]
df_N_GB = df_raw[(df_raw.pitcher_tag == 'N') & (df_raw.batter_tag == 'GB')]
df_GB_FB = df_raw[(df_raw.pitcher_tag == 'GB') & (df_raw.batter_tag == 'FB')]
df_GB_N = df_raw[(df_raw.pitcher_tag == 'GB') & (df_raw.batter_tag == 'N')]
df_GB_GB = df_raw[(df_raw.pitcher_tag == 'GB') & (df_raw.batter_tag == 'GB')]

FB_FB_wOBA = round(np.sum(df_FB_FB.woba_value)/np.sum(df_FB_FB.woba_denom), 3)
FB_N_wOBA = round(np.sum(df_FB_N.woba_value)/np.sum(df_FB_N.woba_denom), 3)
FB_GB_wOBA = round(np.sum(df_FB_GB.woba_value)/np.sum(df_FB_GB.woba_denom), 3)
N_FB_wOBA = round(np.sum(df_N_FB.woba_value)/np.sum(df_N_FB.woba_denom), 3)
N_N_wOBA = round(np.sum(df_N_N.woba_value)/np.sum(df_N_N.woba_denom), 3)
N_GB_wOBA = round(np.sum(df_N_GB.woba_value)/np.sum(df_N_GB.woba_denom), 3)
GB_FB_wOBA = round(np.sum(df_GB_FB.woba_value)/np.sum(df_GB_FB.woba_denom), 3)
GB_N_wOBA = round(np.sum(df_GB_N.woba_value)/np.sum(df_GB_N.woba_denom), 3)
GB_GB_wOBA = round(np.sum(df_GB_GB.woba_value)/np.sum(df_GB_GB.woba_denom), 3)

n_FB_FB = np.sum(df_FB_FB.woba_denom)
n_FB_N = np.sum(df_FB_N.woba_denom)
n_FB_GB = np.sum(df_FB_GB.woba_denom)
n_N_FB = np.sum(df_N_FB.woba_denom)
n_N_N = np.sum(df_N_N.woba_denom)
n_N_GB = np.sum(df_N_GB.woba_denom)
n_GB_FB = np.sum(df_GB_FB.woba_denom)
n_GB_N = np.sum(df_GB_N.woba_denom)
n_GB_GB = np.sum(df_GB_GB.woba_denom)
n_total = n_FB_FB + n_FB_N + n_FB_GB + n_N_FB + n_N_N + n_N_GB + n_GB_FB + n_GB_N + n_GB_GB

perc_FB_FB = n_FB_FB/n_total
perc_FB_N = n_FB_N/n_total
perc_FB_GB = n_FB_GB/n_total
perc_N_FB = n_N_FB/n_total
perc_N_N = n_N_N/n_total
perc_N_GB = n_N_GB/n_total
perc_GB_FB = n_GB_FB/n_total
perc_GB_N = n_GB_N/n_total
perc_GB_GB = n_GB_GB/n_total

t = PrettyTable(['Batter | Pitcher', 'FB', 'Neutral', 'GB'])
t.add_row(['FB', FB_FB_wOBA, N_FB_wOBA, GB_FB_wOBA])
t.add_row(['Neutral', FB_N_wOBA, N_N_wOBA, GB_N_wOBA])
t.add_row(['GB', FB_GB_wOBA, N_GB_wOBA, GB_GB_wOBA])
print(t)

data = t.get_string()
with open('GB-FB.txt', 'w') as info:
    info.write(data)
