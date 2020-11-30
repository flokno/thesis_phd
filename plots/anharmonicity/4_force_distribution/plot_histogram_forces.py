"""inspired by https://www.bastibl.net/publication-quality-plots/"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

# from matplotlib import font_manager
from scipy import stats

plt.style.use("../paper.mplstyle")
fontsize = plt.rcParams["font.size"]


# params = {"text.latex.preamble": [r"\usepackage{amsmath}"]}
# plt.rcParams.update(params)
plt.rc(
    "text.latex",
    preamble=r"\PassOptionsToPackage{full}{textcomp}\usepackage{newtxtext,newtxmath}",
)
subplots_adjust_kw = {"bottom": 0.2, "left": 0.1, "right": 0.99, "wspace": 0.3}

# colors
c1 = "#5759aa"
c2 = "#9c4c36"
# darker:
c1k = "#3F417C"
c2k = "#803E2C"

ds1 = xr.load_dataset("../datasets/Si.nc")
ds2 = xr.load_dataset("../datasets/KCaF3.nc")

# canvas
fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(ncols=2, nrows=2, sharex="col")
fig.subplots_adjust(**subplots_adjust_kw)
fig.set_size_inches(4.1, 3)


def get_x(ds, std=False):
    """return f pd.Series"""
    f = ds.forces.data

    x = f.flatten()

    if std:
        return pd.Series(x / x.std())
    else:
        return pd.Series(x)


# KDE estimation
def get_kde(X, npoints=100, xlim=2):
    """get kde, return x, f"""
    xx = np.linspace(-xlim, xlim, npoints)

    f = stats.gaussian_kde(X)

    return xx, f


def plot_kde(ds, ax, c=c1, npoints=1, levels=64, xlim=1, ylim=1, std=False):
    """plot kde to ax"""
    try:
        name = ds.attrs["System Name"]
    except KeyError:
        name = ds.attrs["system_name"]
    print(name)
    X = get_x(ds, std=std)
    xx, f = get_kde(X, npoints=npoints, xlim=xlim)

    ax.plot(xx, f(xx), color="k", alpha=0.5, lw=1.5)
    ax.fill(xx, f(xx), color=c, alpha=1.0)

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(0, ylim)

    xlim -= 0.5
    ax.set_xticks(np.arange(-xlim, 1.1 * xlim, 1))
    ax.set_xticks(np.arange(-xlim, xlim, 0.5), minor=True)

    ax.set_yticks([0.5], minor=True)

    kw = {"color": "k", "lw": 1, "ls": (0, (5, 7))}
    ax.axvline(X.std(), **kw)
    ax.axvline(-X.std(), **kw)

    kw = {"which": "both", "width": 0.75, "zorder": 10}
    ax.tick_params(axis="x", direction="out", **kw)
    ax.tick_params(axis="y", direction="in", **kw)


def label_axes(ax1, ax2, ax3, ax4, name1="Si", name2=r"KCaF$_3$", pad=2.5):
    # labels
    xlabel1 = r"$F$ (eV/$\mathrm{\AA}$)"
    xlabel2 = r"$F / \sigma [F]$ ~(1)"
    ax2.set_xlabel(xlabel1)
    ax4.set_xlabel(xlabel2)

    ylabel1 = r"$p \left( F \right)$"
    ax1.set_ylabel(ylabel1, rotation=90, labelpad=pad)
    ax2.set_ylabel(ylabel1, rotation=90, labelpad=pad)

    # right labels
    ylabel2 = r"$p \left(F / \sigma [F] \right)$"
    ax3.set_ylabel(ylabel2, rotation=90, labelpad=pad)
    ax4.set_ylabel(ylabel2, rotation=90, labelpad=pad)

    # System names
    x, y = 0.98, 0.91
    ha = "right"
    va = "top"
    fs = fontsize + 2

    # fprop = font_manager.FontProperties(family="serif")

    kw = {"ha": ha, "va": va, "fontsize": fs, "color": "k"}
    plt.text(x, y, name1, transform=ax1.transAxes, **kw)
    plt.text(x, y, name2, transform=ax2.transAxes, **kw)

    # figure labels
    x = 0.16
    kw["color"] = "k"
    plt.text(x, y, "a)", transform=ax1.transAxes, **kw)
    plt.text(x, y, "b)", transform=ax2.transAxes, **kw)

    x = 0.97
    plt.text(x, y, "c)", transform=ax3.transAxes, **kw)
    plt.text(x, y, "d)", transform=ax4.transAxes, **kw)


# plot
kw = {"xlim": 2.5, "ylim": 1.35, "npoints": 100}
plot_kde(ds1, ax1, c=c1, **kw)
plot_kde(ds2, ax2, c=c2, **kw)

kw["std"] = True
plot_kde(ds1, ax3, c=c1, **kw)
plot_kde(ds2, ax4, c=c2, **kw)

label_axes(ax1, ax2, ax3, ax4)


fig.savefig("histogram_forces.pdf", transparent=True, bbox_inches="tight")
