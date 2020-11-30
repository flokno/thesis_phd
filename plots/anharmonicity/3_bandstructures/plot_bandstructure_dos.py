#!/usr/bin/env python
# coding: utf-8


import subprocess as sp
from pathlib import Path

import click
import numpy as np

from plot_config import config, plt

try:
    from ruamel import yaml
except ModuleNotFoundError:
    import yaml


config.subplots_adjust.kw.update(
    {"left": 0.15, "right": 0.9, "bottom": 0.15, "wspace": 0.1}
)


linewidth = 0.75
line_kw = {"color": "black", "linestyle": "-", "linewidth": linewidth}


@click.command()
@click.argument("folder", type=Path)
@click.option("--blue", is_flag=True)
@click.option("--ratio", default=1.618)
@click.option("--ymin", default=0)
@click.option("--ymax", default=16)
@click.option("--reference", type=Path)
def plot(folder, blue, ratio, ymin, ymax, reference):
    """plot bandstructure data in folder"""
    (distances, frequencies, segment_nqpoint, xticks, labels) = read_band_yaml(
        folder / "band.yaml"
    ).values()

    dos = np.loadtxt(folder / "total_dos.dat")

    if blue:
        c = config.color.c1k
    else:
        c = config.color.c2k

    ylim = (ymin, ymax)

    fill_kw = {"color": c, "alpha": config.color.alpha}
    plot_kw = {"color": c, "linestyle": "-", "linewidth": 1}

    fig, (ax, ax2) = plt.subplots(
        ncols=2,
        sharey=True,
        gridspec_kw={"width_ratios": config.gridspec.bandplot.ratio},
    )
    fig.subplots_adjust(**config.subplots_adjust.kw)
    fig.set_size_inches(4.1, 2.1)

    ax.plot(distances, frequencies, **plot_kw)

    if reference is not None:
        ref_data = np.loadtxt(reference)
        ax.plot(*ref_data.T, "o", mfc="None", mec="k", ms=3, mew=0.8)

    for x in xticks:
        ax.axvline(x, **line_kw)

    ax.set_xticks(xticks)
    ax.set_xticklabels(labels)

    ax2.set_xticks([])
    x, y = dos[:, 1], dos[:, 0]
    ax2.fill(x, y, **fill_kw)
    ax2.plot(x, y, **plot_kw)

    ax.axhline(0, color="k", linewidth=linewidth)

    ax.set_xlim(0, distances[-1])
    ax.set_ylim(*ylim)
    yticks = np.arange(min(ylim), 1.05 * max(ylim), 2)
    ax.set_yticks(yticks)
    ax2.set_yticks(yticks)

    ax.set_ylabel(r"$\omega$ (THz)")

    ax2.yaxis.set_label_position("right")
    # ax2.yaxis.set_ticks_position('right')
    ax2.set_ylabel("DOS (arb. units)", rotation=270, labelpad=15)

    ax.xaxis.set_tick_params(direction="in", which="both", width=linewidth)
    ax2.yaxis.set_tick_params(direction="out", which="both", width=linewidth)

    outfile = folder / "bands_dos.pdf"
    print(f"Save plot to {outfile}")
    fig.savefig(outfile, transparent=True, bbox_inches="tight")

    # embed fonts
    cmd = (
        "gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite "  # -dPDFSETTINGS=/prepress "
        "-dEmbedAllFonts=true "
        f"-sOutputFile={folder / outfile.stem}_emb.pdf -f {outfile}"
    )
    sp.run(cmd.split())


def read_band_yaml(filename):
    data = yaml.safe_load(open(filename))  # , Loader=yaml.CLoader)
    frequencies = []
    distances = []
    labels = []
    for j, v in enumerate(data["phonon"]):
        if "label" in v:
            labels.append(v["label"])
        else:
            labels = None
        frequencies.append([f["frequency"] for f in v["band"]])
        distances.append(v["distance"])

    if labels is None:
        labels = [l[0] for l in data["labels"]]
        labels.append(data["labels"][-1][-1])

    new_labels = []
    for label in labels:
        new_labels.append(label.replace(r"\mathsf", ""))
    labels = new_labels

    xticks = [distances[ii * n] for ii, n in enumerate(data["segment_nqpoint"])]
    xticks.append(distances[-1])

    return {
        "distances": np.array(distances),
        "frequencies": np.array(frequencies),
        "segment_nqpoint": data["segment_nqpoint"],
        "xticks": np.array(xticks),
        "labels": labels,
    }


if __name__ == "__main__":
    plot()
