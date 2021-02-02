"""plot
    https://material.io/resources/color/#!/?view.left=0&view.right=0&primary.color=424242
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer

label_alpha = ("NaCl", "MgO")
label_xy_custom = {
    # "AgI": (0.12, 0.4),
    # "CuI": (0.3, 2.5),
    "MgO": (15, 85),
    # "KZnF3": (0.8, 8),
    "KMgF3": (1.8, 23),
    # "NaCl": (2, 12),
    "SnSe": (0.2, 1.3),
    "CuCl": (0.2, 0.9),
    "CsCl": (0.2, 0.6),
    "CsBr": (0.4, 0.175),
    "CsI": (1.5, 0.175),
    "NaI": (3, 0.65),
    "KCl": (10, 1),
    "BaSi2": (3, 0.3),
    "CdS": (20, 0.4),
    "CdSe": (8, 0.4),
    "ZnO": (22, 8),
    "KCl": (20, 1.0),
    "KF": (20, 1.5),
    "SrTiO3": (16, 3),
    # "KF": (1.4, 5.5),
}

labels_latex = {
    "SrTiO3": "SrTiO$_3$",
    "KZnF3": "KZnF$_3$",
    "BaSi2": "BaSi$_2$",
    "KMgF3": "KMgF$_3$",
}

black = "#1b1b1b"
grey = "#6d6d6d"


def main(
    cmap: str = "tab10",
    results_file: str = "results_1130.csv",
    exclude: bool = False,
    hide: bool = True,
    annotate: bool = True,
    fill: bool = False,
):
    """plot kappa vs. kappa"""
    cmap = plt.get_cmap(cmap)

    # style
    plt.style.use("plots.mplstyle")
    fontsize = plt.rcParams["font.size"]

    # read data
    kw = {"comment": "#"}
    df_gk = pd.read_csv(results_file, **kw)
    df_exp = pd.read_csv("gspread_exp_all.csv", **kw)

    # merge data and pick materials w/ >= 30ps simulation time
    df = df_exp.merge(df_gk, on=["space_group", "material", "n_formula"], how="left")
    df = df[df.simulation_time >= 28000]
    # df = df.sort_values("kappa_exp")

    # hide and exclude
    hides = [s for s in open("hide.dat").read().split() if "#" not in s]
    excludes = [s for s in open("exclude.dat").read().split() if "#" not in s]
    if exclude:  # exclude data points
        hides += excludes

    if hide:
        mask = [m not in hides for m in df.material.astype(str)]
        df = df[mask]

    df.to_csv("data_for_plot.csv")

    # compute error bars: find mean, then difference to max and min
    group = df.groupby("material")
    df_xerr = group.mean()
    df_xerr["kappa_exp_err_max"] = group.kappa_exp.max() - df_xerr.kappa_exp
    df_xerr["kappa_exp_err_min"] = -(group.kappa_exp.min() - df_xerr.kappa_exp)

    # create canvas
    fig, ax = plt.subplots()

    # y=x agreement line
    d, c = 1.15, "green"
    xy = [0.1, 100]
    x = np.linspace(*xy, 100)
    kw = {"alpha": 0.2, "color": c, "edgecolor": "face", "linewidth": 0}
    ax.plot(xy, xy, zorder=-1, c="k", lw=0.5, alpha=kw["alpha"])
    if fill:
        ax.fill_between(x, x * d, x / d, zorder=-2, **kw)

    # plot error crosses
    kw = {
        "linewidth": 0,
        "mew": 0.75,
        "elinewidth": 0.6,
        "legend": None,
        "mfc": "white",
        "color": black,
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

    # plot datapoints discerning singlecrystal and non-singlecrystal (polycryst.)
    kw = {"linewidth": 0, "mew": 0.25, "mfc": black, "color": black, "ms": 7}
    iter = zip(df.material, df.kappa_exp, df.kappa, df.polycrystalline)
    for (l, x, y, p) in iter:
        if l in df_xerr.index:
            if l in excludes:
                kw["mfc"], kw["color"] = 2 * ("red",)
            else:
                kw["mfc"], kw["color"] = 2 * (black,)

            if p == "n":
                ax.plot(x, y, marker=".", **kw)
            # elif p == "t":
            #     ax.plot(x, y, marker="|", **{**kw, "mew": 1})
            else:
                ax.plot(x, y, marker="*", **kw)
    if annotate:
        alpha = 0.6
        kw = {
            "arrowprops": {"arrowstyle": "-", "alpha": alpha, "linewidth": 0.5},
            "fontsize": fontsize,
            "zorder": 0,
            "textcoords": "data",
            "color": grey,
        }

        for (l, x, y) in zip(df_xerr.index, df_xerr.kappa_exp, df_xerr.kappa):
            if l in label_xy_custom:
                xt, yt, ha, va = *label_xy_custom[l], "left", "top"
            else:
                xm, ym, ha, va = 0.6, 1.75, "right", "bottom"
                xt, yt = x * xm, y * ym
            label_latex = labels_latex.get(l, l)
            ax.annotate(label_latex, (x, y), xytext=(xt, yt), ha=ha, va=va, **kw)

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
    figname = Path("kappa_vs_exp.pdf")
    if exclude:
        figname = Path("kappa_vs_exp_exclude.pdf")
    fig.savefig(figname, bbox_inches="tight")
    fig.savefig(figname.stem + ".png", bbox_inches="tight", dpi=600)
    print(f".. plotted to {figname}")


if __name__ == "__main__":
    typer.run(main)
