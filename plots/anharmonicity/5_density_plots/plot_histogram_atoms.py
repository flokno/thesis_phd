"""inspired by https://www.bastibl.net/publication-quality-plots/"""
import matplotlib.pyplot as plt
import typer
import numpy as np
import pandas as pd
import xarray as xr

from utils import get_kde
from vibes.helpers.converters import json2atoms

plt.style.use("../paper.mplstyle")
fontsize = plt.rcParams["font.size"]


plt.rc(
    "text.latex",
    preamble=r"\PassOptionsToPackage{full}{textcomp}\usepackage{newtxtext,newtxmath}",
)

subplots_adjust_kw = {
    "left": 0.1,
    "right": 0.98,
    "bottom": 0.1,
    "top": 0.98,
    "wspace": 0.2,
}

npoints = 35j
xlim, ylim = 2, 2

# darker
c2 = "#803E2C"
# cmap1 = "PuBu"
cmap2 = "OrRd"

ds = xr.load_dataset("../datasets/KCaF3.nc")

try:
    supercell = json2atoms(ds.attrs["reference atoms"])
except KeyError:
    supercell = json2atoms(ds.attrs["atoms_supercell"])
symbols = np.array(supercell.get_chemical_symbols())
unique_symbols = np.unique(symbols)


dct = {}
for sym in unique_symbols:
    mask = symbols == sym

    f = ds.forces.data[:, mask]
    fh = ds.forces_harmonic.data[:, mask]

    # std = ds.forces.data.std()
    std = f.std()

    x = f / std
    y = (f - fh) / std

    dct[sym] = {"x": x.flatten(), "y": y.flatten(), "norm": std, "sym": f"{sym}"}

    print(f"sym = {sym}\n")
    print(f"x.std() = {x.std()}\n")
    print(f"y.std() = {y.std()}\n\n")


fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True)
fig.subplots_adjust(**subplots_adjust_kw)
fig.set_size_inches(4.1, 2)


def plot_kde(d, ax, cmap="OrRd", npoints=npoints, levels=64, xlim=xlim, ylim=ylim):
    """plot kde to ax"""
    x, y = d["x"], d["y"]
    std = d["norm"]  # * x.std()

    X, Y = pd.Series(x), pd.Series(y)

    xx, yy, f = get_kde(X, Y, npoints=npoints, xlim=xlim, ylim=ylim)

    cnt = ax.contourf(xx, yy, f, cmap=cmap, levels=levels)

    for c in cnt.collections:
        c.set_edgecolor("face")

    kw = {"ls": (0, (2, 3)), "color": "k"}
    ax.axhline(Y.std(), **kw)
    ax.axhline(-Y.std(), **kw)

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)

    # ticks
    ticks = np.arange(-xlim, 1.1 * xlim, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    ticks_minor = np.arange(-xlim, xlim, 0.5)
    ax.set_xticks(ticks_minor, minor=True)
    ax.set_yticks(ticks_minor, minor=True)

    ax.set_aspect(1)
    print(Y.std())

    ax.tick_params(direction="in", which="both", right=True, top=True, width=0.75)

    # plot data points
    n = 1000
    idx = np.round(np.linspace(0, len(X) - 1, n)).astype(int)
    ax.scatter(X[idx], Y[idx], s=1, marker=".", alpha=0.35, color=c2)

    return cnt


plot_kde(dct["K"], ax1, cmap=cmap2)
plot_kde(dct["Ca"], ax2, cmap=cmap2)
cnt = plot_kde(dct["F"], ax3, cmap=cmap2)

xlabel = r"$p \left( \tilde{F}_{\alpha} \right)$"
xlabel = r"$ {F}_{\alpha} \right)$"

ax1.set_xlabel(r"$F_\mathrm{K} / \sigma[F_\mathrm{K}]$")
ax2.set_xlabel(r"$F_\mathrm{Ca} / \sigma[F_\mathrm{Ca}]$")
ax3.set_xlabel(r"$F_\mathrm{F} / \sigma[F_\mathrm{F}]$")

ylabel = r"$p \left( \tilde{F}_{\alpha}^\mathrm{A} \right)$"
ylabel = r"$F_I^\mathrm{A}  / \sigma[F_I]$"
ax1.set_ylabel(ylabel, labelpad=-4, y=0.6)

# Label the System names
x, y = 0.1, 0.9
ha = "left"
va = "center"
fs = fontsize + 1
name1 = "Si"
name2 = r"KCaF$_3$"

kw = {"fontsize": fs, "ha": ha, "va": va, "color": "k"}
ax1.text(-0.85 * xlim, 0.75 * ylim, "K", **kw)
ax2.text(-0.85 * xlim, 0.75 * ylim, "Ca", **kw)
ax3.text(-0.85 * xlim, 0.75 * ylim, "F", **kw)

# colorbar
# cb_ax = fig.add_axes([0.93, 0.1, 0.02, 0.5])
# cbar = fig.colorbar(cnt, cax=cb_ax)
# cbar = fig.colorbar(cnt, ax=[ax1, ax2, ax3], shrink=0.65, pad=0.02)
# divider = make_axes_locatable(ax3)
# cax = divider.append_axes("right", size="5%", pad=0.05)
#
# cbar = fig.colorbar(cnt, cax=cax, orientation="vertical")
# cbar.set_label("Probability density", rotation=-90, labelpad=15)
# cbar.set_ticks([])


kw = {"bbox_inches": "tight"}
fig.savefig("histogram_atoms.pdf", **kw)
fig.savefig("histogram_atoms.png", dpi=450, **kw)
