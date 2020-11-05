import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cmap = plt.get_cmap("tab10")

# style
plt.style.use("plots.mplstyle")
fontsize = plt.rcParams["font.size"]

# settings
label_hide = ()  # ("CuCl", "AgCl")

# read data
kw = {"comment": "#"}
df_gk = pd.read_csv("results_1104.csv", **kw)
df_exp = pd.read_csv("gspread_exp_all.csv", **kw)

# merge data and pick materials w/ >= 30ps simulation time
df = df_exp.merge(df_gk, on=["space_group", "material", "n_formula"], how="left")
df = df[df.simulation_time > 25000]
# df = df.sort_values("kappa_exp")

df.to_csv("data_for_plot.csv")

# only when viewing:
# for col in ("comment", "source", "ref_exp", "sigma_std", "sigma_err"):
#     del df[col]

# compute error bars: find mean, then difference to max and min
group = df.groupby("material")
df_xerr = group.mean()
df_xerr["kappa_exp_err_max"] = group.kappa_exp.max() - df_xerr.kappa_exp
df_xerr["kappa_exp_err_min"] = -(group.kappa_exp.min() - df_xerr.kappa_exp)

# create canvas
fig, ax = plt.subplots()

# y=x agreement line
d, c = 0.15, "green"
xy = [0.1, 100]
x = np.linspace(*xy, 100)
kw = {"alpha": 0.3, "color": c, "edgecolor": "face", "linewidth": 0}
ax.plot(xy, xy, zorder=-1, c="k", lw=0.5, alpha=kw["alpha"])
ax.fill_between(x, x + x * d, x - x * d, zorder=-2, **kw)

# plot error crosses
kw = {
    "linewidth": 0,
    "mew": 0.5,
    "elinewidth": 0.5,
    "legend": None,
    "mfc": "white",
    "color": "k",
}
# x
ax.errorbar(
    x=df_xerr.kappa_exp,
    y=df_xerr.kappa,
    xerr=(df_xerr.kappa_exp_err_min, df_xerr.kappa_exp_err_max),
    **kw,
)
# y
df_xerr.plot(x="kappa_exp", y="kappa", yerr="kappa_err", ax=ax, capsize=1.2, **kw)

# annotate
alpha = 0.75
kw = {
    "arrowprops": {"arrowstyle": "-", "alpha": alpha, "linewidth": 0.5},
    "fontsize": fontsize,
    "zorder": 0,
    "textcoords": "data",
    "alpha": alpha,
}

label_offset = ("SrTiO3", "NaI", "CsCl", "CdS")
label_xy_custom = {
    "AgI": (0.12, 0.5),
    "CuI": (0.3, 2.5),
    "SnSe": (0.15, 1.1),
    "MgO": (15, 90),
    "KZnF3": (0.8, 8),
}
for ii, (l, x, y) in enumerate(zip(df_xerr.index, df_xerr.kappa_exp, df_xerr.kappa)):
    if l in label_offset:
        xm, ym, ha, va = 1.5, 0.5, "left", "top"
        xt, yt = x * xm, y * ym
    elif l in label_xy_custom:
        xt, yt, ha, va = *label_xy_custom[l], "left", "top"
    else:
        xm, ym, ha, va = 0.6, 1.75, "right", "bottom"
        xt, yt = x * xm, y * ym
    if l not in label_hide:
        ax.annotate(l, (x, y), xytext=(xt, yt), ha=ha, va=va, **kw)

# plot datapoints discerning singlecrystal and non-singlecrystal (polycryst.)
kw = {"linewidth": 0, "mew": 0.5, "mfc": "k", "color": "k"}
for (l, x, y, p) in zip(df.material, df.kappa_exp, df.kappa, df.polycrystalline):
    if l in df_xerr.index:
        if p == "y":
            ax.plot(x, y, marker="*", ms=6, **kw)
        else:
            ax.plot(x, y, marker=".", ms=7, **kw)


# appearance
# fig.set_size_inches(3.4, 3.4)
fig.set_size_inches(4, 4)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_aspect(1)

# labels
ax.set_ylabel("$\\kappa^{\\rm aiGK}$ (W/mK)")
ax.set_xlabel("$\\kappa^{\\rm exp}$ (W/mK)")

# limits
xlim = [0.1, 100]
ax.set_ylim(xlim)
ax.set_xlim(xlim)

# ticks
a0 = np.array([1, 3, 4, 5, 6, 7, 8, 9, 10])
a1 = range(-1, 2)

ticks = sorted(np.array([a0 * 10 ** a for a in a1]).flatten())
ax.set_xticks(ticks, minor=True)

ticks = sorted(np.array([10 ** a for a in a1]).flatten())
ax.set_xticks(ticks)

# plot and save
figname = "kappa_vs_exp.pdf"
fig.savefig(figname, bbox_inches="tight")
print(f".. plotted to {figname}")
