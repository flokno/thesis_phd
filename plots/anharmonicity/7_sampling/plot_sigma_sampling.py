"""inspired by https://www.bastibl.net/publication-quality-plots/"""
from scipy import stats
import pandas as pd
from plot_sigma import plt, df, get_canvas, ms, lw, fontsize

# mpl.use("pdf")

log = open("linregress.log", "w")

df_si = pd.read_csv("Si.csv", index_col="temp", comment="#")

figname = "sigma_temp_one_shot.pdf"

c1, c1k = "#5759aa", "#3F417C"
c2, c2k = "#9c4c36", "#803E2C"

fig, ax = get_canvas(fill=False)
ax.plot(df.Pnma, color=c2k, marker="o", label=r"KCaF$_3$ MD", ms=ms, lw=lw)

kw = {"lw": lw, "ms": ms * 0.8, "linestyle": "dotted", "marker": "v"}
ax.plot(df.oneshot, color=c2, zorder=2, **kw)
ax.plot(df_si.oneshot, color=c1k, zorder=0, **kw)

ax.plot(df_si.MD, color="k", marker="o", ms=ms * 1.3, lw=lw, zorder=1)

# ax.legend(fancybox=False)
kw = {
    "ha": "center",
    "va": "center",
    "transform": fig.transFigure,
    "fontsize": fontsize + 1,
}
plt.text(0.8, 0.41, "Si one-shot", rotation=3, color=c1k, **kw)
plt.text(0.45, 0.75, r"KCaF$_3$ MD", rotation=13, color=c2k, **kw)
plt.text(0.75, 0.59, r"KCaF$_3$ one-shot", rotation=10, color=c2, **kw)
plt.text(0.68, 0.26, "Si MD", rotation=0, color="k", **kw)


# linear regression for first three points
for n, s in zip(
    ("KCaF3 MD", "KCaF3 oneshot", "Si oneshot"), (df.Pnma, df.oneshot, df_si.oneshot)
):
    x, y = s[:2].index, s[:2]
    m, y0, r, p, std = stats.linregress(x, y)
    # ax.plot(s.index, s.index * m + y0)
    str = f"{n}\n" r"$\sigma (T)$ = " f"{m:.6f} * T + {y0:.6f}\n"
    print(str)
    log.write(str)


fig.savefig(figname, bbox_inches="tight", pad=0)
