from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


plt.style.use("../plots.mplstyle")
fontsize = plt.rcParams["font.size"]

cmap = plt.get_cmap("tab10")
# cmap = sns.color_palette('colorblind', n_colors=20) #, as_cmap=True)

subplots_adjust_kw = {"left": 0.15, "right": 0.98, "bottom": 0.15, "top": 0.95}

df = pd.read_csv("sigma_os_md.csv")

df.rename(
    columns={"Space_Group": "spacegroup", "sigma_md": "md", "sigma_os": "os"},
    inplace=True,
)

df_zb = df[df.spacegroup == 216]
df_rs = df[df.spacegroup == 225]
df_wz = df[df.spacegroup == 186]
df_pe = df[df.spacegroup == 62]

# canvas
xmin = 0.07
fig, ax = plt.subplots()
fig.set_size_inches(4.1, 2.73)
fig.subplots_adjust(**subplots_adjust_kw)


xy = {"x": "md", "y": "os"}
kw = {"ax": ax, "edgecolors": None, "alpha": 0.8}

df_zb.plot.scatter(**xy, s=20, marker="D", color=cmap(1), **kw)
df_rs.plot.scatter(**xy, s=30, marker="s", color=cmap(3), **kw)
df_wz.plot.scatter(**xy, s=40, marker="H", color=cmap(0), **kw)
df_pe.plot.scatter(**xy, s=35, marker="X", color=cmap(6), **kw)


# separate axes
tax = ax.twinx()
for x in (ax, tax):
    x.set_xscale("log"), x.set_yscale("log")
    x.set_aspect(1)
    x.set_xlim([xmin, 3]), x.set_ylim([xmin, 1])
tax.set_xticks([]), tax.set_yticks([])
tax.set_xticks([], minor=True), tax.set_yticks([], minor=True)
tax.set_xticklabels([]), tax.set_yticklabels([])

xticks = [0.1, 0.2, 0.3, 0.5, 1, 2, 3]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)

yticks = xticks[:-2]
ax.set_yticks(yticks)
ax.set_yticklabels(yticks)

# minor ticks
ticks = [0.4, 0.6, 0.7, 0.8, 0.9]
ax.set_xticks(ticks, minor=True)
ax.set_yticks(ticks, minor=True)
# ax.set_xticklabels([], minor=True)
# ax.set_yticklabels([], minor=True)

# labels
ax.set_xlabel(r"$\sigma^{\rm A}_{\rm MD}$")
ax.set_ylabel(r"$\sigma^{\rm A}_{\rm OS}$", rotation=0, labelpad=15)


# ideal line
tax.plot([xmin, 10], [xmin, 10], color="k", zorder=-1, lw=0.5, label=None)
# worst difference
diff = (df.md - df.os) / df.md

dy = 1.1

tax.fill_between(
    [xmin, 10],
    [xmin * 0.9, 10 * 0.9],
    [xmin * 1.1, 10 * 1.1],
    color="green",
    alpha=0.2,
    lw=0,
    zorder=-3,
)

# annotate
df_ext = df[df.md > 1]
for (l, x, y) in zip(df_ext.Material, df_ext.md, df_ext.os):
    ax.annotate(
        l,
        (x, y),
        xytext=(3, 3),
        ha="right",
        va="bottom",
        textcoords="offset points",
        # arrowprops={"arrowstyle": "-", "linewidth": 0.5},
    )

kw = {"framealpha": 0}
ax.legend(["ZB", "RS", "WZ", "PS"], loc="upper left", **kw)
tax.legend(["ideal", r"$\pm 10\,\%$"], loc="lower right", **kw)

fig.savefig("sigma_os_md.pdf")
