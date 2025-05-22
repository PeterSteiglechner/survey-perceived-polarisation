import pymc as pm
import pandas as pd

def model1(data):
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=0.3)
        slope = pm.Normal('slope', mu=1, sigma=0.7)
        sigma = pm.Exponential('sigma', 4)

        mu = intercept + slope * data['euclideanDistance'].values

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model


def model2(data):
    data['code_idx'] = pd.Categorical(data['code']).codes
    n_codes = len(data['code_idx'].unique())

    with pm.Model() as model:
        mu_intercept = pm.Normal('mu_intercept', mu=0, sigma=1)
        sigma_intercept = pm.HalfNormal('sigma_intercept', sigma=1)

        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)

        intercepts = pm.Normal('intercepts', mu=mu_intercept, sigma=sigma_intercept, shape=n_codes)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=n_codes)

        sigma = pm.Exponential('sigma', 4)

        mu = intercepts[data['code_idx']] + slopes[data['code_idx']] * data['euclideanDistance'].values

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model



def model3(data):
    #qu = [c[2:] for c in data.columns if "d_" in c]
    e_k = [c for c in data.columns if "d_" in c]
    with pm.Model() as model:
        intercept = pm.HalfNormal('intercept', sigma=0.3)
        mu_slope = pm.Normal('mu_slope', mu=1, sigma=1)
        sigma_slope = pm.HalfNormal('sigma_slope', sigma=1)
        slopes = pm.Normal('slopes', mu=mu_slope, sigma=sigma_slope, shape=len(e_k))

        sigma = pm.Exponential('sigma', 4)

        mu = intercept + sum([
            slopes[nk] * data[k].values for nk, k in enumerate(e_k)
        ])

        pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['perceivedDistance'].values)
    return model

