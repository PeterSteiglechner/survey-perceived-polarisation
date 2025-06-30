## prototypes.py

import matplotlib.pyplot as plt

for lan in ["de", "en"]:
    QUESTIONS_OG = ["climate_concern", "gay_marriage", "rights_indep_integration", "econ_inequality"]
    for QUESTIONS_INDS in [[0,1,2,3], [1,3,0,2], [2,0,3,1], [3,2,1,0]]: # np.random.choice(range(len(QUESTIONS_OG)), size=len(QUESTIONS_OG), replace=False) 

        QUESTIONTEXT = {
            "en":
            dict(zip(QUESTIONS_OG, [
            "I am very concerned about climate change.",
            "It is good that marriages between two women or two men are allowed.",
            "Migrants should be given the same rights as natives, regardless of whether they make an effort and integrate.", # Only migrants who make an effort and integrate should be given the same rights as natives.
            "The differences in income and in wealth in Germany are too high.",
        ])), "de":
            dict(zip(QUESTIONS_OG, [
            "Ich bin sehr besorgt über den Klimawandel.",
            "Es ist gut, dass Ehen zwischen zwei Frauen bzw. zwischen zwei Männern erlaubt sind.",
            "Migranten und Migrantinnen sollten unabhängig davon, ob sie sich anstrengen und integrieren,  die gleichen Rechte bekommen wie Einheimische.", #"Nur Migranten, die sich anstrengen und integrieren, sollten die gleichen Rechte bekommen wie Einheimische.",
            "Die Einkommens- und Vermögensunterschiede in Deutschland sind zu groß.",
        ]))
        }
        QUESTIONSHORTTEXT =  {
            "en":
            dict(zip( QUESTIONS_OG, [
                "extreme concern about climate change", 
                "support same-sex marriage",
                "equal rights for migrants regardless of integration",  #"equal rights only for migrants who integrate",
                "income and wealth differences too high"
        ])), 
            "de":
                    dict(zip( QUESTIONS_OG, [
                "Extreme Besorgnis über Klimawandel", 
                "Unterstützung für gleichgeschlechtliche Ehe",
                "Gleiche Rechte für Migranten/-innen\nunabhängig von Integration",
                "Einkommens- und Vermögens-\nunterschiede zu groß"
        ])),
        }

        QUESTIONS = [QUESTIONS_OG[n] for n in QUESTIONS_INDS]

        import pandas as pd
        import sys
        import numpy as np
        sys.path.append("survey/")
        from personas import personas
        likert2ones = {"Strongly agree": 1, "Agree":0.5, "Neutral":0., "Disagree":-0.5, "Strongly disagree":-1, "NA": np.nan}

        personas_tex = list(personas)
        for P in personas_tex:
            for n, qsc in enumerate(QUESTIONS_OG):
                # q = QUESTIONSHORTTEXT[lan][qsc]
                P[qsc] = P["responses"][qsc] #likert2ones[likert_tex2num[P["responses"][qsc]]]
        pd.DataFrame(personas_tex).drop(columns=["responses"]).to_csv("../_static/personas.csv")

        # personas_tex

        for P in personas:
            for n, qsc in enumerate(QUESTIONS_OG):
                # q = QUESTIONSHORTTEXT[lan][qsc]
                P[qsc] = likert2ones[P["responses"][qsc]]


        vals_arr = {
            f"P{n+1}": {q: P[q] for q in QUESTIONS if not np.isnan(P[q])} for n, P in enumerate(personas)
        }
        import matplotlib as mpl 
        rgba = lambda r,g,b,a: mpl.colors.rgb2hex((r/255, g/255, b/255, a), keep_alpha=True) 
        alp = 0.8
        cols = {
            -1: rgba(230,97,1, alp),
            -0.5:  rgba(253,184,99, alp),
            0: rgba(165,165,165, alp), 
            0.5:  rgba(178,171,210, alp),
            1: rgba(94,60,153, alp)
            }
        for p, vals in vals_arr.items():

            y = - np.arange(len(vals.keys()))
            fig, ax = plt.subplots(1,1,figsize=(18/2.54, (2+13/4*len(y))/2.54))
            bar_heights = [vals[q] + (0. if abs(vals[q])>0 else 0.05)  for q in vals.keys() ]
            colors = [cols[v] for v in vals.values()]
            ax.barh(y, bar_heights, color=colors, height=0.3, alpha=0.7)
            ax.set_yticks([])
            ax.set_xticks([])
            #ax.set_xticklabels(["strongly\ndisagree", "neutral", "strongly\nagree"])
            for n, qsc in enumerate(vals.keys()):
                q = QUESTIONSHORTTEXT[lan][qsc]
                if qsc in vals.keys():
                    ax.text(-0.,y[n]+0.25, q, rotation=0, va="bottom", ha="center", bbox={"pad":4, "facecolor":"gainsboro", "edgecolor":"gainsboro", "alpha":0.7}, fontsize=15)
                    ax.text(-1.05, y[n], "Strongly\ndisagree" if lan=="en" else "Stimme\nüberhaupt\nnicht zu", va="center", ha="right", fontsize=12)
                    ax.text(1.05, y[n], "Strongly\nagree" if lan=="en" else "Stimme voll\nund ganz zu", va="center", ha="left", fontsize=12)
                    yc+=1
            ax.spines['bottom'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.hlines(y, -1, [min(v, 0) for v in vals.values()], linestyles="--", lw=0.5, colors="grey")
            ax.hlines(y, 1, [max(v, 0) for v in vals.values()],  linestyles="--", lw=0.5, colors="grey")
            ax.set_xlim(-1,1)
            ax.vlines(0,y[-1]-0.3, y[0]+.5, colors="grey")
            ax.text(-0.2, 1.+0.2/len(y), f"{p}", ha="left", va="top", fontsize=20, transform=ax.transAxes)
            ax.set_ylim(y[-1]-0.3, y[0]+.5)
            fig.tight_layout()
            fname = f"../_static/{p}_op_{lan}_sort{''.join([f"{n}" for n in QUESTIONS_INDS])}.png"
            print(fname)
            plt.savefig(fname, dpi=600)
            plt.close()




        #################################
        #####  defined them   #####
        #################################
