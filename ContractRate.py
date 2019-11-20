# ContactRate.py
# Created 11/05/2019 by KAC

"""Looks at platoon advantages from contact rate. Confirming (or disputing) research done in The Book."""

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
df_qualified_batters = pd.read_csv(data_dir + '800PAData_PlateDiscipline.csv')
df_qualified_batters = df_qualified_batters[['Name', 'Contact%']]
df_qualified_batters = df_qualified_batters.rename(columns={'Contact%': 'Contact'})
df_qualified_batters['Tag'] = np.nan
df_qualified_batters.Tag[(df_qualified_batters['Contact'] > 0.82)] = 'High'
df_qualified_batters.Tag[(df_qualified_batters['Contact'] < 0.74)] = 'Low'
df_qualified_batters.Tag[(df_qualified_batters['Contact'] <= 0.82) & (df_qualified_batters['Contact'] >= 0.74)] = 'Neutral'
batter_tag = dict(zip(df_qualified_batters.Name, df_qualified_batters.Tag))
# print(df_qualified_batters.describe())
print("Number of Batters in Each Category: \n", df_qualified_batters.Tag.value_counts())

# Qualified pitcher data and eliminating unneeded rows
df_qualified_pitchers = pd.read_csv(data_dir + '200IPData_PlateDiscipline.csv')
df_qualified_pitchers = df_qualified_pitchers[['Name', 'Contact%']]
df_qualified_pitchers = df_qualified_pitchers.rename(columns={'Contact%': 'Contact'})
df_qualified_pitchers['Tag'] = np.nan
df_qualified_pitchers.Tag[(df_qualified_pitchers['Contact'] > 0.80)] = 'High'
df_qualified_pitchers.Tag[(df_qualified_pitchers['Contact'] < 0.75)] = 'Low'
df_qualified_pitchers.Tag[(df_qualified_pitchers['Contact'] <= 0.80) & (df_qualified_pitchers['Contact'] >= 0.75)] = 'Neutral'
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
df_H_H = df_raw[(df_raw.pitcher_tag == 'High') & (df_raw.batter_tag == 'High')]
df_H_N = df_raw[(df_raw.pitcher_tag == 'High') & (df_raw.batter_tag == 'Neutral')]
df_H_L = df_raw[(df_raw.pitcher_tag == 'High') & (df_raw.batter_tag == 'Low')]
df_N_H = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'High')]
df_N_N = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Neutral')]
df_N_L = df_raw[(df_raw.pitcher_tag == 'Neutral') & (df_raw.batter_tag == 'Low')]
df_L_H = df_raw[(df_raw.pitcher_tag == 'Low') & (df_raw.batter_tag == 'High')]
df_L_N = df_raw[(df_raw.pitcher_tag == 'Low') & (df_raw.batter_tag == 'Neutral')]
df_L_L = df_raw[(df_raw.pitcher_tag == 'Low') & (df_raw.batter_tag == 'Low')]

H_H_wOBA = round(np.sum(df_H_H.woba_value)/np.sum(df_H_H.woba_denom), 3)
H_N_wOBA = round(np.sum(df_H_N.woba_value)/np.sum(df_H_N.woba_denom), 3)
H_L_wOBA = round(np.sum(df_H_L.woba_value)/np.sum(df_H_L.woba_denom), 3)
N_H_wOBA = round(np.sum(df_N_H.woba_value)/np.sum(df_N_H.woba_denom), 3)
N_N_wOBA = round(np.sum(df_N_N.woba_value)/np.sum(df_N_N.woba_denom), 3)
N_L_wOBA = round(np.sum(df_N_L.woba_value)/np.sum(df_N_L.woba_denom), 3)
L_H_wOBA = round(np.sum(df_L_H.woba_value)/np.sum(df_L_H.woba_denom), 3)
L_N_wOBA = round(np.sum(df_L_N.woba_value)/np.sum(df_L_N.woba_denom), 3)
L_L_wOBA = round(np.sum(df_L_L.woba_value)/np.sum(df_L_L.woba_denom), 3)

t = PrettyTable(['Batter | Pitcher', 'High Contact', 'Neutral Contact', 'Low Contact'])
t.add_row(['High Contact', H_H_wOBA, N_H_wOBA, L_H_wOBA])
t.add_row(['Neutral Contact', H_N_wOBA, N_N_wOBA, L_N_wOBA])
t.add_row(['Low Contact', H_L_wOBA, N_L_wOBA, L_L_wOBA])
print(t)

data = t.get_string()
with open('Contact.txt', 'w') as info:
    info.write(data)

