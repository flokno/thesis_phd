"""inspired by https://www.bastibl.net/publication-quality-plots/"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import typer
import xarray as xr

from utils import get_kde, get_xy

plt.style.use("../paper.mplstyle")
fontsize = plt.rcParams["font.size"]


plt.rc(
    "text.latex",
    preamble=r"\PassOptionsToPackage{full}{textcomp}\usepackage{newtxtext,newtxmath}",
)

# colors
c1 = "#5759aa"
c2 = "#9c4c36"
# darker:
c1k = "#3F417C"
c2k = "#803E2C"

cmap1 = "PuBu"
cmap2 = "OrRd"


subplots_adjust_kw = {
    "left": 0.1,
    "right": 0.98,
    "bottom": 0.1,
    "top": 0.98,
    "wspace": 0.2,
}


def plot_kde(
    ds,
    ax,
    fig,
    harmonic=False,
    cmap="PuBu",
    color="k",
    npoints=3j,
    levels=64,
    xlim=1,
    ylim=1,
    contour=True,
):
    """plot kde to ax"""
    try:
        name = ds.attrs["System Name"]
    except KeyError:
        name = ds.attrs["system_name"]
    X, Y, std = get_xy(ds, harmonic=harmonic)

    if contour:
        xx, yy, f = get_kde(X, Y, npoints=npoints, xlim=xlim, ylim=ylim)

        cnt = ax.contourf(xx, yy, f, cmap=cmap, levels=levels)

        for c in cnt.collections:
            c.set_edgecolor("face")

    if not harmonic:
        kw = {"color": "k", "lw": 1, "alpha": 0.8, "ls": (0, (5, 1))}
        ax.axhline(Y.std(), **kw)
        ax.axhline(-Y.std(), **kw)

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)

    dmajor, dminor = 1, 0.2
    if xlim > 1:
        dminor = 0.5

    major_ticks = {"ticks": np.arange(-xlim, 1.1 * xlim, dmajor)}
    ax.set_xticks(**major_ticks)
    ax.set_yticks(**major_ticks)

    minor_ticks = {"ticks": np.arange(-xlim, xlim, dminor), "minor": True}
    ax.set_xticks(**minor_ticks)
    ax.set_yticks(**minor_ticks)

    ax.set_aspect(1)

    typer.echo(f"System: {name}\n")
    typer.echo(f"F.std = {std}\n")
    typer.echo(f"X.std = {X.std()}\n")
    typer.echo(f"Y.std = {Y.std()}\n\n")

    ax.tick_params(direction="in", which="both", right=True, top=True)
    ax.tick_params(which="both", width=0.75)

    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)

    # cbar = fig.colorbar(cnt, cax=cax, orientation="vertical")
    # cbar.set_ticks([])
    cbar = None

    # plot data points
    n = 2000
    idx = np.round(np.linspace(0, len(X) - 1, n)).astype(int)
    ax.scatter(X[idx], Y[idx], s=1, marker=".", alpha=0.35, color=color)

    return cbar


def get_fig(harmonic=False, npoints=3, lim=1):
    plt.style.use("../paper.mplstyle")

    # adjust height

    ds1 = xr.load_dataset("../datasets/Si.nc")
    ds2 = xr.load_dataset("../datasets/KCaF3.nc")
    # ds2 = xr.load_dataset("datasets/CuI.nc")

    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
    fig.subplots_adjust(**subplots_adjust_kw)
    fig.set_size_inches(4.1, 2.5)

    kw = {"harmonic": harmonic, "npoints": npoints * 1j, "xlim": lim, "ylim": lim}
    cbar = plot_kde(ds1, ax1, fig, cmap=cmap1, color=c1k, **kw)
    cbar = plot_kde(ds2, ax2, fig, cmap=cmap2, color=c2k, **kw)

    xlabel = r"$ F / \sigma[F]$"
    for ax in (ax1, ax2):
        ax.set_xlabel(xlabel)
    # ax1.set_xlabel(r"$F / \sigma_\mathrm{Si}[F]$")
    # ax2.set_xlabel(r"$F / \sigma_\mathrm{KCaF}[F]$")

    # cbar label
    # ylabel = r"$p \left( \tilde{F}_{I, \alpha}^\mathrm{A} \right)$"
    # ylabel = r"$\tilde{F}_{I, \alpha}^\mathrm{A}$"
    # ylabel = r"$F_{I, \alpha}^\mathrm{A}$ $/$ $\sigma [F]$"
    # cbar.set_label("Probability density", rotation=-90, labelpad=15)

    if harmonic:
        ylabel = r"$F^\mathrm{Ha}  / \sigma[F]$"
    else:
        ylabel = r"$F^\mathrm{A}  / \sigma[F]$"

    kw = {
        "ha": "center",
        "va": "center",
        "transform": fig.transFigure,
        "fontsize": fontsize,
    }
    # plt.text(0.53, 0.53, ylabel, **kw)
    ax1.set_ylabel(ylabel, rotation=90, labelpad=0)

    # Label the System names
    x, y = 0.1, 0.9
    ha = "left"
    va = "center"
    fs = fontsize + 1
    name1 = "Si"
    name2 = r"KCaF$_3$"
    # name2 = r"CuI"

    kw = {"fontsize": fs, "ha": ha, "va": va, "color": "k"}

    ax1.text(-0.85 * lim, 0.75 * lim, name1, **kw)
    ax2.text(-0.85 * lim, 0.75 * lim, name2, **kw)
    # ax1.set_title(name1, fontsize=fs)
    # ax2.set_title(name2, fontsize=fs)

    return fig


def main(harmonic: bool = False, dpi: int = 450, npoints: int = 35, lim: int = 2):
    fig = get_fig(harmonic=harmonic, npoints=npoints, lim=lim)

    if harmonic:
        outfile = "histogram_harmonic.png"
    else:
        outfile = "histogram.png"

    kw = {"bbox_inches": "tight"}
    fig.savefig(Path(outfile).stem + ".pdf", **kw)
    fig.savefig(outfile, dpi=dpi, **kw)


if __name__ == "__main__":
    typer.run(main)
