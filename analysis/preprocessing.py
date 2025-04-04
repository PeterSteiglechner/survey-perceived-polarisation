import numpy as np 
import pandas as pd 
import os 
import ast
from itertools import combinations

def map_value(x, from_min=-1, from_max=1, to_min=1, to_max=7):
    # Linear interpolation formula
    return to_min + (x - from_min) * (to_max - to_min) / (from_max - from_min)

# find files
path = '../data'
files = os.listdir(path)
file = files[0]

# read file 
df = pd.read_csv(os.path.join(path, file))

#### gather actual beliefs ####
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

# organize 
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

# the p guys .. 
p_list = []
vals_arr = {
    "P1": [1, 1, 1, 1],
    "P2": [0.5,0.5,0.5,0.5],
    "P3": [0.2, 0.1, -0.5, 0.2],
    "P4": [0.05, -0.05, -1, -1],
}
for key, val in vals_arr.items(): 
    sub_lst = [(key, policy, value) for policy, value in zip(variables, val)]
    p_list.extend(sub_lst)

df_p = pd.DataFrame(p_list, columns = ['label', 'issue', 'position'])
df_p['type'] = 'P'
df_p['var'] = df_p['label']
df_p['position'] = df_p['position'].apply(map_value)

# gather everything inshallah
df_actual = pd.concat([df_self_long, df_friends_long, df_party_long, df_p])
df_actual = df_actual[['position', 'label', 'type', 'issue']]

#### gather perceived ####
# actual positions really easy to access
pos = df['survey.1.player.positions'][0]
pos = ast.literal_eval(pos)

#### we now have the belief + space positions ####

#### now get the distances ####

# calculate perceived distances 
distances = []
for (point1, point2) in combinations(pos, 2):
    label_x = point1['label']
    label_y = point2['label']
    x1, y1 = point1['x'], point1['y']
    x2, y2 = point2['x'], point2['y']
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distances.append({
        'x': label_x, 
        'x_pos': (np.round(x1, 2), np.round(y1, 2)), 
        'y': label_y, 
        'y_pos': (np.round(x2, 2), np.round(y2, 2)), 
        'euclidean': distance,
    })
perceived_distance = pd.DataFrame(distances)
self_perceived = perceived_distance[perceived_distance['x']=='self']

# calculate objective distances
from itertools import combinations 
unique_labels = df_actual['label'].unique().tolist() 
pairwise_combinations = list(combinations(unique_labels, 2))

issue_labels = {
    "climate_concern": 1,
    "gay_adoption": 2,
    "migration_enriches_culture": 3,
    "govt_reduce_inequ": 4
}

df_actual['issue_labels'] = df_actual['issue'].map(issue_labels)
df_actual = df_actual.sort_values('issue_labels')

list_topic = []
list_agg = []
for p1, p2 in pairwise_combinations: 
    v1 = df_actual[df_actual['label']==p1]['position'].to_numpy()
    v2 = df_actual[df_actual['label']==p2]['position'].to_numpy()
    t_diff = v1-v2
    a_diff = np.sum(np.abs(v1-v2))

    # save information
    list_topic.append((p1, p2, t_diff))
    list_agg.append((p1, p2, a_diff))

# Build long-format data
long_data = []
for person_a, person_b, values in list_topic:
    for topic, value in zip(issue_labels.keys(), values):
        long_data.append({
            'person_a': person_a,
            'person_b': person_b,
            'topic': topic,
            'value': value
        })
df_topics = pd.DataFrame(long_data)
df_agg = pd.DataFrame(list_agg, columns=['x', 'y', 'delta'])

### okay so finally we have everything ### 

# now we can aggregate or whatever # 
df_self_actual = df_agg[df_agg['x'] == 'self']
merge_perceived_actual = df_self_actual.merge(self_perceived, on = ['x', 'y'], how = 'inner')
merge_perceived_actual['correspondence'] = merge_perceived_actual['euclidean'] / merge_perceived_actual['delta']
merge_perceived_actual
### then measures / models we actually want ###

'''
1. p_dist ~ a_dist
2. p_dist ~ a_dist_i * B--population weight for each topic.
3. p_dist ~ a_dist_i * [scalar_i], ...--where scalar is obtained from data:
-data 1: social contacts (within our survey: individual)
-data 2: parties (within our survey)
-data 3: parties (from external survey)


Where scalar can be: 
1. population average weighting of dimension. 
2. weighting of dimension based on *in group*

And where *in group* can be: 
1. spread (e.g., standard deviation) of social contacts 
2. spread (e.g., standard deviation) of political party (e.g., from our own data or from surveys).

Hypothesis then is: 
1. some topics will be more important for some groups (i.e., better prediction of p_dist).
2. is this just the same (importance) as perceived distance?
-- I maybe wanted to try to decouple these things such that it is actually how you *perceive distance*
-- and not just what you choose to value (importance).


'''