import numpy as np 
import pandas as pd 
import pymc as pm 

# load data 
df = pd.read_csv('cleandata/pilot_internal.csv')
df['question'].unique()

'''
'climate_concern'
'gay_adoption'
'migration_enriches_culture'
'govt_reduce_inequ'
'name'
'perceived_distances'
'manhattan_distances'
'euclidean_distances'
'''

# all of the questions
df_q = df[df['question'].isin([
    'climate_concern', 
    'gay_adoption', 
    'migration_enriches_culture',
    'govt_reduce_inequ'
    ])].drop_duplicates().dropna() # n=400

# always with reference to self I assume
df_d = df[df['question'].isin([
    'perceived_distances',
    'manhattan_distances',
    'euclidean_distances'
]
)].drop_duplicates().dropna() # n=300 (n=270 without NAN).

# but where do we have objective distance on a specific question?
# that is why I do not understand this format at all.