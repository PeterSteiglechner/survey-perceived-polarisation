import arviz as az 
import matplotlib.pyplot as plt 
import numpy as np 
import pymc as pm
import pytensor.tensor as pt 
import pandas as pd 

# random seed
RANDOM_SEED = 3251
rng = np.random.default_rng(RANDOM_SEED)
az.style.use("arviz-darkgrid")

# load data 
df = pd.read_csv('cleandata/pilot_internal_preprocessed.csv')
n_participants = df['code'].nunique()

# formulate PyMC models

# simplest model (with varying intercepts)
with pm.Model() as model_1:
    # priors 
    alpha = pm.Normal("alpha", mu=0, sigma=10)
    beta = pm.Normal("beta", mu=0, sigma=10)
    
    # random intercepts for each ID
    sigma_alpha_id = pm.Exponential("sigma_alpha_id", 1.0)
    alpha_id_offset = pm.Normal("alpha_id_offset", mu=0, sigma=1, shape=n_participants)
    alpha_id = pm.Deterministic("alpha_id", alpha_id_offset * sigma_alpha_id)
    
    # expected value
    mu = alpha + alpha_id[df["ID"]] + beta * df['X']    