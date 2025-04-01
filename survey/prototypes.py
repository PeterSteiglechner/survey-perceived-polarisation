## prototypes.py

import matplotlib.pyplot as plt


QUESTIONS_SC =[
    "concerned about climate", 
    "adoption rights for gay couples", 
    "migration enriches culture",
    "state should reduce\nincome differences"]
questiontext = [
        'I am very concerned about climate change.', 
        'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 
        'It is enriching for cultural life in Germany when migrants come here.', 
        'The state should take measures to reduce income differences more than before.']

vals_arr = {
    "P1": [1, 1, 1, 1],
    "P2": [0.5,0.5,0.5,0.5],
    "P3": [0.2, 0.1, -0.5, 0.2],
    "P4": [0.05, -0.05, -1, -1],
}
for p, vals in vals_arr.items():

    fig, ax = plt.subplots(1,1,figsize=(16/2.54, 12/2.54))
    y = [3,2,1,0]
    ax.barh(y, vals, color=["green", "purple", "blue", "red"], height=0.5)
    ax.set_yticks([])
    ax.set_xticks([-1,0,1])
    ax.set_xticklabels(["strongly\ndisagree", "neutral", "strongly\nagree"])
    for n, qsc in enumerate(QUESTIONS_SC):
        ax.text(-1.05,y[n], qsc, rotation=0, va="center", ha="right")
    ax.spines['bottom'].set_visible(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.hlines(y, -1, [min(v, 0) for v in vals], linestyles="--", lw=0.5, colors="grey")
    ax.set_xlim(-1,1)
    ax.vlines(0,-0.5,3.5, colors="k")
    ax.text(0.8, 3.5, f"{p}", ha="center", va="bottom", fontsize=20)
    ax.set_ylim(-0.5, 3.5)
    fig.tight_layout()
    plt.savefig(f"{p}.png")

