#################################
#####  Analyse data   #####
#################################

import numpy as np
import json
import os
import pandas as pd
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

P_ops = {
    "P1": [0,0, 0,-1],  # LIB
    "P2": [0, -1, 0, -1], # climate-hoax RIGHT 
    "P3": [1, 1, 1, 1], # LEFT
    "P4": [0,  0, -1, 0], # RIGHT
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

func = "euclidean"
opDist = manhattan if func=="manhattan" else euclidean

prototypes_party = ["GreenVoter", "AfDVoter"] 

df_op_arr = []
for fname in filelist:
    print(fname)
    data = pd.read_csv(folder+fname).set_index("participant.code")

    for code, x in data.iterrows():
        df_op = []
        
        df_op.append(x[[f'{surveyname}.{id}.player.own_{q}' for q in questions_sc]].values)
        
        namesType = ["self"]+\
            [f"friend{f}" for f in range(1, nfriends+1)] +\
            prototypes_party +\
            [f"P{n}" for n in range(1,nP+1)]

        names = [code]+\
            [data.loc[code, f"{surveyname}.{id}.player.friend{n}"] for n in range(1, nfriends+1)] +\
            prototypes_party +\
            [f"P{n}" for n in range(1,nP+1)]

        for f_id in range(1,nfriends+1):
            df_op.append(x[[f"{surveyname}.{id}.player.f{f_id}_{q}" for q in questions_sc]].values)
        
        for p_id  in prototypes_party:
            df_op.append(x[[f"{surveyname}.{id}.player.{p_id}_{q}" for q in questions_sc]].values)
        
        for p_id in range(1,nP+1):
            df_op.append(P_ops[f"P{p_id}"])  
        
        df_op = pd.DataFrame(df_op, columns=questions_sc, index=namesType)
        df_op["name"] = names
        df_op = df_op.replace([-999], np.nan)

        pos = json.loads(x[f'{surveyname}.{id}.player.positions'])
        df_op["perceived_distance"] = [np.nan] + [dist(pos, "self", f) for f in names[1:]]
        
        df_op["manhattan_distance"] = [np.nan] + [manhattan(df_op.T, "self", f) for f in namesType[1:]]
        
        df_op["euclidean_distance"] = [np.nan] + [euclidean(df_op.T, "self", f) for f in namesType[1:]]
                
        # make long format:
        df_op_long = df_op.reset_index()
        df_op_long["code"] = code


        df_op_long = df_op_long.melt(id_vars=["code", "index"], var_name="question", value_name="response").rename(columns={"index":"id"})        
        df_op_arr.append(df_op_long)

# this format is pretty crazy though (i.e., saving a ton of very different things in the question column)
df = pd.concat(df_op_arr)
df.to_csv("cleandata/pilot_internal.csv", index=False)


#################################
#####  prediction-ready dataframe   #####
#################################

observed = []
observed.extend([f"friend{f}" for f in range(1, nfriends+1)])
observed.extend([f"P{f}" for f in range(1, nP+1)])
observed.extend(prototypes_party)
observed_cat = ["friend"] * nfriends + ["P"] * nP + ["voter"] * len(prototypes_party)

codes = df.code.unique()

df = df.set_index(["code", "id", "question"])

results = []
for code in codes: 
    myops = df.loc[[(code, "self", q) for q in questions_sc],"response"]
    for obs, obs_cat in zip(observed, observed_cat):
        otherops = df.loc[[(code, obs, q) for q in questions_sc],"response"]
        d = otherops.values - myops.values

        res = [code, obs, obs_cat]
        res.extend(d)
        res.append(df.loc[(code, obs, "euclidean_distance"), "response"])
        res.append(df.loc[(code, obs, "perceived_distance"), "response"])
        
        results.append(res)
df_for_predict = pd.DataFrame(results, columns=["code", "observed", "category"]+[f"d_{q}" for q in questions_sc]+["euclideanDistance",  "perceivedDistance"])
df_for_predict 


import seaborn as sns
sns.scatterplot(df_for_predict, x="euclideanDistance", y="perceivedDistance")