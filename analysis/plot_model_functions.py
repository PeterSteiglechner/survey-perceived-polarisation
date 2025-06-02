# plot model functions



import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import arviz as az
from preprocessing import questions_sc
questions_short = dict(zip(questions_sc, ["cc", "adopt", "migr", "inequ"]))


supersmallfs = 6
smallfs = 7
bigfs= 9
plt.rcParams.update({"font.size":smallfs})
plt.rcParams.update({"axes.labelsize":bigfs})
plt.rcParams.update({"axes.titlesize":bigfs})


cmapObs = dict(P1="#FD021A", P2="#FD6702", P3="#FD0298", P4="#FAE705", friend1 = "#43ED1D", friend2="#43ED1D", friend3="#43ED1D", GreenVoter ="#46962b", AfDVoter ="#009ee0")
x_range = np.linspace(0,1, 101)

def plot_rawData(df):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    title = f"perceived distance over euclidean distance"
    ax.set_title(title, fontsize=smallfs)
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/data.png", dpi=600)
    return fig, ax



def plot_model1(df, summary):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    title = f"pd = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} × ed"
    ax.plot(x_range, summary['mean'][f'intercept'] + summary['mean'][f'slope'] * x_range, color='red', label='code', clip_on=False)
    ax.set_title(title, fontsize=smallfs)
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model1.png", dpi=600)
    return fig, ax

def plot_model2(df, summary):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        d_c = df.loc[df.code==code]
        ax.plot(x_range, summary['mean'][f'intercepts[{n}]'] + summary['mean'][f'slopes[{n}]'] * x_range, 
        color='red', label='code', clip_on=False)
        ax.set_title(f"{code}:\n"+ f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} + {summary['mean'][f'slopes[{n}]']:.2f} × ed ", fontsize=smallfs)
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                        fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model2.png", dpi=600)
    return fig, axs

def plot_model3(df, summary):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    mean_pred = summary['mean'][f'intercept'] + sum([summary['mean'][f'slopes[{n}]'] * x_range for n in range(len(questions_sc))])
    ax.plot(x_range, mean_pred, color='red', label='code', clip_on=False)
    ax.set_title(f"M3: \n"+ f"pd = {summary['mean'][f'intercept']:.2f} + \n +"+" +\n+  ".join([f"{summary['mean'][f'slopes[{n}]']:.2f} × ed_{q}" for n, q in enumerate(questions_short)]), fontsize=smallfs)
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model3.png", dpi=600)
    return fig, ax

def plot_model4(df, summary):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        d_c = df.loc[df.code==code]
        ax.plot(x_range, summary.loc[f'intercepts[{n}]']["mean"] + 
                sum([summary.loc[f'slopes[{nq}, {n}]']["mean"] * x_range for nq in range(len(questions_sc))]),                color='red', label='code', clip_on=False)
        ax.set_title(f"{code}:\n"+ f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} +\n"+"+ \n".join([f"{summary['mean'][f'slopes[{nq}, {n}]']:.2f} × ed_{q}" for nq, (q_old, q) in enumerate(questions_short.items())]), fontsize=supersmallfs)
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                        fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model4.png", dpi=600)
    return fig, axs











def plot_model1nl(df, summary):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    title = f"pd = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} × ed^{summary['mean']['alpha']:.2f}"
    ax.plot(x_range, summary['mean'][f'intercept'] + summary['mean'][f'slope'] * x_range**summary["mean"]['alpha'], color='red', label='code', clip_on=False)
    ax.set_title(title, fontsize=smallfs)
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model1nl.png", dpi=600)
    return fig, ax


def plot_model2nl(df, summary):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        d_c = df.loc[df.code==code]
        ax.plot(x_range, summary['mean'][f'intercepts[{n}]'] + summary['mean'][f'slopes[{n}]'] * x_range**(summary["mean"][f"alphas[{n}]"]), 
        color='red', label='code', clip_on=False)
        ax.set_title(
            f"{code}:\n"+ \
            f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} + {summary['mean'][f'slopes[{n}]']:.2f} × ed^{summary['mean'][f'alphas[{n}]']:.2f} ", 
            fontsize=smallfs)
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                        fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model2nl.png", dpi=600)
    return fig, axs





def plot_model3nl(df, summary):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    mean_pred = summary['mean'][f'intercept'] + sum([summary['mean'][f'slopes[{n}]'] * x_range**(summary['mean'][f'alpha']) for n in range(len(questions_sc))])
    ax.plot(x_range, mean_pred, color='red', label='code', clip_on=False)
    ax.set_title(f"M3: \n"+ f"pd = {summary['mean'][f'intercept']:.2f} + \n +"+" +\n+  ".join([f"{summary['mean'][f'slopes[{n}]']:.2f} × ed_{q}^{summary['mean'][f'alpha']:.2f}" for n, q in enumerate(questions_short)]), fontsize=smallfs)
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model3nl.png", dpi=600)
    return fig, ax
def plot_model4nl(df, summary):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        d_c = df.loc[df.code==code]
        predicted = summary.loc[f'intercepts[{n}]']["mean"] + sum([summary.loc[f'slopes[{nq}, {n}]']["mean"] * x_range**summary.loc[f'alphas[{n}]']["mean"] for nq in range(len(questions_sc))])
        ax.plot(x_range, predicted,color='red', label='code', clip_on=False)
        ax.set_title(f"{code}:\n"+ f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} +\n"+"+ \n".join([f"{summary['mean'][f'slopes[{nq}, {n}]']:.2f} × ed_{q}^{summary['mean'][f'alphas[{n}]']:.2f}" for nq, (q_old, q) in enumerate(questions_short.items())]), fontsize=supersmallfs)
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01), fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model4nl.png", dpi=600)
    return fig, axs

