import numpy as np 
import pandas as pd 
import os 
import ast
from itertools import combinations

# find files
path = '../data'
files = os.listdir(path)
file = files[0]

# read file 
df = pd.read_csv(os.path.join(path, file))

# gather friend variables
n_friends = 3
variables = [
    'climate_concern', 
    'gay_adoption',
    'migration_enriches_culture',
    'govt_reduce_inequ'
    ]
friend_list = []
for var in variables: 
    var_list = [f"survey.1.player.f{i+1}_{var}" for i in range(n_friends)]
    friend_list.extend(var_list)    

# gather party variables
party_list = []
parties = ['AfD_Voter', 'Green_Voter']
for var in variables: 
    var_list = [f"survey.1.player.{p}_{var}" for p in parties]
    party_list.extend(var_list)

# gather personal variables
self_list = [f'survey.1.player.{var}' for var in variables]

### organize ###
df_friends_wide = df[friend_list]
df_friends_long = df_friends_wide.melt(var_name='variable', value_name='position')
df_friends_long[['var', 'issue']] = df_friends_long['variable'].str.extract(r'\.(f\d+)_(.+)$')
df_friends_long['type'] = 'friend'

# omg we actually need the friend names as well 
mapping = {f'f{i+1}': df[f'survey.1.player.friend{i+1}'][0] for i in range(n_friends)}
df_friends_long['label'] = df_friends_long['var'].map(mapping)

df_party_wide = df[party_list]
df_party_long = df_party_wide.melt(var_name='variable', value_name='position')
df_party_long[['var', 'issue']] = df_party_long['variable'].str.extract(r'player\.([A-Za-z]+_Voter)_(.+)$')
df_party_long['type'] = 'party'
df_party_long['label'] = df_party_long['var']

df_self_wide = df[self_list]
df_self_long = df_self_wide.melt(var_name='variable', value_name='position')
df_self_long['issue'] = df_self_long['variable'].str.extract(r'player\.(.+)$')
df_self_long[['var', 'label', 'type']] = 'self'

# gather everything inshallah
df_actual = pd.concat([df_friends_long, df_party_long, df_self_long])
df_actual = df_actual[['position', 'label', 'var', 'issue']]

# positions
pos = df['survey.1.player.positions'][0]
pos = ast.literal_eval(pos)

# calculate distance
# Calculate distances
distances = []
for (point1, point2) in combinations(pos, 2):
    label_x = point1['label']
    label_y = point2['label']
    x1, y1 = point1['x'], point1['y']
    x2, y2 = point2['x'], point2['y']
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distances.append({'x': label_x, 'y': label_y, 'perceived_distance': distance})

# Create a pandas DataFrame
perceived_distance = pd.DataFrame(distances)

### okay for now just focus on self distance ### 
self_perceived = perceived_distance[perceived_distance['x']=='self']

# a bit more wrangling needed for self 
df_actual = df_actual[['position', 'label', 'issue']]
self_actual = df_actual[df_actual['label']=='self']
other_actual = df_actual[df_actual['label']!='self']
self_actual = self_actual.rename(columns={
    'position': 'pos_self',
    'label': 'lab_self'
})
self_merged = self_actual.merge(other_actual, on = 'issue', how = 'inner')
self_merged['distance'] = self_merged['pos_self'] - self_merged['position']
self_merged['abs_distance'] = self_merged['distance'].abs()

# we can also aggregate this 
self_agg = self_merged.groupby('label')['abs_distance'].sum().reset_index(name='distance_actual')

# now look at the two together:
self_perceived = self_perceived[['y', 'perceived_distance']]
self_perceived = self_perceived.rename(columns = {
    'y': 'label',
})

# merge these two 
distance_merge = self_agg.merge(self_perceived, on = 'label', how = 'inner')
distance_merge['scaling'] = distance_merge['perceived_distance'] / distance_merge['distance_actual']