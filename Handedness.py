# Handedness.py
# Created 11/03/2019 by KAC

"""Looks at platoon advantages from handedness. Confirming (or disputing) research done in The Book."""

# import warnings filter
from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=Warning)

# Load packages
import pandas as pd
import numpy as np
from prettytable import PrettyTable

# Load CSV files needed
data_dir = '/Users/Koby/PycharmProjects/PlatoonAdvantages/Input/'
player_info = pd.read_csv(data_dir + 'player_names.csv')
df_qualified_players = pd.read_csv(data_dir + '800PAData.csv')
df_LL_raw = pd.read_csv(data_dir + 'LvLSplits.csv')
df_LR_raw = pd.read_csv(data_dir + 'LvRSplits.csv')
df_RL_raw = pd.read_csv(data_dir + 'RvLSplits.csv')
df_RR_raw = pd.read_csv(data_dir + 'RvRSplits.csv')

# Combines the list of qualified batters with their player info like ID and handedness.
# Cuts the colummns down to name, mlb ID, and handedness batting.
df_qualified_players = pd.merge(left=df_qualified_players, right=player_info, how='left', left_on='Name', right_on='mlb_name')
df_qualified_players = df_qualified_players[['Name', 'mlb_id', 'bats']]
print("Total Batters: ", len(df_qualified_players))

# Splits the qualified batters up by how they bat
df_L_batters = df_qualified_players[df_qualified_players.bats == 'L']
df_R_batters = df_qualified_players[df_qualified_players.bats == 'R']
df_S_batters = df_qualified_players[df_qualified_players.bats == 'S']

# Merges performance data in each matchup situation with the appropriate list of batters.
# FIRST LETTER IS FOR PITCHER HAND, SECOND FOR BATTER HAND
df_LL = pd.merge(left=df_LL_raw, right=df_L_batters, how='inner', on='Name')
df_LL = df_LL[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]
df_LR = pd.merge(left=df_LR_raw, right=df_R_batters, how='inner', on='Name')
df_LR = df_LR[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]
df_LS = pd.merge(left=df_LR_raw, right=df_S_batters, how='inner', on='Name')
df_LS = df_LS[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]

df_RL = pd.merge(left=df_RL_raw, right=df_L_batters, how='inner', on='Name')
df_RL = df_RL[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]
df_RR = pd.merge(left=df_RR_raw, right=df_R_batters, how='inner', on='Name')
df_RR = df_RR[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]
df_RS = pd.merge(left=df_RL_raw, right=df_S_batters, how='inner', on='Name')
df_RS = df_RS[['Name', 'mlb_id', 'bats', 'PA', 'wOBA']]

# Calculates weighted average wOBA values suing PA as weighting
LL_wOBA = round(np.average(df_LL.wOBA, weights=df_LL.PA), 3)
LR_wOBA = round(np.average(df_LR.wOBA, weights=df_LR.PA), 3)
LS_wOBA = round(np.average(df_LS.wOBA, weights=df_LS.PA), 3)
RL_wOBA = round(np.average(df_RL.wOBA, weights=df_RL.PA), 3)
RR_wOBA = round(np.average(df_RR.wOBA, weights=df_RR.PA), 3)
RS_wOBA = round(np.average(df_RS.wOBA, weights=df_RS.PA), 3)

# Creates a table to visualize the data like in The Book
t = PrettyTable(['Batter | Pitcher', 'Left', 'Right', "Hitter's Platoon Advantage"])
t.add_row(['Left', LL_wOBA, RL_wOBA, round((RL_wOBA - LL_wOBA), 3)])
t.add_row(['Right', LR_wOBA, RR_wOBA, round((LR_wOBA - RR_wOBA), 3)])
t.add_row(['Switch', LS_wOBA, RS_wOBA, 'N/A'])
t.add_row(["Pitcher's Platoon Advantage", round((LR_wOBA - LL_wOBA), 3), round((RL_wOBA - RR_wOBA), 3), 'N/A'])
print(t)

data = t.get_string()
with open('Hand.txt', 'w') as info:
    info.write(data)