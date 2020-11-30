from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as st
import typer

plt.style.use("plots.mplstyle")


# annotate materials
kw_lb = dict(xytext=(-2, -3), ha="right", va="top")
kw_rb = dict(xytext=(2, -3), ha="left", va="top")
kw_rt = dict(xytext=(0, 3), ha="left", va="bottom")
annot_dict = {
    "MgTe": kw_lb,
    # "Mg3Sb2": kw_lb,
    "MgO": kw_rt,
    "NaF": kw_rt,
    "NaCl": kw_rt,
    # "NaBr": kw_rt,
    "KCl": kw_rt,
    "NaI": kw_rt,
    "CsBr": kw_lb,
    "CsI": kw_lb,
    "SnSe": kw_rb,
    "CsCl": kw_rt,
}

labels_latex = {"SrTiO3": "SrTiO$_3$", "KZnF3": "KZnF$_3$", "BaSi2": "BaSi$_2$"}


def main(
    cmap: str = "tab10", results_file: str = "results_1130.csv", exclude: bool = True,
):
    """plot kappa vs. sigma"""
    cmap = plt.get_cmap(cmap)

    # read data
    kw = {"comment": "#"}
    df = pd.read_csv(results_file, **kw)

    columns = [
        "space_group",
        "n_formula",
        "material",
        "sigma",
        "kappa",
        "sigma_err",
        "kappa_err",
        "simulation_time",
    ]
    df = df[columns]

    # pick materials w/ >= 30ps simulation time
    tmax = 25 * 1000
    df = df[df.simulation_time > tmax]

    # kick out sigma > 1
    print("Materials with sigma > 1:")
    print(df[df.sigma.ge(1)])
    print(".. discard these for the plot")
    df = df[df.sigma.le(1)]

    print(f"min. simulation time: {tmax / 1000} ps")
    print(f"No. of datapoints:    {len(df)}")
    print(f"min. sigma:           {df.sigma.min()}")

    if exclude:  # exclude data points
        excludes = [s for s in open("exclude.dat").read().split() if "#" not in s]
        mask = [m not in excludes for m in df.material.astype(str)]
        df = df[mask]

    df.to_csv("data_for_plot.csv")

    # create canvas
    fig, ax = plt.subplots()
    fig.set_size_inches(4.1, 4.1)

    tax = ax.twinx()
    ax.set_zorder(tax.get_zorder() + 1)

    for x in (ax, tax):
        x.set_xscale("log"), x.set_yscale("log")
        x.set_ylim([0.05, 100]), x.set_xlim((0.125, 1))
        x.patch.set_visible(False)

    # ticks
    a0 = np.array([1, 3, 4, 5, 6, 7, 8, 9, 10])
    a1 = range(-1, 2)

    ticks = (0.2, 0.3, 0.4, 0.5, 1)
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks)

    ticks = (0.6, 0.7, 0.8, 0.9)
    ax.set_xticks(ticks, minor=True)
    ax.set_xticklabels([], minor=True)

    tax.set_yticks([])
    tax.set_yticks([], minor=True)

    # plot
    kw = {
        "x": "sigma",
        "y": "kappa",
        "s": 30,
        "ax": ax,
        "edgecolors": None,
        "alpha": 0.8,
    }

    # plot materials with small spread in sigma
    d_sigma_err = 0.01

    # plot this set based on space group
    df1 = df[df.sigma_err.le(d_sigma_err)]

    df_ort = df1[df1.space_group.le(62)]
    df_tet = df1[df1.space_group.eq(122)]
    df_tri = df1[df1.space_group.between(160, 166)]
    df_wur = df1[df1.space_group.eq(186)]
    df_zbl = df1[df1.space_group.eq(216) & df1.n_formula.eq(2)]
    df_hsl = df1[df1.space_group.eq(216) & df1.n_formula.eq(3)]
    df_csc = df1[df1.space_group.eq(221) & df1.n_formula.eq(2)]
    df_per = df1[df1.space_group.eq(221) & df1.n_formula.eq(5)]
    df_rck = df1[df1.space_group.eq(225) & df1.n_formula.eq(2)]
    df_caf = df1[df1.space_group.eq(225) & df1.n_formula.eq(3)]

    df_ort.plot.scatter(**kw, marker="8", color=cmap(2))
    # df_tet.plot.scatter(**kw, marker="|", color=cmap(10))
    df_tri.plot.scatter(**kw, marker="v", color=cmap(9))
    df_wur.plot.scatter(**kw, marker="H", color=cmap(0))
    df_rck.plot.scatter(**kw, marker="s", color=cmap(3))
    df_csc.plot.scatter(**kw, marker="d", color=cmap(4))
    df_per.plot.scatter(**kw, marker="X", color=cmap(6))
    # df_zbl.plot.scatter(**kw, marker="D", color=cmap(1))
    # df_caf.plot.scatter(**kw, marker="P", color=cmap(7))
    df_hsl.plot.scatter(**kw, marker=">", color=cmap(7))

    # legend = ["Orth.", "Tet.", "Tri.", "WZ", "RS", "CsCl", "Per.", "ZB", "CaF"]
    legend = ["Orth.", "Tri.", "WZ", "RS", "CsCl", "Per.", "Heus.", "else"]
    ax.legend(legend, framealpha=0, loc="upper right")

    # df1.plot.scatter(**kw, marker=".", color="k")

    df2 = df[df.sigma_err.gt(d_sigma_err)]
    kw["alpha"] = 1
    df2.plot.scatter(**kw, marker="*", color="purple", zorder=-1)

    # annotate these
    for (l, x, y) in zip(df2.material, df2.sigma, df2.kappa):
        ax.annotate(
            l,
            (x, y),
            xytext=(0, 3),
            ha="left",
            va="bottom",
            textcoords="offset points",
            # arrowprops={"arrowstyle": "-", "linewidth": 0.5},
        )

    for (l, x, y) in zip(df1.material, df1.sigma, df1.kappa):
        if l in annot_dict:
            kw = annot_dict[l]
            ax.annotate(l, (x, y), textcoords="offset points", **kw)

    # fit df1
    X, Y = df1.sigma, df1.kappa
    # fit logarithm
    slope, intercept, r_value, p_value, std_err = st.linregress(np.log(X), np.log(Y))

    print("Linregress:")
    print(f".. slope:     {slope}")
    print(f".. intercept: {intercept}")
    print(f".. r_value:   {r_value}")
    print(f".. p_value:   {p_value}")
    print(f".. std_err:   {std_err}")

    # exponentiate back
    x = np.linspace(0.1, 1, 3)
    y = intercept + slope * np.log(x)

    y_0 = np.exp(intercept)
    pow = x ** slope
    y = y_0 * pow

    tax.plot(x, y, color="k", lw=0.75, zorder=-5, ls="--", alpha=0.5)

    diff = 5
    tax.fill_between(
        x, y / diff, y * diff, color="black", alpha=0.05, lw=0, zorder=-3,
    )

    num_str = f"{slope:.1f}"
    fit_str = "$\\log \\kappa \\propto " + num_str + "\\cdot \\sigma^{\\rm A}$"
    fit_str += f"\nPearson $\\rho$: {abs(r_value):.2f}"
    tax.legend(
        [fit_str], loc="lower left", framealpha=1, fancybox=True, shadow=True,
    )

    # labels
    ax.set_ylabel("$\\kappa^{\\rm aiGK}_{300\\,{\\rm K}}$ (W/mK)")
    ax.set_xlabel("$\\sigma^{\\rm A}$ (1)")

    # plot and save
    figname = "kappa_vs_sigma.pdf"
    fig.savefig(figname, bbox_inches="tight")
    fig.savefig(Path(figname).stem + ".png", dpi=300, bbox_inches="tight")
    print(f".. plotted to {figname}")

    print("Materials w/ kappa < 1 W/mK")
    print(df[df.kappa.le(1)])


typer.run(main)
