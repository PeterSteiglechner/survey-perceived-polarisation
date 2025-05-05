
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
bigfs = 9
smallfs = 7
plt.rcParams.update({"font.size":smallfs})

from model_functions import *

LIKERT5_de = {1:"Stimme voll und ganz zu", 2:"Stimme eher zu", 3: "Teils/teils", 4:"Stimme eher nicht zu", 5: "Stimme überhaupt nicht zu"}
LIKERT5 = {1:"strongly agree", 2:"agree", 3: "neutral", 4:"disagree", 5: "strongly disagree"}
LIKERT5_TO_OP = lambda l: -(l-(1+(5-1)/2))/((5-1)/2)
OP_TO_LIKERT5 = lambda op: (-op+1)/2 * (5-1) + 1
#################################
#####  Group Definitions   #####
#################################
parties = ["Linke", "Grüne", "SPD", "FDP", "CDU/CSU", "AfD", "not_voting"]
response_to_party = dict(zip(np.arange(1,10.5), ["SPD", "CDU/CSU", "Grüne","FDP","AfD", "Linke", np.nan, "not_voting"]))
partycolors = dict(zip(["CDU/CSU", "SPD", "Linke", "Grüne", "FDP", "AfD", "not_voting"], ["#000000", "#E3000F", "#b61c3e", "#1AA037", "#FFEF00", "#0489DB", "grey"]))  # 


#################################
#####  Load data   #####
#################################
df = pd.read_stata(f"~/csh-research/projects/#data/raw/triggerpunkte/ZA8826_v1-0-0.dta", convert_categoricals=False)
#df.set_index("lfdn",inplace=True)


#################################
#####  Select columns and rename   #####
#################################
meta = pd.read_csv("questionaire.csv")
questions_meta = meta.loc[meta["selected"].dropna().index]
polQ = questions_meta.loc[questions_meta.topic!="identity", :] 
vars = polQ["topic"].tolist()
df = df.rename(columns=dict(zip(questions_meta["var"], questions_meta["topic"])))
df["identity"] = df["identity"].map(response_to_party)
df = df[vars+["identity"]]

df["wave"] = 1
df["participant_weight"] = 1
waves = [1]
data = df[["wave", "participant_weight", "identity"]+vars].dropna(how="any", axis="index")
data[vars] = data[vars].map(LIKERT5_TO_OP)

# data.groupby("identity")[vars].mean().plot.bar()
# plt.close()
# y = vars[2]
# sns.violinplot(data, x="identity", y=y, hue="identity", hue_order=parties)
# parties
#################################
#####  Infer lenses   #####
#################################

Lenses = inferSubjectiveLenses(data, parties=parties, waves=waves, variables=vars)
Lenses = Lenses[1]

#################################
#####  Evaluate distances  #####
#################################

# P_ops = {
#     "Pleft":np.array([1,-1,1,1]), # inequality=agree, migration=disagree, minorities=agree, climate=agree
#     "Plib":np.array([-1,0,-1,0]),
#     "Pright":np.array([0,1,-1,-1]), # inequality=neutral, migration=agree, minorities=disagree, cliamte=disagree
# }

P_ops = {
    "Pleft":np.array([1,1,1,1]), # inequality=agree, migration=disagree, minorities=agree, climate=agree
    "Plib":np.array([-1,0,0,0]),
    "Pright":np.array([0,-1,0,0]), # inequality=neutral, migration=agree, minorities=disagree, cliamte=disagree
}


def predict_dist(Lenses,id,self, other):
    D = Lenses[id]
    d = self - other  # distance vector from observer i
    percD  = np.sum(np.dot(d, D) * d)**(1/2)
    euclD = np.sum(d * d)**(1/2)
    return percD, euclD

myOp = LIKERT5_TO_OP(np.array([3,3,3,3]))
predictPdist = []

for P, opP in P_ops.items():
    for id in parties:
        percD, euclD = predict_dist(Lenses, id, myOp, opP)
        predictPdist.append({
             "party": id,
             "observed": P,
             "perceived distance": percD,
             "euclidean distance": euclD
        })

predictPdist = pd.DataFrame(predictPdist)
predictPdist.attrs["myOp"] = myOp


#################################
#####  PLOT   #####
#################################
fig, axs = plt.subplots(1,4, sharex=True, sharey=True, figsize=(16/2.54,9/2.54))
for ax, (P, opP) in zip(axs, P_ops.items()):
    sns.barplot(predictPdist.loc[predictPdist.observed==P], y="perceived distance", x="party", hue="party", palette=partycolors, ax=ax)
    ax.set_xticklabels([])
    
    ax.hlines(predictPdist.loc[predictPdist.observed==P]["euclidean distance"], -0.5, len(parties)-0.5, linestyles=":", color="grey", linewidth=1)
    ax.set_xticklabels([])
    
    ax.set_title(f"{P}")
    ax.text(0.5, 0.98, f"P = ({', '.join([f'{x:.1f}' for x in OP_TO_LIKERT5(opP)])})", fontsize=smallfs, va="top", ha="center", transform=ax.transAxes)

fig.suptitle("Prediction of perceived distance between self and P1 - P4\nfor an individual with opinion "+f"[{', '.join([f'{x:.0f}' for x in OP_TO_LIKERT5(myOp)])}]"+" on a 5-point scale by identity", fontsize=bigfs)
fig.tight_layout()






#################################
#####  Bootstrap   #####
#################################

#from tqdm import tqdm

def bootstrap_predict_distances(data, P_ops, parties, myOp, n_bootstrap=1000, random_state=None):
    rng = np.random.default_rng(random_state)
    bootstrap_results = []
    for b in range(n_bootstrap):#tqdm(range(n_bootstrap), desc="Bootstrapping"):
        resampled_data = data.sample(frac=1, replace=True, random_state=rng.integers(0, 1e9))

        Lenses = inferSubjectiveLenses(resampled_data, parties=parties, waves=waves, variables=vars)[1]  # 1 is the wave here        
        
        for P, opP in P_ops.items():
            for id in parties:
                percD, euclD = predict_dist(Lenses, id, myOp, opP)
                bootstrap_results.append({
                    "party": id,
                    "observed": P,
                    "perceived distance": percD,
                    "euclidean distance": euclD,
                    "bootstrap_iter": b
                })
    return pd.DataFrame(bootstrap_results)

myOp = LIKERT5_TO_OP(np.array([3,3,3,3]))

n_bootstrap = 1000
bootstrap_df = bootstrap_predict_distances(data, P_ops, parties, myOp, n_bootstrap=n_bootstrap)


######### VIS ################
bootstrap_df["party"] = pd.Categorical(bootstrap_df["party"], categories=parties, ordered=True)

fig, axs = plt.subplots(1,1, sharex=True, sharey=True, figsize=(16/2.54,9/2.54))

ax = sns.pointplot(
    data=bootstrap_df,
    x="observed",
    y="perceived distance",
    hue="party",
    palette=partycolors,
    dodge=0.8,
    errorbar=("pi", 95),   # Use 95% percentile interval from raw bootstrapped data
    linestyle='none',
    capsize=0.1,
    err_kws={'linewidth': 1}
)
ax.legend(bbox_to_anchor=(1.025, 1), loc="upper left", fontsize=smallfs)
ax.set_ylim(0,)
ax.vlines(np.arange(0.5, len(P_ops)-0.5), 0, ax.get_ylim()[1], color="gainsboro")
ax.set_xticklabels(
    [f"{p.get_text()}\n[{', '.join([f'{x:.1f}' for x in OP_TO_LIKERT5(P_ops[p.get_text()])])}]" for p in ax.get_xticklabels()], fontsize=smallfs
)
ax.text(0.975, 0.975, f"errorbars = 95% CI from {n_bootstrap} bootstraps", ha="right", va="top", fontsize=smallfs, transform=ax.transAxes)







# #################################
# #####  CROSSVALIDATION   #####
# #################################


# from sklearn.model_selection import StratifiedKFold

# def crossval_predict_distances(data, P_ops, parties, myOp, n_splits=5, random_state=None):
#     results = []
#     skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

#     # Stratify by party identity (for lens inference)
#     y = data["identity"]

#     for fold, (train_idx, test_idx) in enumerate(skf.split(data, y)):
#         train_data = data.iloc[train_idx]
#         #test_data = data.iloc[test_idx]

#         # Infer lenses on training set only
#         Lenses = inferSubjectiveLenses(train_data, parties=parties, waves=waves, variables=vars)
#         Lenses = Lenses[1]

#         for P, opP in P_ops.items():
#             for id in parties:
#                 percD, euclD = predict_dist(Lenses, id, myOp, opP)
#                 results.append({
#                     "party": id,
#                     "observed": P,
#                     "perceived distance": percD,
#                     "euclidean distance": euclD,
#                     "fold": fold
#                 })

#     return pd.DataFrame(results)




# myOp = LIKERT5_TO_OP(np.array([3,3,3,3]))

# n_splits = 5
# crossval_df = crossval_predict_distances(data, P_ops, parties, myOp, n_splits=n_splits)


# ######### VIS ################
# crossval_df["party"] = pd.Categorical(crossval_df["party"], categories=parties, ordered=True)

# fig, axs = plt.subplots(1,1, sharex=True, sharey=True, figsize=(16/2.54,9/2.54))

# ax = sns.pointplot(
#     data=crossval_df,
#     x="observed",
#     y="perceived distance",
#     hue="party",
#     palette=partycolors,
#     dodge=0.8,
#     errorbar=("pi", 95),   # Use 95% percentile interval from raw bootstrapped data
#     linestyle='none',
#     capsize=0.1,
#     err_kws={'linewidth': 1}
# )
# ax.legend(fontsize=smallfs, ncol=2)
# ax.set_ylim(0,)
# ax.vlines(np.arange(0.5, len(P_ops)-0.5), 0, ax.get_ylim()[1], color="gainsboro")
# ax.set_xticklabels(
#     [f"{p.get_text()}\n{', '.join([f'{x:.1f}' for x in OP_TO_LIKERT5(P_ops[p.get_text()])])}" for p in ax.get_xticklabels()], fontsize=smallfs
# )
# ax.text(0.95, 0.95, f"errorbars = 5-95 interval from {n_splits} splits in the cross-validation", ha="right", va="top", fontsize=smallfs, transform=ax.transAxes)


#################################
#####  Data Efficiency   #####
#################################



def subsampling_predict_distances(data, P_ops, parties, myOp, fractions, seeds):
    n_repeats = len(seeds)
    all_results = []
    for frac in fractions:
        for rep, seed in zip(range(n_repeats), seeds):
            subsample = data.sample(frac=frac, replace=False, random_state=seed)
            #print(len(subsample))

            Lenses = inferSubjectiveLenses(subsample, parties=parties, waves=waves, variables=vars)[1]

            for P, opP in P_ops.items():
                for id in parties:
                    percD, euclD = predict_dist(Lenses, id, myOp, opP)
                    all_results.append({
                        "party": id,
                        "observed": P,
                        "perceived distance": percD,
                        "euclidean distance": euclD,
                        "fraction": frac,
                        "repeat": rep
                    })

    return pd.DataFrame(all_results)


fractions = np.linspace(0.3, 1.0, 10)  # 10% to 100%
n_repeats = 10


sampled_results = subsampling_predict_distances(data, P_ops, parties, myOp, fractions, seeds=range(n_repeats))

fig, ax = plt.subplots(1,1, figsize=(16/2.54,9/2.54))

P_test = "Pleft"

ax = sns.lineplot(
    data=sampled_results.loc[sampled_results.observed==P_test],
    x="fraction",
    y="perceived distance",
    hue="party",
    #style="observed",  # optional, if multiple observed profiles
    palette=partycolors,
    estimator="mean",         # mean over repeats
    errorbar=("pi", 95),      # 95% percentile interval over repeats
    marker="o",
    ax=ax,
)

ax.set_title(f"Perceived distance to {P_test} over  dataset size (with 95% CI over {n_repeats} repeats)", fontsize=bigfs)
ax.set_ylabel("Perceived distance", fontsize=bigfs)
ax.set_xlabel("Fraction of data used to infer lenses", fontsize=bigfs)
ax.legend(bbox_to_anchor=(1.025, 1), loc="upper left", fontsize=smallfs)
fig.tight_layout()



#################################
#####  Actual Predictions for each participant   #####
#################################

results = []
for n, (P, op_P) in enumerate(P_ops.items()):
    data[f"euclidean distance"] = data.apply(lambda x: predict_dist(Lenses, x["identity"], x[vars], op_P)[1] , axis=1)
    for v in vars:
        data[f"{v} distance"]  = data[v] - op_P[n]
    data[f"perceived distance"] = data.apply(lambda x: predict_dist(Lenses, x["identity"], x[vars], op_P)[0], axis=1)
    data["P"] = P
    results.append(data.copy())

results = pd.concat(results).reset_index()

results.groupby(["identity", "P"])[f"perceived distance"].mean()

fig, axs = plt.subplots(2, 1, sharex=True)
sns.boxplot(results, x="P", y=f"euclidean distance", hue="identity", palette=partycolors, hue_order=parties, ax=axs[0], legend=False, fliersize=1, whis=[5,95])

sns.boxplot(results, x="P", y=f"perceived distance", hue="identity", palette=partycolors, hue_order=parties, ax=axs[1], legend=False, fliersize=1, whis=[5,95])





#################################
#####  scatter   #####
#################################


fig, axs = plt.subplots(1,2, sharey=True, sharex=True)

for v in vars:
    results[f"{v} abs distance"]  = abs(data[v] - op_P[n])

sns.stripplot(results, x="climate abs distance", y=f"euclidean distance", hue="identity", palette=partycolors, jitter=0.33, size=3, alpha=0.2, ax=axs[0], legend=False)

sns.stripplot(results, x="climate abs distance", y=f"perceived distance", hue="identity", palette=partycolors, jitter=0.33, size=3, alpha=0.2, ax=axs[1], legend=False)

sns.barplot(results, hue="identity", x="identity", y="climate abs distance", palette=partycolors, hue_order=parties, )

plt.figure()
sns.scatterplot(results.groupby(["identity", "climate abs distance"])["perceived distance"].mean().reset_index(), x="climate abs distance", hue="identity", hue_order=parties, palette=partycolors, y="perceived distance")



