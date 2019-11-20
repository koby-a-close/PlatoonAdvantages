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
df_qualified_batters = df_qualified_batters[['Name', 'Pull%', 'Oppo%']]
df_qualified_batters = df_qualified_batters.rename(columns={'Pull%': 'Pull', 'Oppo%': 'Oppo'})
df_qualified_batters['Tag'] = np.nan
df_qualified_batters.Tag[(df_qualified_batters['Pull'] > 0.44)] = 'Pull'
df_qualified_batters.Tag[(df_qualified_batters['Oppo'] > 0.27) & (df_qualified_batters['Pull'] < 0.41)] = 'Oppo'
df_qualified_batters = df_qualified_batters.fillna('Neutral')
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.Tag))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.Tag.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_BattedBall.csv')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'Pull%', 'Oppo%']]
df_qualified_pitchers = df_qualified_pitchers.rename(columns={'Pull%': 'Pull', 'Oppo%': 'Oppo'})
df_qualified_pitchers['Tag'] = np.nan
df_qualified_pitchers.Tag[(df_qualified_pitchers['Pull'] > 0.42)] = 'Pull'
df_qualified_pitchers.Tag[(df_qualified_pitchers['Oppo'] > 0.27) & (df_qualified_pitchers['Pull'] < 0.38)] = 'Oppo'
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
df_P_P = df_raw[(df_raw.pitcher_tag == 'Pull') & (df_raw.batter_tag == 'Pull')]
df_P_N = df_raw[(df_raw.pitcher_tag == 'Pull') & (df_raw.batter_tag == 'Neutral')]
df_P_O = df_raw[(df_raw.pitcher_tag == 'Pull') & (df_raw.batter_tag == 'Oppo')]
df_N_P = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Pull')]
df_N_N = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Neutral')]
df_N_O = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Oppo')]
df_O_P = df_raw[(df_raw.pitcher_tag == 'Oppo') & (df_raw.batter_tag == 'Pull')]
df_O_N = df_raw[(df_raw.pitcher_tag == 'Oppo') & (df_raw.batter_tag == 'Neutral')]
df_O_O = df_raw[(df_raw.pitcher_tag == 'Oppo') & (df_raw.batter_tag == 'Oppo')]

P_P_wOBA = round(np.sum(df_P_P.woba_value)/np.sum(df_P_P.woba_denom), 3)
P_N_wOBA = round(np.sum(df_P_N.woba_value)/np.sum(df_P_N.woba_denom), 3)
P_O_wOBA = round(np.sum(df_P_O.woba_value)/np.sum(df_P_O.woba_denom), 3)
N_P_wOBA = round(np.sum(df_N_P.woba_value)/np.sum(df_N_P.woba_denom), 3)
N_N_wOBA = round(np.sum(df_N_N.woba_value)/np.sum(df_N_N.woba_denom), 3)
N_O_wOBA = round(np.sum(df_N_O.woba_value)/np.sum(df_N_O.woba_denom), 3)
O_P_wOBA = round(np.sum(df_O_P.woba_value)/np.sum(df_O_P.woba_denom), 3)
O_N_wOBA = round(np.sum(df_O_N.woba_value)/np.sum(df_O_N.woba_denom), 3)
O_O_wOBA = round(np.sum(df_O_O.woba_value)/np.sum(df_O_O.woba_denom), 3)

t = PrettyTable(['Batter | Pitcher', 'Pull', 'Neutral', 'Oppo'])
t.add_row(['Pull', P_P_wOBA, N_P_wOBA, O_P_wOBA])
t.add_row(['Neutral', P_N_wOBA, N_N_wOBA, O_N_wOBA])
t.add_row(['Oppo', P_O_wOBA, N_O_wOBA, O_O_wOBA])
print(t)

data = t.get_string()
with open('Pull-OppoRate_2.txt', 'w') as info:
    info.write(data)

