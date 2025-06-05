# plot model functions



import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import arviz as az
from preprocessing import questions_sc
questions_short = dict(zip(questions_sc, ["c", "a", "m", "i"]))
questions_shorter = dict(zip(questions_sc, ["cl", "ad", "mi", "in"]))


supersmallfs = 6
smallfs = 7
bigfs= 9
plt.rcParams.update({"font.size":smallfs})
plt.rcParams.update({"axes.labelsize":bigfs})
plt.rcParams.update({"axes.titlesize":bigfs})



def predict_model1_manhattan(summary1, ed_cc, ed_adopt, ed_migr, ed_ineq, linear=True):
    alpha = 1 if linear else summary1.loc[f'alpha', 'mean']
    return (
        summary1.loc['intercept', 'mean']
        + summary1.loc['slope', 'mean'] * sum([np.abs(ed) for ed in [ed_cc, ed_adopt, ed_migr, ed_ineq]])**alpha
    )

def predict_model1(summary1, ed, linear=True):    
    alpha = 1 if linear else summary1.loc[f'alpha', 'mean']
    return (
        summary1.loc['intercept', 'mean']
        + summary1.loc['slope', 'mean'] * ed**alpha
    )

def predict_model2(summary2, ed, n, linear=True):
    #n = list(ed.code.unique()).index(code)
    alpha = 1 if linear else summary2.loc[f'alphas[{n}]', 'mean']
    return (
        summary2.loc[f'intercepts[{n}]', 'mean']
        + summary2.loc[f'slopes[{n}]', 'mean'] * ed**alpha
    )

def predict_model3(summary3, ed_cc, ed_adopt, ed_migr, ed_ineq, linear=True):
    alpha = 1 if linear else summary3.loc[f'alpha', 'mean']
    return (
        summary3.loc['intercept', 'mean']
        + summary3.loc['slopes[0]', 'mean'] * ed_cc**alpha
        + summary3.loc['slopes[1]', 'mean'] * ed_adopt**alpha
        + summary3.loc['slopes[2]', 'mean'] * ed_migr**alpha
        + summary3.loc['slopes[3]', 'mean'] * ed_ineq**alpha
    )

def predict_model4(summary4, ed_cc, ed_adopt, ed_migr, ed_ineq, n, linear=True):
    alpha = 1 if linear else summary4.loc[f'alphas[{n}]', 'mean']
    return (
        summary4.loc[f'intercepts[{n}]', 'mean']
        + summary4.loc[f'slopes[0, {n}]', 'mean'] * ed_cc**alpha
        + summary4.loc[f'slopes[1, {n}]', 'mean'] * ed_adopt**alpha
        + summary4.loc[f'slopes[2, {n}]', 'mean'] * ed_migr**alpha
        + summary4.loc[f'slopes[3, {n}]', 'mean'] * ed_ineq**alpha
    )


cmapObs = dict(P1="#FD021A", P2="#FD6702", P3="#FD0298", P4="#FAE705", friend1 = "#43ED1D", friend2="#43ED1D", friend3="#43ED1D", GreenVoter ="#46962b", AfDVoter ="#009ee0")



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



def plot_model1(df, summary, linear=True):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    title = fr"$pd = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} \cdot d"+("$" if linear else (r"^{"+rf"{summary['mean']['alpha']:.2f}"+r"}$"))
    ax.set_title(title, fontsize=smallfs)

    x_range = df["euclideanDistance"].unique()
    x_range.sort()
    y_pred = predict_model1(summary, x_range, linear=linear)
    
    # plot regression line
    ax.plot(x_range, y_pred, color='red', label='code', clip_on=False)
    # plot: other-other:
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01), fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model1"+("nl" if not linear else "")+".png", dpi=600)
    return fig, ax

def plot_model2(df, summary, linear=True):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        title = f"{code}:\n"+ rf"$pd = {summary['mean'][f'intercepts[{n}]']:.2f} + {summary['mean'][f'slopes[{n}]']:.2f} \cdot d"+("$" if linear else (r"^{"+f"{summary['mean'][f'alphas[{n}]']:.2f}"+r"}$"))
        ax.set_title(title, fontsize=supersmallfs)

        x_range = df.loc[df.code==code, "euclideanDistance"].unique()
        x_range.sort()
        y_pred = predict_model2(summary, x_range, n, linear=linear)
        
        # plot regression line
        ax.plot(x_range, y_pred, color='red', label='code', clip_on=False)
        # plot: other-other:
        d_c = df.loc[df.code==code]
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                        fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    for ax in axs[-1, -2:]:
        ax.axis("off")
    fig.tight_layout()
    plt.savefig(f"figs/model2"+("nl" if not linear else "")+".png", dpi=600)
    return fig, axs

def plot_model3(df, summary, x_var, linear=True):
    fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
    title = fr"$pd = {summary['mean'][f'intercept']:.2f}$ + "+(r" $+$ ").join([fr"${summary['mean'][f'slopes[{nq}]']:.2f} \cdot d_{q}"+(r"$" if linear else (r"^{"+f"{summary['mean']['alpha']:.2f}"+r"}$")) for nq, (q_old, q) in enumerate(questions_short.items())])
    ax.set_title(title, fontsize=smallfs)
    # plot regression
    x = []
    for nq, q in enumerate(questions_sc):
        if x_var==q:
            x_range = df[f"ed_{q}"].unique()
            x_range.sort() 
            x.append(x_range)
        else:
            x.append(df[f"ed_{q}"].mean())
    y_pred = predict_model3(summary, x[0], x[1], x[2], x[3], linear=linear)  
    ax.plot(x_range, y_pred, color='red', clip_on=False)
    # plot other-other
    sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x=f"ed_{x_var}", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
    # plot self-other:
    sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x=f"ed_{x_var}", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
    for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
        ax.annotate(txt, (df.loc[df.observedA=="self", f"ed_{x_var}"].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                    fontsize=supersmallfs, alpha=0.7)
    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(0,1)
    fig.tight_layout()
    plt.savefig(f"figs/model3"+("nl" if not linear else "")+f"_{x_var}.png", dpi=600)
    return fig, ax

def plot_model4(df, summary, x_var, linear=True):
    fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
    for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
        title = f"{code}: "+ rf"$pd = {summary['mean'][f'intercepts[{n}]']:.2f}$ + "+"\n"+ (r"$ +$").join([fr"${summary['mean'][f'slopes[{nq}, {n}]']:.2f} \cdot d_{q}"+("$" if linear else (r"^{"+f"{summary['mean'][f'alphas[{n}]']:.2f}"+r"}$"))+("\n" if nq==1 else "")  for nq, (q_old, q) in enumerate(questions_short.items())])
        ax.set_title(title, fontsize=supersmallfs)

        x = []
        for nq, q in enumerate(questions_sc):
            if x_var==q:
                x_range = df[f"ed_{q}"].unique()
                x_range.sort() 
                x.append(x_range)
            else:
                x.append(df[f"ed_{q}"].mean())
        y_pred = predict_model4(summary, x[0], x[1], x[2], x[3], n, linear=linear) 
        ax.plot(x_range, y_pred,color='red', label='code', clip_on=False)
        d_c = df.loc[df.code==code]
        sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x=f"ed_{x_var}", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
        # plot self-other:
        sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x=f"ed_{x_var}", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
        ax.set_xlabel(f"d_{questions_shorter[x_var]}")
        for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
            ax.annotate(txt, (d_c.loc[d_c.observedA=="self", f"ed_{x_var}"].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
                        fontsize=supersmallfs, alpha=0.7)
    for ax in axs.flatten():
        ax.set_xlim(-0.1,1.1)
        ax.set_ylim(0,1)
    for ax in axs[-1, -2:]:
        ax.axis("off")
    fig.tight_layout()
    plt.savefig(f"figs/model4"+("nl" if not linear else "")+f"_{x_var}.png", dpi=600)
    return fig, axs











# def plot_model1nl(df, summary):
#     fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
#     title = f"pd = {summary['mean']['intercept']:.2f} + {summary['mean']['slope']:.2f} \cdot d^{summary['mean']['alpha']:.2f}"

#     ax.plot(x_range, summary['mean'][f'intercept'] + summary['mean'][f'slope'] * x_range**summary["mean"]['alpha'], color='red', label='code', clip_on=False)
#     ax.set_title(title, fontsize=smallfs)
#     sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
#     # plot self-other:
#     sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
#     for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
#         ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
#                     fontsize=supersmallfs, alpha=0.7)
#     ax.set_xlim(0,1)
#     ax.set_ylim(0,1)
#     fig.tight_layout()
#     plt.savefig(f"figs/model1nl.png", dpi=600)
#     return fig, ax


# def plot_model2nl(df, summary):
#     fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
#     for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
#         d_c = df.loc[df.code==code]
#         ax.plot(x_range, summary['mean'][f'intercepts[{n}]'] + summary['mean'][f'slopes[{n}]'] * x_range**(summary["mean"][f"alphas[{n}]"]), 
#         color='red', label='code', clip_on=False)
#         ax.set_title(
#             f"{code}:\n"+ \
#             f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} + {summary['mean'][f'slopes[{n}]']:.2f} \cdot d^{summary['mean'][f'alphas[{n}]']:.2f} ", 
#             fontsize=smallfs)
#         sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
#         # plot self-other:
#         sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
#         for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
#             ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
#                         fontsize=supersmallfs, alpha=0.7)
#     for ax in axs.flatten():
#         ax.set_xlim(0,1)
#         ax.set_ylim(0,1)
#     fig.tight_layout()
#     plt.savefig(f"figs/model2nl.png", dpi=600)
#     return fig, axs





# def plot_model3nl(df, summary):
#     fig, ax = plt.subplots(1,1, sharex=True, sharey=True, figsize=(12/2.54, 12/2.54))
#     mean_pred = summary['mean'][f'intercept'] + sum([summary['mean'][f'slopes[{n}]'] * x_range**(summary['mean'][f'alpha']) for n in range(len(questions_sc))])
#     ax.plot(x_range, mean_pred, color='red', label='code', clip_on=False)
#     ax.set_title(f"M3: \n"+ f"pd = {summary['mean'][f'intercept']:.2f} + \n +"+" +\n+  ".join([f"{summary['mean'][f'slopes[{n}]']:.2f} \cdot d_{q}^{summary['mean'][f'alpha']:.2f}" for n, q in enumerate(questions_short)]), fontsize=smallfs)
#     sns.scatterplot(df.loc[df.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
#     # plot self-other:
#     sns.scatterplot(df.loc[df.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
#     for i, txt in enumerate(df.loc[df.observedA=="self"]['observedB']):
#         ax.annotate(txt, (df.loc[df.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, df.loc[df.observedA=="self", 'perceivedDistance'].iloc[i]+0.01),
#                     fontsize=supersmallfs, alpha=0.7)
#     ax.set_xlim(0,1)
#     ax.set_ylim(0,1)
#     fig.tight_layout()
#     plt.savefig(f"figs/model3nl.png", dpi=600)
#     return fig, ax
# def plot_model4nl(df, summary):
#     fig, axs = plt.subplots(3,4, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))
#     for n, (code, ax) in enumerate(zip(df.code.unique(), axs.flatten())):
#         d_c = df.loc[df.code==code]
#         predicted = summary.loc[f'intercepts[{n}]']["mean"] + sum([summary.loc[f'slopes[{nq}, {n}]']["mean"] * x_range**summary.loc[f'alphas[{n}]']["mean"] for nq in range(len(questions_sc))])
#         ax.plot(x_range, predicted,color='red', label='code', clip_on=False)
#         ax.set_title(f"{code}:\n"+ f"pd = {summary['mean'][f'intercepts[{n}]']:.2f} +\n"+"+ \n".join([f"{summary['mean'][f'slopes[{nq}, {n}]']:.2f} \cdot d_{q}^{summary['mean'][f'alphas[{n}]']:.2f}" for nq, (q_old, q) in enumerate(questions_short.items())]), fontsize=supersmallfs)
#         sns.scatterplot(d_c.loc[d_c.observedA!="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", style="code", legend=False, color="grey", alpha=0.5, clip_on=False)
#         # plot self-other:
#         sns.scatterplot(d_c.loc[d_c.observedA=="self"], ax=ax, x="euclideanDistance", y="perceivedDistance", hue="observedB", style="code", legend=False, palette=cmapObs, clip_on=False)
#         for i, txt in enumerate(d_c.loc[d_c.observedA=="self"]['observedB']):
#             ax.annotate(txt, (d_c.loc[d_c.observedA=="self", 'euclideanDistance'].iloc[i]+0.01, d_c.loc[d_c.observedA=="self", 'perceivedDistance'].iloc[i]+0.01), fontsize=supersmallfs, alpha=0.7)
#     for ax in axs.flatten():
#         ax.set_xlim(0,1)
#         ax.set_ylim(0,1)
#     fig.tight_layout()
#     plt.savefig(f"figs/model4nl.png", dpi=600)
#     return fig, axs

