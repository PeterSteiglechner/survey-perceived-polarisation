

## 
# my in-group is very pro-env and pro-gay
# i perceive distances in these topics as larger
# if someone has a distance on x-axis --> expect large distance on y-axis.

colors = ["green", "purple", "blue", "red"]
#jitter = lambda liste: np.array(liste)+np.random.random()*0.0 - 0.0
fig, axs = plt.subplots(1,2)
xs = jitter(op_distances)
axs[0].scatter(xs, perceived_distances, label="overall", color="k")
for f,xpos,ypos in zip(friends, xs, perceived_distances):
    axs[0].text(xpos, ypos, f, fontsize=12, color="k")

for nq, q in enumerate(questions_sc):
    col = colors[nq]
    ys = jitter(rel_op_distances_qu[nq])
    axs[1].scatter(perceived_distances, ys, marker="x", alpha=0.8, label=q, color=col)
    for f,ypos, xpos in zip(friends, ys, perceived_distances):
        phi = np.random.randint(360)
        axs[1].text(xpos,ypos,f+"_"+q[:3], fontsize=7, ha="right" if phi<90 or phi>270 else "left", va="bottom" if phi<180 else "top",  rotation=phi*np.pi/180, color=col)
if code==data.index[0]:
    axs[0].legend(ncol=1, fontsize=7)
axs[0].set_xlabel(f"distance in opinions ({func})")
axs[0].set_ylabel("perceived political distance")
axs[1].set_xlabel(f"perceived distance")
axs[1].set_ylabel(f"relative opinion distance for each question ({func})")
plt.show()