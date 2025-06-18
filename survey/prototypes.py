## prototypes.py

import matplotlib.pyplot as plt


QUESTIONS = ["climate_concern", "gay_marriage", "rights_for_integration", "econ_inequality"]
QUESTIONTEXT = dict(zip(QUESTIONS, [
    "I am very concerned about climate change.",
    "It is good that marriages between two women or two men are allowed.",
    "Only migrants who make an effort and integrate should be given the same rights as natives.",
    "The differences in income and wealth in Germany are too high.",
]))
QUESTIONSHORTTEXT = dict(zip( QUESTIONS, [
        "concerned about climate change", 
        "support same-sex marriage",
        "migrant rights should depend on integration effort",
        "economic differences too high"
])) 
# QUESTIONS_SC =["climate_concern", 
#                    "gay_adoption", 
#                     "migration_enriches_culture",
#                    "govt_reduce_inequ",
#                    "free_elect", 
#                    "politician_salaries"]
# questionshorttext =[
#     "concerned about climate", 
#     "equal adoption rights for gay couples", 
#     "migration enriches culture",
#     "state should act to reduce income differences", 
#     "free & fair elections important", 
#     "higher politician salaries"]

# questiontext = [
#         'I am very concerned about climate change.', 
#         'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 
#         'It is enriching for cultural life in Germany when migrants come here.', 
#         'The state should take measures to reduce income differences more than before.',
#         'That national elections are free and fair is extremely important for democracy.',
#         'Politicians should receive a higher salary during their term of office.'
#         ]


import pandas as pd

from personas import personas

LIKERT5_string = [
        (1, 'Strongly agree'),
        (2, 'Agree'),
        (3, 'Neutral'),
        (4, 'Disagree'),
        (5, 'Strongly disagree'),
        (-999, "----Refuse/Don't know----"),
    ]
likert_tex2num = {tex:num for num, tex in LIKERT5_string}
likert2ones = {num: -(num-3)/2 for tex, num in likert_tex2num.items() if num!=999}

personas_tex = list(personas)
for P in personas_tex:
    for n, (qsc, q) in enumerate(QUESTIONSHORTTEXT.items()):
        P[qsc] = P["responses"][qsc] #likert2ones[likert_tex2num[P["responses"][qsc]]]
pd.DataFrame(personas_tex).drop(columns=["responses"]).to_csv("../_static/2025-06-17_personas-TEX.csv")

personas_tex

for P in personas:
    for n, (qsc, q) in enumerate(QUESTIONSHORTTEXT.items()):
        P[qsc] = likert2ones[likert_tex2num[P["responses"][qsc]]]


vals_arr = {
    f"P{n+1}": [P[q] for q in QUESTIONS] for n, P in enumerate(personas)
}


for p, vals in vals_arr.items():

    fig, ax = plt.subplots(1,1,figsize=(16/2.54, 12/2.54))
    y = [3, 2,1,0]
    bar_heights = [v + (0. if abs(v)>0 else 0.05)  for v in vals ]
    colors = ["darkgrey" if abs(v)<=0.05 else ("green" if v>0 else "red") for v in vals]
    #["green", "purple", "blue", "red", "brown", "orange"]
    ax.barh(y, bar_heights, color=colors, height=0.3, alpha=0.7)
    ax.set_yticks([])
    ax.set_xticks([])
    #ax.set_xticklabels(["strongly\ndisagree", "neutral", "strongly\nagree"])
    for n, (qsc, q) in enumerate(QUESTIONSHORTTEXT.items()):
        ax.text(-0.,y[n]+0.37, q, rotation=0, va="center", ha="center", bbox={"pad":4, "facecolor":"gainsboro", "edgecolor":"gainsboro", "alpha":0.7}, fontsize=15)
        ax.text(-1.05, y[n], "Strongly\ndisagree", va="center", ha="right", fontsize=12)
        ax.text(1.05, y[n], "Strongly\nagree", va="center", ha="left", fontsize=12)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.hlines(y, -1, [min(v, 0) for v in vals], linestyles="--", lw=0.5, colors="grey")
    ax.hlines(y, 1, [max(v, 0) for v in vals],  linestyles="--", lw=0.5, colors="grey")
    ax.set_xlim(-1,1)
    ax.vlines(0,-0.3,3.5, colors="grey")
    ax.text(-1.1, 3.5, f"{p}", ha="center", va="center", fontsize=20)
    ax.set_ylim(-0.3, 3.5)
    fig.tight_layout()
    print(f"{p}.png")
    plt.savefig(f"../_static/{p}_op.png", dpi=600)



