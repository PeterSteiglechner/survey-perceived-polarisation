#%%
import arviz as az 
import matplotlib.pyplot as plt 
import numpy as np 
import pymc as pm
import pytensor.tensor as pt 
import pandas as pd 
import seaborn as sns
import xarray as xr 
from models import model1, model2, model3
from preprocessing import questions_sc


az.style.use("arviz-darkgrid")
smallfs = 7
bigfs = 9
supersmallfs = 6
plt.rcParams.update({'font.size': smallfs, 'axes.titlesize':bigfs})
plt.rc('axes', labelsize=bigfs)    # fontsize of the x and y labels
plt.rc('legend',fontsize=smallfs)
plt.rc('legend',title_fontsize=smallfs)
plt.rc('xtick', labelsize=smallfs)    # fontsize of the tick labels
plt.rc('ytick', labelsize=smallfs)    # fontsize of the tick labels

# random seed
RANDOM_SEED = 3251
rng = np.random.default_rng(RANDOM_SEED)

dims = (600, 600)
maxPD = (dims[0]**2+dims[1]**2)**0.5
Nquestions = 4
Lik = 5
maxED = (Nquestions*(Lik-1)**2)**0.5

# load data 
df = pd.read_csv('cleandata/pilot_internal_preprocessed.csv')
n_participants = df['code'].nunique()
data = df 
data.loc[:, "perceivedDistance"] = data["perceivedDistance"] / maxPD
data.loc[:, "euclideanDistance"] = data["euclideanDistance"] / maxED
for q in questions_sc:
    data.loc[:, f"d_{q}"] = abs(data[f"d_{q}"]) / Lik
# clean
data = data.loc[df[[f"d_{q}" for q in questions_sc] + ["euclideanDistance", "perceivedDistance"]].isna().sum(axis=1)==0]

#%%
#################################
#####  PLOT DATA   #####
#################################
cmapObs = dict(P1="#FD021A", P2="#FD6702", P3="#FD0298", P4="#FAE705", friend1 = "#9C8563", friend2="#979C63", friend3="#9C6863", GreenVoter ="#46962b", AfDVoter ="#009ee0")

fig, ax = plt.subplots(1,1,figsize=(12/2.54, 9/2.54))
sns.scatterplot(data, x="euclideanDistance", y="perceivedDistance", hue="observed", legend=False, palette=cmapObs, style="code")
for i, txt in enumerate(data['observed']):
     ax.annotate(txt, (data['euclideanDistance'].iloc[i]+0.01, data['perceivedDistance'].iloc[i]+0.01),
                  fontsize=supersmallfs, alpha=0.7)
ax.set_xlabel('Euclidean Distance')
ax.set_ylabel('Perceived Distance')
ax.set_title('Relationship between Euclidean and Perceived Distances')
ax.grid(True)
fig.tight_layout()
plt.savefig("figs/m1.png")

#%%
#################################
#####  MODEL 1   #####
#################################
# Use base model
with model1(data) as M1:
    trace1 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.9)

# Print summary statistics of the model
summary = az.summary(trace1)
print("\nModel Summary:")
print(summary)

#%% Plot the posterior distributions
az.plot_trace(trace1)
plt.tight_layout()
plt.show()

#%%
#################################
#####  Plot Prior   #####
#################################
with M1:
    idata = pm.sample_prior_predictive(draws=20, random_seed=rng)

_, ax = plt.subplots()

x = xr.DataArray(np.linspace(0, 1,20), dims=["plot_dim"])
prior = idata.prior
y = prior["intercept"] + prior["slope"] * x

ax.plot(x, y.stack(sample=("chain", "draw")), c="k", alpha=0.4)

ax.set_xlabel("Predictor (stdz)")
ax.set_ylabel("Mean Outcome (stdz)")
ax.set_title("Prior predictive checks -- Half-Normal intercept & Normal slope priors");

#%% # posterior predictive check
with M1:
    posterior_predictive = pm.sample_posterior_predictive(trace1, return_inferencedata=True)
    
x = data['euclideanDistance']
sort_idx = np.argsort(x.values)
y_obs = data['perceivedDistance']
y_pred_samples = posterior_predictive.posterior_predictive['likelihood'].stack(sample=("chain", "draw")).values.T  # shape: (samples, observations)

# Compute mean and credible interval from predictions
y_pred_mean = y_pred_samples.mean(axis=0)
y_pred_hpd = az.hdi(y_pred_samples, hdi_prob=0.94)

# Sort x and corresponding predictions
x_s = x.values[sort_idx]
y_obs_s = y_obs.values[sort_idx]
y_pred_mean_s = y_pred_mean[sort_idx]
y_pred_hpd_s = y_pred_hpd[sort_idx]

plt.scatter(x_s, y_obs_s, color='black', label='Observed')
plt.plot(x_s, y_pred_mean_s, color='blue', label='Predicted Mean')
plt.fill_between(x_s, y_pred_hpd_s[:, 0], y_pred_hpd_s[:, 1], color='blue', alpha=0.3, label='94% Credible Interval')
plt.xlabel('euclideanDistance')
plt.ylabel('perceivedDistance')
plt.legend()
plt.title("Posterior Predictive Check")
plt.show()



#%%  # Compute and print the Bayesian R-squared
with M1:
    posterior_samples = pm.sample_posterior_predictive(trace1)
    
# Extract the predicted values
y_pred = posterior_samples.posterior_predictive["likelihood"].mean(dim=["chain", "draw"]).values
y_true = data['perceivedDistance'].values

# Calculate mean of observed data
y_mean = np.mean(y_true)
# Calculate total sum of squares
ss_tot = np.sum((y_true - y_mean) ** 2)
# Calculate residual sum of squares
ss_res = np.sum((y_true - y_pred) ** 2)
# Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f"Bayesian R-squared: {r_squared:.4f}")

regression_equ = f"perc-dist = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} × eucl-dist "+rf"($R^2$: {r_squared:.4f})"
cis = f"95% CIs:\nintercept: [{summary['hdi_3%']['intercept']:.2f}, {summary['hdi_97%']['intercept']:.2f}]\nslope: [{summary['hdi_3%']['slope']:.2f}, {summary['hdi_97%']['slope']:.2f}]"
print(f"\nRegression Equation: \n{regression_equ}")
print(cis)



#%% # plot data+lines   

#################################
#####  PLOT WITH LINE   #####
#################################
def plot_dataLines_model1(data, trace, cmapObs):
    summary = az.summary(trace)
    regression_equ = f"perc-dist = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} × eucl-dist "+rf"($R^2$: {r_squared:.4f})"
    cis = f"95% CIs:\nintercept: [{summary['hdi_3%']['intercept']:.2f}, {summary['hdi_97%']['intercept']:.2f}]\nslope: [{summary['hdi_3%']['slope']:.2f}, {summary['hdi_97%']['slope']:.2f}]"
    fig, ax = plt.subplots(1,1,figsize=(18/2.54, 14/2.54))
    sns.scatterplot(data, x="euclideanDistance", y="perceivedDistance", hue="observed", style="code", legend=False, palette=cmapObs)
    for i, txt in enumerate(data['observed']):
        ax.annotate(txt, (data['euclideanDistance'].iloc[i]+0.01, data['perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)

    # Extract posterior samples
    posterior_samples = trace.posterior.stack(samples=("chain", "draw"))
    intercept_samples = posterior_samples['intercept'].values
    slope_samples = posterior_samples['slope'].values

    # Create grid for prediction
    x_range = np.linspace(0, 1, 100)
    # Plot a subset of posterior regression lines
    for i in range(0, len(intercept_samples), 20):  # Plot every 20th sample
        ax.plot(x_range, intercept_samples[i] + slope_samples[i] * x_range, 
                color='gray', alpha=0.1)
    # Plot the average regression line
    ax.plot(x_range, summary['mean']['intercept'] + summary['mean']['slope'] * x_range, 
            color='red', label='Mean Regression Line')
    ax.legend()
    # Add labels for data points
    for i, txt in enumerate(data['observed']):
        plt.annotate(txt, (data['euclideanDistance'].iloc[i]+0.01, data['perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlabel('Euclidean Distance')
    ax.set_ylabel('Perceived Distance')
    ax.text(0.95, 0.05, cis, fontsize=smallfs, ha="right", va="bottom", transform=ax.transAxes)
    ax.set_title(f'Model 1: {regression_equ}')
    ax.grid(True)
    fig.tight_layout()

    return

plot_dataLines_model1(data, trace1, cmapObs=cmapObs)





#%% # Plot the residuals
plt.figure(figsize=(10, 6))
residuals = y_true - y_pred
plt.scatter(data['euclideanDistance'], residuals)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Euclidean Distance')
plt.ylabel('Residuals')
plt.title('Residuals vs Euclidean Distance')
plt.grid(True)
plt.tight_layout()
plt.show()

# #%%
# # Check if there are any systematic patterns based on 'observed' categories
# plt.figure(figsize=(12, 6))
# categories = data['observed'].unique()
# colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
# color_dict = dict(zip(categories, colors))

# for i, row in data.iterrows():
#     plt.scatter(row['euclideanDistance'], row['perceivedDistance'], 
#                 color=color_dict[row['observed']], 
#                 label=row['observed'])

# # Create a proper legend without duplicates
# handles, labels = plt.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# plt.legend(by_label.values(), by_label.keys(), title='Category')

# # Plot regression line
# plt.plot(x_range, summary['mean']['intercept'] + summary['mean']['slope'] * x_range, 
#          color='black', linestyle='--')

# plt.xlabel('Euclidean Distance')
# plt.ylabel('Perceived Distance')
# plt.title('Relationship by Category')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

#%%
# Print interpretation
print("\nInterpretation of the Model:")
print(f"The model suggests that for each unit increase in Euclidean distance, ")
print(f"the perceived distance increases by approximately {summary['mean']['slope']:.2f} units.")
print(f"The baseline perceived distance (when Euclidean distance is 0) is approximately {summary['mean']['intercept']:.2f} units.")
print(f"The residual standard deviation (sigma) is {summary['mean']['sigma']:.2f}, representing the typical deviation")
print(f"of observed values from the predicted regression line.")




# # formulate PyMC models

# # simplest model (with varying intercepts)
# with pm.Model() as model_1:
#     # priors 
#     alpha = pm.Normal("alpha", mu=0, sigma=10)
#     beta = pm.Normal("beta", mu=0, sigma=10)
    
#     # random intercepts for each ID
#     sigma_alpha_id = pm.Exponential("sigma_alpha_id", 1.0)
#     alpha_id_offset = pm.Normal("alpha_id_offset", mu=0, sigma=1, shape=n_participants)
#     alpha_id = pm.Deterministic("alpha_id", alpha_id_offset * sigma_alpha_id)
    
#     # expected value
#     mu = alpha + alpha_id[df["code"]] + beta * df['X']    



#%%
#################################
#####  MODEL 2   #####
#################################


with model2(data) as m2:
    trace2 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.9)
summary2 = az.summary(trace2)

# %%
fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
for n, (code, ax) in enumerate(zip(data.code.unique(), axs.flatten())):
    d_c = data.loc[data.code==code]
    x_range = np.linspace(0,1, 101)
    # Plot the average regression line
    ax.plot(x_range, summary2['mean'][f'intercepts[{n}]'] + summary2['mean'][f'slopes[{n}]'] * x_range, 
            color='red', label='code', clip_on=False)
    ax.set_title(f"{code}:\n"+ f"pd = {summary2['mean'][f'intercepts[{n}]']:.2f} + {summary2['mean'][f'slopes[{n}]']:.2f} × ed ", fontsize=smallfs)

    sns.scatterplot(d_c, ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observed", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(d_c['observed']):
        ax.annotate(txt, (d_c['euclideanDistance'].iloc[i]+0.01, d_c['perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
fig.tight_layout()
plt.savefig("figs/m2.png", dpi=600)
# %%


#%%
#################################
#####  MODEL 3   #####
#################################
from models import model3

with model3(data) as M3:
    trace3 = pm.sample(1000, tune=1000, return_inferencedata=True, target_accept=0.9)
summary3 = az.summary(trace3)
# %%
fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(18/2.54,14/2.54))
qu  = [c[2:] for c in data.columns if "d_" in c]
x_range = np.linspace(0,1, 101)
# Plot the average regression line
mean_pred = summary3['mean'][f'intercept'] + sum([summary3['mean'][f'slopes[{n}]'] * x_range for n in range(len(qu))])
ax.plot(x_range, mean_pred, 
            color='red', label='code', clip_on=False)
ax.set_title(f"M3: \n"+ f"pd = {summary3['mean'][f'intercept']:.2f} + \n +"+" +\n+  ".join([f"{summary3['mean'][f'slopes[{n}]']:.2f} × ed_{q}" for n, q in enumerate(qu)]), fontsize=smallfs)

sns.scatterplot(data, ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observed", style="code", legend=False, palette=cmapObs, clip_on=False)
for i, txt in enumerate(data['observed']):
    ax.annotate(txt, (data['euclideanDistance'].iloc[i]+0.01, data['perceivedDistance'].iloc[i]+0.01),
                fontsize=supersmallfs, alpha=0.7)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
fig.tight_layout()
plt.savefig("figs/m3.png", dpi=600)
# %%



#%% 

with M1:
    posterior_samples = pm.sample_posterior_predictive(trace1)
    
# Extract the predicted values
y_pred = posterior_samples.posterior_predictive["likelihood"].mean(dim=["chain", "draw"]).values
y_true = data['perceivedDistance'].values

# Calculate mean of observed data
y_mean = np.mean(y_true)
# Calculate total sum of squares
ss_tot = np.sum((y_true - y_mean) ** 2)
# Calculate residual sum of squares
ss_res = np.sum((y_true - y_pred) ** 2)
# Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f"Model 1: Bayesian R-squared: {r_squared:.4f}")



with m2:
    posterior_samples = pm.sample_posterior_predictive(trace2)
    
# Extract the predicted values
y_pred = posterior_samples.posterior_predictive["likelihood"].mean(dim=["chain", "draw"]).values
y_true = data['perceivedDistance'].values

# Calculate mean of observed data
y_mean = np.mean(y_true)
# Calculate total sum of squares
ss_tot = np.sum((y_true - y_mean) ** 2)
# Calculate residual sum of squares
ss_res = np.sum((y_true - y_pred) ** 2)
# Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f"MOdel 2: Bayesian R-squared: {r_squared:.4f}")



with M3:
    posterior_samples = pm.sample_posterior_predictive(trace3)
    
# Extract the predicted values
y_pred = posterior_samples.posterior_predictive["likelihood"].mean(dim=["chain", "draw"]).values
y_true = data['perceivedDistance'].values

# Calculate mean of observed data
y_mean = np.mean(y_true)
# Calculate total sum of squares
ss_tot = np.sum((y_true - y_mean) ** 2)
# Calculate residual sum of squares
ss_res = np.sum((y_true - y_pred) ** 2)
# Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f" Model 3: Bayesian R-squared: {r_squared:.4f}")

# %%
