#################################
#####  Analyse data   #####
#################################

import numpy as np
import json
import os
import pandas as pd
from itertools import combinations


folder = "data/"
questions_sc = [
    "climate_concern",
    "gay_adoption",
    "migration_enriches_culture",
    "govt_reduce_inequ",
    ]
filelist = os.listdir(folder)
filelist = [f for f in filelist if ".csv" in f]
print(filelist)
surveyname = "survey"
id=1

# P_ops = {
#     "P1": [0,0, 0,-1],  # LIB
#     "P2": [0, -1, 0, -1], # climate-hoax RIGHT 
#     "P3": [1, 1, 1, 1], # LEFT
#     "P4": [0,  0, -1, 0], # RIGHT
# }

P_ops_Likert = {
     "P1": [3, 3, 3, 5],  # LIB
     "P2": [3, 5, 3, 5], # climate-hoax RIGHT 
     "P3": [1, 1, 1, 1], # LEFT
     "P4": [3, 3, 5, 3], # RIGHT
}

#################################
#####  FUNCTIONS    #####
#################################

def manhattan(df, a, b, questions=questions_sc):
    # a and b need to be "self", 1, 2, 3, P1, P2, ...
    if type(df)==pd.Series:
        return  np.abs(df.loc[a] - df.loc[b])
   
    else:
        return  np.abs(df.loc[questions, [a]].values - df.loc[questions, [b]].values).mean() 
    

def euclidean(df, a, b, questions=questions_sc):
    # a and b need to be self, 1, 2, 3, P1, P2, ...
    if type(df)==pd.Series:
        return  np.linalg.norm(df.loc[a] - df.loc[b])
   
    else:
        return  np.linalg.norm(df.loc[questions, [a]].values - df.loc[questions, [b]].values) 
   
def dist(positions, a, b): 
    # positions needs to be a list of points with labels, x, y
    # a and b need to be "self", "f1", "P1", ...
    pos_labels = [dot["label"] for dot in positions]
    a_ind = pos_labels.index(a)
    b_ind = pos_labels.index(b)
    posa = (positions[a_ind]["x"], positions[a_ind]["y"])
    posb =  (positions[b_ind]["x"], positions[b_ind]["y"])
    return ((posa[0]-posb[0])**2 + (posa[1]-posb[1])**2)**0.5 

#################################
#####  MAIN  #####
#################################

nfriends = 3
nP = 4
typical_voters = ["GreenVoter", "AfDVoter"] 
namesType = (
    ["self"]
    + [f"friend{f}" for f in range(1, nfriends + 1)]
    + typical_voters
    + [f"P{n}" for n in range(1, nP + 1)]
)
categories=dict(zip(namesType, ["self"]+["friend"]*nfriends + ["voter"]*len(typical_voters) + ["P"]*nP))


def get_attributes(x, base, ids):
    return x[[f"{base}{suffix}" for suffix in ids]].values

def build_names(data, code, base, prototypes_party, nfriends, nP):
    self_name = [code]
    friend_names = [data.loc[code, f"{base}friend{n}"] for n in range(1, nfriends + 1)]
    proto_names = prototypes_party
    fixed_names = [f"P{n}" for n in range(1, nP + 1)]
    return self_name + friend_names + proto_names + fixed_names

codes = []
rows = []
columns = ["code", "identity", "observedA", "observedB", "cat_A", "cat_B"]+[f"A_{q}" for q in questions_sc]+[f"B_{q}" for q in questions_sc]+[f"ed_{q}" for q in questions_sc]+["posAx", "posAy", "posBx", "posBy"] + ["euclideanDistance", "perceivedDistance"]
    
for fname in filelist:
    data = pd.read_csv(folder + fname).set_index("participant.code")
    
    for code, x in data.iterrows():
        codes.append(code)
        base = f"{surveyname}.{id}.player."
        
        # Self
        df_op = [get_attributes(x, base, [f"own_{q}" for q in questions_sc])]

        # Friends
        df_op += [
            get_attributes(x, base, [f"f{f}_{q}" for q in questions_sc])
            for f in range(1, nfriends + 1)
        ]

        # Prototypes
        df_op += [
            get_attributes(x, base, [f"{proto}_{q}" for q in questions_sc])
            for proto in typical_voters
        ]

        # Fixed profiles
        df_op += [P_ops_Likert[f"P{n}"] for n in range(1, nP + 1)]

        # Names and types
        df_op = pd.DataFrame(df_op, columns=questions_sc, index=namesType)
        names = build_names(data, code, base, typical_voters, nfriends, nP)
        df_op["name"] = names
        
        df_op = df_op.replace(-999, np.nan)

        # Positions
        pos = pd.DataFrame(json.loads(x[f"{base}positions"])).set_index("label")
        pos = pos.rename(dict(zip(names, namesType)))
        df_op["xPos"] = pos.loc[df_op.index, "x"]
        df_op["yPos"] = pos.loc[df_op.index, "y"]


        for (A, B) in combinations(df_op.index, 2):
            diff = abs(df_op.loc[A,questions_sc] - df_op.loc[B, questions_sc])
            xA, yA = df_op.loc[A, ['xPos', 'yPos']]
            xB, yB = df_op.loc[B, ['xPos', 'yPos']]
            pos_dist = np.sqrt((xA - xB)**2 + (yA - yB)**2)
            row = [code, x[base+"feel_closest_party"]] +\
                [A, B] + \
                [categories[A], categories[B]]+\
                list(df_op.loc[A,questions_sc].values) + \
                list(df_op.loc[B,questions_sc].values) + \
                list(diff.values) + \
                [xA, yA] + [xB, yB] + \
                [np.linalg.norm(diff.values), pos_dist] 
            rows.append(pd.Series(row, index=columns))

diff_df = pd.DataFrame(rows, columns=columns)

diff_df.to_csv("cleandata/pilot_internal_preprocessed.csv", index=False)


import seaborn as sns
ax = sns.scatterplot(diff_df, x="euclideanDistance", y="perceivedDistance", hue="cat_B")
