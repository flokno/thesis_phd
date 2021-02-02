import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats as st

plt.style.use("../../plots.mplstyle")
fontsize = plt.rcParams["font.size"]

cmap = plt.get_cmap("tab10")

subplots_adjust_kw = {"left": 0.15, "right": 0.98, "bottom": 0.1, "top": 0.98}

df = pd.read_csv("kappa_sigma.csv").dropna()

df.rename(
    columns={
        "Space_Group": "spacegroup",
        "kappa_L": "kappa",
        "sigma_a_no_nmh": "sigma",
        "Material": "material",
    },
    inplace=True,
)

df_zb = df[df.spacegroup == 216]
df_rs = df[df.spacegroup == 225]
df_wz = df[df.spacegroup == 186]

# canvas
xmin = 0.07
fig, ax = plt.subplots()
fig.set_size_inches(4.1, 4.1)
fig.subplots_adjust(**subplots_adjust_kw)


xy = {"x": "sigma", "y": "kappa"}
kw = {"ax": ax, "edgecolors": None, "alpha": 0.8}

df_zb.plot.scatter(**xy, s=20, marker="D", color=cmap(1), **kw)
df_rs.plot.scatter(**xy, s=30, marker="s", color=cmap(3), **kw)
df_wz.plot.scatter(**xy, s=40, marker="H", color=cmap(0), **kw)


# separate axes
tax = ax.twinx()
ax.set_zorder(tax.get_zorder() + 1)
ax.patch.set_visible(False)

for x in (ax, tax):
    x.set_xscale("log"), x.set_yscale("log")
    x.set_xlim([0.08, 0.5]), x.set_ylim([1, 4e3])
    x.set_aspect(1 / x.get_data_ratio())

xticks = [0.1, 0.2, 0.3, 0.4, 0.5]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)

# # minor ticks
ticks = np.arange(0.1, 0.5, 0.05)
ax.set_xticks(ticks, minor=True)
ax.set_xticklabels([], minor=True)

# remove yticks from tax
tax.set_yticks([])
tax.set_yticks([], minor=True)

# labels
ax.set_xlabel(r"$\sigma^{\rm A}$")
ax.set_ylabel(
    r"$\kappa^{\rm exp}_{\rm 300\,K} ({\rm W/mK})$"
)  # , rotation=0, labelpad=15)


X, Y = df.sigma, df.kappa
# fit logarithm
slope, intercept, r_value, p_value, std_err = st.linregress(np.log(X), np.log(Y))

print("Linregress:")
print(f".. slope:     {slope}")
print(f".. intercept: {intercept}")
print(f".. r_value:   {r_value}")
print(f".. p_value:   {p_value}")
print(f".. std_err:   {std_err}")


# exponentiate back
x = np.linspace(0.05, 0.5, 3)
y = np.exp(intercept + slope * np.log(x))

y_0 = np.exp(intercept)
pow = x ** slope
y = y_0 * pow

tax.plot(x, y, color="k", lw=0.75, zorder=-5, ls="--", alpha=0.5)

diff = 5
tax.fill_between(
    x, y / diff, y * diff, color="black", alpha=0.05, lw=0, zorder=-3,
)

# annotate some materials
kw_lb = dict(xytext=(-3, -3), ha="right", va="top")
kw_rt = dict(xytext=(0, 3), ha="left", va="bottom")
annot_dict = {
    "C": kw_rt,
    "BN": kw_rt,
    "BeO": kw_rt,
    "Si": kw_lb,
    "BP": kw_lb,
    "InP": kw_rt,
    "MgO": kw_lb,
    "ZnO": kw_rt,
    "SrO": kw_lb,
    "PbSe": kw_lb,
    "NaI": kw_lb,
}
for (l, x, y) in zip(df.material, df.sigma, df.kappa):
    if l in annot_dict:
        kw = annot_dict[l]
        ax.annotate(l, (x, y), textcoords="offset points", **kw)
    else:
        ...
        # ax.annotate(l, (x, y), textcoords="offset points", alpha=.5, **kw_lb)


kw = {"framealpha": 0}
ax.legend(["ZB", "RS", "WZ"], loc="upper right", **kw)
s1 = f"{y_0:.2f}"
s2 = f"{slope:.2f}"
print(s1, s2, r_value, r_value ** 2)
# fit_str = "$y = 0.02 \\cdot x^{-4.79}$"
# fit_str = f"\nPower: {slope:.2f}\nPearson correlation: {abs(r_value):.2f}"
# fit_str = "$\\log \\kappa \\propto " + num_str + "\\cdot \\sigma^{\\rm A}$"

num_str = f"{slope:.1f}"
fit_str = "$\\log \\kappa \\propto " + num_str + "\\cdot \\sigma^{\\rm A}$"
fit_str += f"\nPearson $\\rho$: {abs(r_value):.2f}"

tax.legend([fit_str, "within order of magnitude"], loc="lower left", **kw)

fig.savefig("sigma_vs_kappa.pdf")
fig.savefig("sigma_vs_kappa.png", bbox_inches="tight", dpi=600)
