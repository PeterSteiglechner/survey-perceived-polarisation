#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_stata(f"~/csh-research/projects/opinion-data-curation/data/raw/triggerpunkte/ZA8826_v1-0-0.dta", convert_categoricals=False)
#df.set_index("lfdn",inplace=True)


# %%
likert5_de = {1:"Stimme voll und ganz zu", 2:"Stimme eher zu", 3: "Teils/teils", 4:"Stimme eher nicht zu", 5: "Stimme überhaupt nicht zu"}
likert5 = {1:"strongly agree", 2:"agree", 3: "neutral", 4:"disagree", 5: "strongly disagree"}


#%%
questions_text = ['I am very concerned about climate change.', 'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 'It is enriching for cultural life in Germany when migrants come here.', 'The state should take measures to reduce income differences more than before. ']

questions_sc = [
    "climate_concern",
    "gay_adoption",
    "migration_enriches_culture",
    "govt_reduce_inequ",
    ]

questions = ["v401_1a", "v301_1c", "v201_2b", "v104_3a"]


partymap = dict(zip(np.arange(1,10.5), ["SPD", "CDU/CSU", "Grüne","FDP","AfD", "Linke", np.nan, "not_voting"]))
partycolsGE = dict(zip(["CDU/CSU", "SPD", "Linke", "Grüne", "FDP", "AfD", "not_voting"], ["#000000", "#E3000F", "#b61c3e", "#1AA037", "#FFEF00", "#0489DB", "grey"]))  # 

df = df.rename(columns=dict(zip(questions, questions_sc)))
df["identity"] = df["v302"].map(partymap)  # which party would you vote for?


df = df[questions_sc+["identity"]]

#%% 
df
#%%


import sys
from model_functions import *
#%%

parties = ["Linke", "Grüne", "SPD", "FDP", "CDU/CSU", "AfD", "not_voting"]
df["essround"]=1
df["anweight"] = 1
waves = [1]
variables = questions_sc
data = df[["essround", "anweight", "identity"]+variables].dropna(how="any", axis="index")

data[variables] = ((data[variables]-1)/4 * 6+1)

Lenses = inferSubjectiveLenses(data, parties=parties, waves=waves, variables=variables)
Lenses = Lenses[1]

#%%
P_ops = {
    "P1": np.array([1, 1, 1, 1])*4/2+3,
    "P2": np.array([0.5,0.5,0.5,0.5])*4/2+3,
    "P3": np.array([0.2, 0.1, -0.5, 0.2])*4/2+3,
    "P4": np.array([0.05, -0.05, -1, -1])*4/2+3,
}

# P_ops = {
#     "P1": np.array([1, 1, 1, 1])*3+4,
#     "P2": np.array([0.5,0.5,0.5,0.5])*3+4,
#     "P3": np.array([0.2, 0.1, -0.5, 0.2])*3+4,
#     "P4": np.array([0.05, -0.05, -1, -1])*3+4,
# }
#%%
myOp = np.array([3,3,3,3])
predictPdist = []
for P, opP in P_ops.items():
    for id in parties:
        D = Lenses[id]
        d = myOp - opP  # distance vector from observer i
        percD  = np.sum(np.dot(d, D) * d)**(1/2)
        euclD = np.sum(d * d)**(1/2)
        predictPdist.append([id, P, percD, euclD])
predictPdist = pd.DataFrame(predictPdist, columns=["party", "observed", "perceived distance", "euclidean distance"], )
predictPdist.attrs["myOp"] = myOp
#%%

fig, axs = plt.subplots(1,4, sharex=True, sharey=True)
for ax, (P, opP) in zip(axs, P_ops.items()):
    sns.barplot(predictPdist.loc[predictPdist.observed==P], y="perceived distance", x="party", hue="party", palette=partycolsGE, ax=ax)
    ax.set_xticklabels([])
    
    ax.hlines(predictPdist.loc[predictPdist.observed==P]["euclidean distance"], 0, 5)
    ax.set_xticklabels([],alpha=0.4)
    
    ax.set_title(f"{P}")
    ax.text(0.95, 0.95, f"{', '.join([f'{x:.2f}' for x in opP])})", fontsize=9, va="top", ha="right", transform=ax.transAxes)
#%%



# subjDist = subjectiveDistanceMatrix(data[variables].to_numpy(), data[variables].to_numpy(), data["identity"], Lenses[waves[0]])

# meanD = calc_meanPerceivedDisagreement(data, waves=waves, variables=variables, Lenses=Lenses)

# meanObjD = calc_meanObjectiveDisagreement(data, waves=waves, variables=variables)


# # %%


# print(meanD)
# print(meanObjD)

# #%%
# # 
# PxA_meanDist_df, PxP_meanDist_df = calc_meanPerceivedDisagreement_betweenGroups(data, waves, parties, variables, Lenses)




# #%%


# #PxA_meanDist_df[1][1].plot.bar()
# plt.figure()
# obs_p = np.array([a[0] for a in PxP_meanDist_df[1][1].index])
# obd_p = np.array([a[1] for a in PxP_meanDist_df[1][1].index])#[:, 1]#.plot()
# PxP_meanDist_df["obs"] = obs_p
# PxP_meanDist_df["obd"] = obd_p
# PxP_meanDist_df["dist"] = PxP_meanDist_df[1][1]

# sns.heatmap(PxP_meanDist_df.pivot_table(index="obs", columns="obd", values="dist"), cmap="hot_r", vmax=4, vmin=2.5)

# plt.figure()
# sns.barplot(PxA_meanDist_df[1][1].loc[[p[0].lower() for p in parties]])



# #%%

# prototypes = pd.DataFrame([[1,1,1,1], 
#                            [2,1,2,5],
#                            df.loc[df.identity=="Green", variables].mean().values,
#                            df.loc[df.identity=="AfD", variables].mean().values,
#                            df.loc[:, variables].mean().values
#                            ], columns=variables, 
#                            index=[
#                                "activist",
#                                "tech bro",
#                                "afd avg",
#                                "avg"
#                                ])

# means = df.groupby("identity")[variables].mean()
# #%%

# distances = []
# for pname, op in prototypes.iterrows():
#     print(pname, op)
#     for p in means.index:
#         dvec = (means.loc[p] - op).values
#         d = np.sum(np.dot(dvec, Lenses[1][p]) * dvec)**(1/2)
#         dhomo = np.sum(np.dot(dvec, Lenses[1]["None"]) * dvec)**(1/2) 
#         dobj = np.sum(np.dot(dvec, np.diag(np.ones(len(dvec)))) * dvec)**(1/2) 
#         distances.append((pname, p, d, dhomo, dobj))

# distances = pd.DataFrame(distances, columns = ["prototype", "identity", "d_subj_het", "d_subj_hom", "d_obj"])

# # %%
# # 
# fig, ax = plt.subplots(1,1)
# sns.scatterplot(distances, x="d_subj_het", y="d_obj", style="prototype", hue="identity", marker="s", palette=partycolsGE,ax=ax)
# ax.set_aspect("equal")
# ax.plot([0,4], [0,4], color="k", ls="--", zorder=0)