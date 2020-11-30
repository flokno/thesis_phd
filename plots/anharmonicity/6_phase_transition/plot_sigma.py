"""inspired by https://www.bastibl.net/publication-quality-plots/"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.use("pdf")

plt.style.use("../paper.mplstyle")
fontsize = plt.rcParams["font.size"]

subplots_adjust_kw = {"left": 0.16, "right": 0.95, "bottom": 0.2, "top": 0.95}

# plot
figname = "sigma_temp.pdf"
df = pd.read_csv("KCaF3.csv", index_col="temp", comment="#")

lw = 1.1
ms = 3.5
ymin, ymax = 0.0, 1.1
c2k = "#803E2C"


# set up canvas
def get_canvas(ymin=ymin, ymax=ymax, fill=True):
    fig, ax = plt.subplots()
    fig.subplots_adjust(**subplots_adjust_kw)
    fig.set_size_inches(4.1, 2.28)

    # labels and ticks
    ax.set_xlabel(f"Temperature $T$ (K)")
    ax.set_ylabel(r"$\sigma^\mathrm{\,A} (T)$", labelpad=5)  # , rotation=0, y=0.4)
    ax.set_xlim([180, 820])
    ax.set_ylim([ymin, ymax])
    ax.set_xticks(np.arange(200, 1.1 * 800, 100), minor=True)
    ax.set_yticks(np.arange(ymin, ymax, 0.2))
    ax.set_yticks(np.arange(ymin, ymax, 0.1), minor=True)

    if fill:
        ax.fill_betweenx([0, 1.5], 0, 500, color="k", alpha=0.2, linewidth=0)
        ax.fill_betweenx([0, 1.5], 500, 900, color=c2k, alpha=0.2, linewidth=0)

    ax.tick_params(direction="in", which="both", right=True, top=True)

    return fig, ax


if __name__ == "__main__":
    fig, ax = get_canvas()
    ax.plot(df.Pnma, color="k", marker="o", label=df.Pnma.name, ms=ms, lw=0, zorder=1)
    ax.plot(df.Cub, color=c2k, marker="s", zorder=0, ms=ms, lw=0)

    # plot lines
    ax.plot(df.iloc[:4].Pnma, color="k", ls="-", lw=lw, zorder=-1)
    ax.plot(df.iloc[3:].Pnma, color="k", ls="--", lw=lw, zorder=-1)
    ax.plot(df.iloc[:4].Cub, color=c2k, ls="--", lw=lw, zorder=-1)
    ax.plot(df.iloc[3:].Cub, color=c2k, ls="-", lw=lw, zorder=-1)

    c2, c2k = "#9c4c36", "#803E2C"
    kw = {
        "ha": "center",
        "va": "center",
        "transform": fig.transFigure,
        "fontsize": fontsize + 1,
    }
    # plt.text(0.75, 0.62, r"Cubic", rotation=0, color=c2k, **kw)
    plt.text(0.3, 0.7, r"Cubic", rotation=0, color=c2k, **kw)
    plt.text(0.3, 0.35, r"Pnma", rotation=13, color="k", **kw)
    #

    fig.savefig(figname)
