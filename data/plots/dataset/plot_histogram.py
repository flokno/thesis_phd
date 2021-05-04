import numpy as np
import pandas as pd
import seaborn as sns
import typer
from matplotlib import pyplot as plt

subplots_adjust_kw = {
    "left": 0.125,
    "right": 0.98,
    "bottom": 0.175,
    "top": 0.98,
}

sns.set_style("ticks")
plt.style.use("../plots.mplstyle")

# https://coolors.co/0013c7-0e04a0-0b0285-070069-520a64-720236-860229-9a021c-9f010e-a40000
colors = [
    "#0013c7",
    "#0013c7",
    "#0013c7",
    "#0013c7",
    "#0013c7",
    "#0e04a0",
    "#0b0285",
    "#070069",
    "#520a64",
    "#720236",
    "#860229",
    "#9a021c",
    "#9f010e",
    "#a40000",
    "#a40000",
    "#a40000",
    "#a40000",
    "#a40000",
    "#a40000",
    "#a40000",
    "#a40000",
]


def main(file: str = "list_final.csv", outfile: str = "histogram.pdf"):
    # read data
    df = pd.read_csv(file)

    fig, ax = plt.subplots(figsize=(4.1, 3))
    # create canvas
    fig.subplots_adjust(**subplots_adjust_kw)
    fig.set_size_inches(4.1, 2.28)

    s = df.sigmaA_300
    bins = np.arange(0.1, 0.6, 0.025)
    n, bins, patches = ax.hist(s, density=False, bins=bins)
    ax.axvline(s.mean(), c="k", label="mean")
    ax.axvline(s.median(), c="k", ls="--", label="median")
    ax.legend(frameon=False)
    ax.grid(False)

    ax.set_xlabel(r"$\sigma^{\rm A}_{\rm OS}$")
    ax.set_ylabel("Count")

    # color
    for ii, p in enumerate(patches):
        plt.setp(p, "facecolor", colors[ii])

    fig.savefig("histogram.pdf", bbox_inches="tight")


if __name__ == "__main__":
    typer.run(main)
