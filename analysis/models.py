import pymc as pm
import pandas as pd


def model1(data):
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=1)
        slope = pm.Normal('slope', mu=1, sigma=1)
        sigma = pm.Exponential('sigma', 1)

        mu = intercept + slope * data['euclideanDistance'].values

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model


def model2(data):
    data['code_idx'] = pd.Categorical(data['code']).codes
    n_codes = len(data['code_idx'].unique())

    with pm.Model() as model:
        mu_intercept = pm.Normal('mu_intercept', mu=1, sigma=1)
        sigma_intercept = pm.HalfNormal('sigma_intercept', sigma=1)

        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)

        intercepts = pm.Normal('intercepts', mu=mu_intercept, sigma=sigma_intercept, shape=n_codes)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=n_codes)

        sigma = pm.Exponential('sigma', 1)

        mu = intercepts[data['code_idx']] + slopes[data['code_idx']] * data['euclideanDistance'].values

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model



def model3(data, questions):
    e_k = [f"ed_{q}" for q in questions] #[c for c in data.columns if "ed_" in c]
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=1)
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=len(e_k))

        sigma = pm.Exponential('sigma', 1)

        mu = intercept + sum([
            slopes[nk] * data[k].values for nk, k in enumerate(e_k)
        ])

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model

def model4(data, questions):
    data['code_idx'] = pd.Categorical(data['code']).codes
    n_codes = len(data['code_idx'].unique())
    e_k = [f"ed_{q}" for q in questions] 
    with pm.Model() as model:
        mu_intercept = pm.Normal('mu_intercept', mu=1, sigma=1)
        sigma_intercept = pm.HalfNormal('sigma_intercept', sigma=1)
        
                
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)
        
        intercepts = pm.Normal('intercepts', mu=mu_intercept, sigma=sigma_intercept, shape=n_codes)
        
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=(len(e_k), n_codes))
        
        sigma = pm.Exponential('sigma', 1)

        mu = intercepts[data['code_idx']] + sum([
            slopes[nk, data["code_idx"]] * data[k].values for nk, k in enumerate(e_k)
        ])

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model





#################################
#####  NON-LINEAR   #####
#################################

def model1NL(data):
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=1)
        slope = pm.Normal('slope', mu=1, sigma=1)
        sigma = pm.Exponential('sigma', 1)
        alpha = pm.Normal("alpha", mu=1, sigma=1)
        mu = intercept + slope * data['euclideanDistance'].values**alpha

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model


def model2NL(data):
    data['code_idx'] = pd.Categorical(data['code']).codes
    n_codes = len(data['code_idx'].unique())

    with pm.Model() as model:
        mu_intercept = pm.Normal('mu_intercept', mu=1, sigma=1)
        sigma_intercept = pm.HalfNormal('sigma_intercept', sigma=1)
        mu_alpha = pm.Normal("mu_alpha", mu=1, sigma=1)
        sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)

        intercepts = pm.Normal('intercepts', mu=mu_intercept, sigma=sigma_intercept, shape=n_codes)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=n_codes)
        alphas = pm.Normal("alphas", mu=mu_alpha, sigma=sigma_alpha, shape=n_codes)

        sigma = pm.Exponential('sigma', 1)

        mu = intercepts[data['code_idx']] + slopes[data['code_idx']] * data['euclideanDistance'].values**alphas[data['code_idx']]

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model



def model3NL(data, questions):
    e_k = [f"ed_{q}" for q in questions] #[c for c in data.columns if "ed_" in c]
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=1)
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=len(e_k))
        alpha = pm.Normal("alpha", mu=1, sigma=1)

        sigma = pm.Exponential('sigma', 1)

        mu = intercept + sum([
            slopes[nk] * data[k].values**alpha for nk, k in enumerate(e_k)
        ])

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model

def model4NL(data, questions):
    data['code_idx'] = pd.Categorical(data['code']).codes
    n_codes = len(data['code_idx'].unique())
    e_k = [f"ed_{q}" for q in questions] 
    with pm.Model() as model:
        mu_intercept = pm.Normal('mu_intercept', mu=1, sigma=1)
        sigma_intercept = pm.HalfNormal('sigma_intercept', sigma=1)

        mu_alpha = pm.Normal("mu_alpha", mu=1, sigma=1)
        sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)
                
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)
        
        intercepts = pm.Normal('intercepts', mu=mu_intercept, sigma=sigma_intercept, shape=n_codes)
        
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=(len(e_k), n_codes))
        
        alphas = pm.Normal("alphas", mu=mu_alpha, sigma=sigma_alpha, shape=n_codes)

        sigma = pm.Exponential('sigma', 1)

        mu = intercepts[data['code_idx']] + sum([
            slopes[nk, data["code_idx"]] * data[k].values**alphas[data['code_idx']] for nk, k in enumerate(e_k)
        ])

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model