import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from ase.io import read
from scipy.stats import gaussian_kde


plt.style.use("../../../plots.mplstyle")


def get_kde(atoms, element="F", rmax=5.5, bw_method=None):
    atoms_reduced = atoms[atoms.symbols == element]
    distances = np.sort(atoms_reduced.get_all_distances(mic=True).flatten())
    distances = distances[distances < rmax]

    kde = gaussian_kde(distances, bw_method=bw_method)

    return kde


def main(
    file: str,
    element: str = "F",
    rmin: float = 2.5,
    rmax: float = 4.7,
    nbins: int = 500,
    kde_width: float = 0.02,
    reference_file: str = "geometry.in.ref",
    format: str = "aims",
):
    atoms0 = read(reference_file, format=format)
    atoms1 = read(file, format=format)

    fig, ax = plt.subplots()
    fig.set_size_inches(4.1, 3.1)

    x = np.linspace(rmin, rmax, nbins)

    kw = {"element": element, "rmax": rmax, "bw_method": kde_width}

    kde = get_kde(atoms0, **kw)
    y0 = kde.evaluate(x)

    kde = get_kde(atoms1, **kw)
    y1 = kde.evaluate(x)

    # make pandas df
    df = pd.DataFrame({"reference": y0, "deformed": y1}, index=x)
    df.reference.plot(ax=ax, alpha=0.5)
    df.deformed.plot(ax=ax)

    ax.legend(["reference", "deformed"], framealpha=0)

    ax.set_xlabel(f"{element}-{element} distance (Å)")
    ax.set_ylabel(f"Radial distribution function (arb. units)")

    df.to_csv(file + ".csv")

    fig.savefig(file.replace(".", "_") + ".pdf", bbox_inches="tight")


typer.run(main)
