import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


log = open("convergence.log", "w")

plt.style.use("../paper.mplstyle")
fontsize = plt.rcParams["font.size"]


# colors
c1, c1k = "#5759aa", "#3F417C"
c2, c2k = "#9c4c36", "#803E2C"
alpha = 0.5

s1 = np.loadtxt("datasets/Si.sampling.dat")
s2 = np.loadtxt("datasets/KCaF3.sampling.dat")

s1 = pd.Series(s1)
s2 = pd.Series(s2)
s1.index += 1
s2.index += 1

name1 = "Si"
name2 = "KCaF$_3$"

# create canvas
subplots_adjust_kw = {
    "left": 0.125,
    "right": 0.98,
    "bottom": 0.175,
    "top": 0.98,
}

fig, ax = plt.subplots()
fig.subplots_adjust(**subplots_adjust_kw)
fig.set_size_inches(4.1, 2.28)


## plot
kw2 = {"marker": "o", "linewidth": 0, "ms": 3}

# MD reference
ax.axhline(0.153, c="k", zorder=0, ls=(0, (5, 5)))
ax.axhline(0.362, c="k", zorder=0, ls=(0, (5, 5)))

# data
ax.plot(s1, c=c1, **kw2)
ax.plot(s2, c=c2, **kw2)

# mean and expanding std
s = s2
std = s.expanding(min_periods=2).std() / s.index ** 0.5
ax.fill_between(s.index, s.mean() + std, s.mean() - std, alpha=alpha, facecolor=c2k)

# ax.plot(s1.expanding(min_periods=2).mean(), c=c1k)
ax.plot(s2.expanding(min_periods=2).mean(), c=c2k)


# limits
ylim = 0.65
xlim = 30
ax.set_ylim(0, ylim)
ax.set_xlim(0, xlim + 1)

# ticks
ax.tick_params(direction="in", which="both", right=True, top=True)
ax.set_xticks(np.arange(0, 1.1 * xlim, 5))
ax.set_xticks(np.arange(0, xlim, 1), minor=True)
ax.set_yticks(np.arange(0, ylim, 0.2))
ax.set_yticks(np.arange(0, ylim, 0.1), minor=True)

# label
ax.set_xlabel("sample number $n$")
# ylabel = r"$\sigma \left[ \tilde F^\mathrm{\,A} (t) \right]$"
# ylabel = r"$\sigma \left[ F^\mathrm{\,A} (t) \right]$ $/$ $\sigma \left[ F (t) \right]$"
ylabel = r"$\sigma^{\rm A} [{\bf R}_n]$"
ax.set_ylabel(ylabel, labelpad=5)  # , rotation=0, y=0.4)

kw = {
    "ha": "center",
    "va": "center",
    "transform": fig.transFigure,
    "fontsize": fontsize + 2,
}

plt.text(0.85, 0.275, "Si", color=c1k, **kw)
plt.text(0.85, 0.75, r"KCaF$_3$", color=c2k, **kw)


# save
fig.savefig("convergence_sigma_MC.pdf")


# log statistic
for name, s in zip((name1, name2), (s1, s2)):
    log.write(f"System: {name}\n")
    log.write(f"sigma.mean= {s.mean()}\n")
    log.write(f"sigma.std= {s.std()}\n")
    log.write(f"sigma[:10].mean= {s.iloc[:10].mean()}\n")
    log.write(f"sigma[:10].std= {s.iloc[:10].std()}\n")
