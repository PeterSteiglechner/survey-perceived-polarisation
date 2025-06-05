# run pymc models


#%%
import arviz as az 
import numpy as np 
import pymc as pm
#import pytensor.tensor as pt 
import pandas as pd 
import seaborn as sns
import xarray as xr 
from itertools import combinations 
from models import model1, model2, model3, model4, model1NL, model2NL, model3NL, model4NL
from plot_model_functions import *
from preprocessing import questions_sc as questions
questions_short = dict(zip(questions, ["cc", "adopt", "migr", "inequ"]))

#%% load data

dims = (600, 600)
maxPD = (dims[0]**2+dims[1]**2)**0.5
Nquestions = 4.
Lik = 5.
maxED = (Nquestions*(Lik-1)**2)**0.5

df = pd.read_csv('cleandata/pilot_internal_preprocessed.csv')
n_participants = df['code'].nunique()
df.loc[:, "perceivedDistance"] = df["perceivedDistance"] / maxPD
df.loc[:, "euclideanDistance"] = df["euclideanDistance"] / maxED
df[[f"ed_{q}" for q in questions]] = df[[f"ed_{q}" for q in questions]].abs() / (Lik-1)
# clean
df = df.loc[df[[f"ed_{q}" for q in questions] + ["euclideanDistance", "perceivedDistance"]].isna().sum
(axis=1)==0]


# %% 
plot_rawData(df)
# %%
#################################
#####  FIT LINEAR MODELS   #####
#################################
# random seed
RANDOM_SEED = 7353
rng = np.random.default_rng(RANDOM_SEED)

with model1(df) as m1:
    trace1 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples1 = pm.sample_posterior_predictive(trace1)
summary1 = az.summary(trace1)

with model2(df) as m2:
    trace2 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples2 = pm.sample_posterior_predictive(trace2)
summary2 = az.summary(trace2)


with model3(df, questions=questions) as m3:
    trace3 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples3 = pm.sample_posterior_predictive(trace3)
summary3 = az.summary(trace3)

with model4(df, questions=questions) as m4:
    trace4 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples4 = pm.sample_posterior_predictive(trace4)
summary4 = az.summary(trace4)

#%% 

#################################
#####  NON Linear   #####
#################################

with model1NL(df) as m1nl:
    trace1nl = pm.sample(1000, tune=100, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples1nl = pm.sample_posterior_predictive(trace1nl)
summary1nl = az.summary(trace1nl)

with model2NL(df) as m2nl:
    trace2nl = pm.sample(1000, tune=100, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples2nl = pm.sample_posterior_predictive(trace2nl)
summary2nl = az.summary(trace2nl)

with model3NL(df, questions=questions) as m3nl:
    trace3nl = pm.sample(1000, tune=100, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples3nl = pm.sample_posterior_predictive(trace3nl)
summary3nl = az.summary(trace3nl)

with model4NL(df, questions=questions) as m4nl:
    trace4nl = pm.sample(1000, tune=100, return_inferencedata=True, target_accept=0.95, idata_kwargs={"log_likelihood": True})
    posterior_samples4nl = pm.sample_posterior_predictive(trace4nl)
summary4nl = az.summary(trace4nl)

#%%
fig, axs = plot_model1(df, summary1)
fig, axs = plot_model2(df, summary2)
for q in questions:
    fig, axs = plot_model3(df, summary3, q)
    fig, axs = plot_model4(df, summary4, q)

#%%

fig, axs = plot_model1(df, summary1nl, linear=False)
fig, axs = plot_model2(df, summary2nl, linear=False)
for q in questions:
    fig, axs = plot_model3(df, summary3nl, q, linear=False)
    fig, axs = plot_model4(df, summary4nl, q, linear=False)



#%%
#################################
#####  MODEL COMPARISON   #####
#################################
traces = {'model1': trace1, 'model2': trace2, "model3":trace3, "model4":trace4,'model1nl': trace1nl, 'model2nl': trace2nl, "model3nl":trace3nl, "model4nl":trace4nl}
loos = {}
for m, t in traces.items():
    loos[m] = az.loo(t)
# Compare the models
comparison = az.compare(traces)
comparison

az.plot_compare(comparison)


# %%
# #################################
#####  ANALYSE MODEL 4 BY GROUP/IDENTITY/INDIVIDUAL  #####
#################################


# group by partisan identity

meta = df[["code", "identity"]].set_index("code")
meta = meta[~meta.index.duplicated(keep='first')].to_dict()["identity"]
codes = df.code.unique()
slopes = []
for nq, q in enumerate(questions):
    res = summary4.loc[[s for s in summary4.index if f"slopes[{nq}," in s], "mean"].values
    resSD = summary4.loc[[s for s in summary4.index if f"slopes[{nq}," in s], "sd"].values
    for nc, code in enumerate(codes):
        slopes.append([code, meta[code], q, res[nc], resSD[nc]])
slopes = pd.DataFrame(slopes, columns=["code", "who", "qu", "slopeMean", "slopeStd"])


import seaborn as sns
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,1, figsize=(9, 6))
sns.boxplot(data=slopes, x='qu', y='slopeMean', hue='who', showcaps=True, boxprops={'alpha':0.3}, showfliers=False, whis=[0,100], ax=ax)
sns.stripplot(data=slopes, x='qu', y='slopeMean', hue='who', 
              dodge=True, alpha=0.8, jitter=True, size=10, ax=ax)
ax.set_xlabel("question")
ax.set_ylabel("mean regression slope")
ax.legend(title="Survey Participant", loc='upper right')
ax.set_ylim(0,)
fig.tight_layout()


# %%

# group by Victor/Peter
meta = pd.read_csv("data/meta/codes.csv", delimiter=",").set_index("code").to_dict()["participant"]
codes = df.code.unique()

slopes = []
for nq, q in enumerate(questions):
    print(q)
    res = summary4.loc[[s for s in summary4.index if f"slopes[{nq}," in s], "mean"].values
    resSD = summary4.loc[[s for s in summary4.index if f"slopes[{nq}," in s], "sd"].values
    for nc, code in enumerate(codes):
        slopes.append([code, meta[code], q, res[nc], resSD[nc]])
slopes = pd.DataFrame(slopes, columns=["code", "who", "qu", "slopeMean", "slopeStd"])

fig, ax = plt.subplots(1,1, figsize=(9, 6))
sns.boxplot(data=slopes, x='qu', y='slopeMean', hue='who', showcaps=True, boxprops={'alpha':0.3}, showfliers=False, whis=[0,100], ax=ax)
sns.stripplot(data=slopes, x='qu', y='slopeMean', hue='who', 
              dodge=True, alpha=0.8, jitter=True, size=10, ax=ax)
ax.set_xlabel("question")
ax.set_ylabel("mean regression slope")
ax.legend(title="Survey Participant", loc='upper right')
ax.set_ylim(0,)
fig.tight_layout()
# %%
