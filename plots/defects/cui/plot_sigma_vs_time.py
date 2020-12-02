from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import typer

plt.style.use("../../plots.mplstyle")
plt.tick_params(top=True)

red = "#9c4c36"
grey = "#6d6d6d"
black = "#1b1b1b"
sepia = "#704214"
purple = "#800080"

fontsize = plt.rcParams["font.size"]


def main(
    cmap: str = "tab10",
    outfile: str = "sigma_vs_time.pdf",
    results_file: str = "sigmas_per_trajectory.csv",
    index_col: str = "time",
):
    """plot kappa vs. sigma"""
    cmap = plt.get_cmap(cmap)

    # read data
    kw = {"comment": "#", "index_col": index_col}
    df = pd.read_csv(results_file, **kw)

    # to ps
    df.index /= 1000

    # create canvas
    fig, axs = plt.subplots(nrows=df.shape[1], sharex=True)
    fig.set_size_inches(4.1, 4.1)
    fig.subplots_adjust(hspace=0)

    labels = ["a)", "b)", "c)", "d)", "e)"]

    for ii, ax in enumerate(axs):
        s = df.iloc[:, ii]
        s.plot(ax=ax, c=grey, lw=1, alpha=0.5)

        roll = s.rolling(200, center=True).mean()
        roll.plot(ax=ax, c=black, lw=1)

        # average where sigma < 1
        y0 = roll[roll.lt(1)].mean()
        # first peak
        y1 = roll[roll.ge(2 * y0) & roll.lt(3 * y0)].mean()
        y2 = roll[roll.ge(3 * y0)].mean()

        typer.echo(f"Base line: {y0}")
        typer.echo(f"1st jump:  {y1}")
        typer.echo(f"2nd jump:  {y2}")
        kw = {"color": red, "lw": 0.8, "ls": "--"}
        ax.axhline(y0, **kw)
        ax.axhline(y1, **kw)
        ax.axhline(y2, **kw)
        # ax.axhline(y0, lw=0.75, c="#704214", ls="--")
        # ax.plot([0, x0], [y0, y0])
        # ax.text(1, 0.11, "$\\sigma^{\\rm A}$ = " + f"{y0:.2f}")
        x = 62
        for y in (y0, y1, y2):
            if not y:
                continue
            ax.text(x, y, f"{y:.1f}", va="center", fontsize=fontsize - 1)

        ax.set_ylim([0, 2])

        ax.text(1, 1.9, labels[ii], va="top")

        ax.set_yticks([0, 1])
        ax.set_yticks(np.arange(0, 2, 0.25), minor=True)

    ax.set_xlabel("Time $t$ (ps)")
    ax.set_xlim([0, df.index.max()])
    # ax.set_xlim([-5, 70])

    axs[0].set_ylabel("$\\sigma^{\\rm A} (t)$", rotation=0, labelpad=10, y=1, va="top")
    #   legend = ["raw data", "$200\\,$fs avg."]
    #   leg = axs[0].legend(legend, framealpha=0, ncol=2, fontsize=fontsize-1)
    #   hp = leg._legend_box.get_children()[1]
    #   for vp in hp.get_children():
    #       for row in vp.get_children():
    #           row.set_width(70)  # need to adapt this manually
    #           row.mode = "expand"
    #           row.align = "right"

    fig.savefig(outfile, bbox_inches="tight")
    fig.savefig(Path(outfile).stem + ".png", bbox_inches="tight", dpi=600)


typer.run(main)
