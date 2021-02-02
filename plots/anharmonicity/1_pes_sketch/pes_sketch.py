import numpy as np
from matplotlib import pyplot as plt


plt.style.use("../../plots.mplstyle")

c1 = "#363639"
c2 = "#5759aa"
c3 = "#9c4c36"

c2k = "#3F417C"  # blue 30% black
c3k = "#803E2C"  # red 30% black

x = np.linspace(-2.5, 10, 1000)

# maybe use
# https://matplotlib.org/gallery/axisartist/demo_axisline_style.html

fig, (ax1, ax2) = plt.subplots(figsize=(4, 7), nrows=2, sharex=True)

fontsize = 20

w3 = 0.3
w4 = 0.024

# define potential, harmonic approx, anharmonic contribution + derivatives
y2 = lambda x: x ** 2
y3 = lambda x: y2(x) - w3 * x ** 3 + w4 * x ** 4
dy = lambda x: y3(x) - y2(x)

f2 = lambda x: -2 * x
f3 = lambda x: f2(x) + 3 * w3 * x ** 2 - 4 * w4 * x ** 3
df = lambda x: f3(x) - f2(x)

kw = {"lw": 2}
ax1.plot(x, y3(x), c=c1, lw=2)
ax1.plot(x, y2(x), ls="--", c=c2, **kw)
ax1.plot(x, y3(x) - y2(x), c=c3, **kw)

ax2.plot(x, f3(x), c=c1, lw=2)
ax2.plot(x, f2(x), ls="--", c=c2, **kw)
ax2.plot(x, f3(x) - f2(x), c=c3, **kw)

# arrows
kw_arrow_axis = {"head_width": 0.3, "head_length": 0.5, "fc": c1, "ec": c1}

# backbone of plot (x- and y-axes, labels)
for ax in (ax1, ax2):
    ax.set_xticks([]), ax.set_xticklabels([]), ax.set_yticks([]), ax.set_yticklabels([])

    ax.set_xlim([-4, 8]), ax.set_ylim([-4.5, 4.5])

    ax.arrow(-3.5, 0, 10.5, 0, **kw_arrow_axis)
    ax.arrow(-3.5, -5, 0, 8.9, **kw_arrow_axis)

    # draw x-axis label
    kw = {"fontsize": fontsize}
    ax.text(6.1, 0.35, r"${\bf R}$", **kw)

    # draw equil. position
    ax.text(-1.1, -1.1, r"${\bf R}_0$", **kw)

    kw = {"ms": 12, "c": "k", "mew": 2}
    ax.plot(0, 0, "|", **kw)

    for spine in ("left", "bottom", "right", "top"):
        ax.spines[spine].set_visible(False)

x0 = 1.9
# draw line
ax1.plot([x0, x0], [dy(x0), y2(x0)], c=c1, lw=1.5)
ax2.plot([x0, x0], [df(x0), f2(x0)], c=c1, lw=1.5)

# draw atom
kw = {"ms": 22, "c": "k"}
ax1.plot(x0, 0, ".", **kw)
ax2.plot(x0, 0, ".", **kw, zorder=4)

# labels
r0 = 2.6
ax1.text(r0, 1.3, r"$\mathcal V$", fontsize=fontsize, c=c1)
ax1.text(r0, 3.4, r"$\mathcal V^{(2)}$", fontsize=fontsize, c=c2)
ax1.text(r0, -2.2, r"$\mathcal V^{\rm A}$", fontsize=fontsize, c=c3)

ax2.text(r0, -2.1, r"$ F$", fontsize=fontsize, c=c1)
ax2.text(r0, -4.1, r"${ F}^{(2)}$", fontsize=fontsize, c=c2)
ax2.text(r0, 2.2, r"${ F}^{\rm A}$", fontsize=fontsize, c=c3)

kw = {"rotation": 90, "labelpad": 0, "y": 0.5, "fontsize": fontsize - 3}
ax1.set_ylabel(r"{\rm Potential Energy}", **kw)
ax2.set_ylabel(r"{\rm Force}", **kw)


fig.savefig("sketch_vertical.pdf", bbox_inches="tight")
