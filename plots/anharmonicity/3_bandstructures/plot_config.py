import matplotlib as mpl
import matplotlib.pyplot as plt
import toml

mpl.use("pdf")


class adict(dict):
    def __init__(self, obj={}):
        super().__init__(obj)
        self.__dict__ = self


plt.style.use("../../plots.mplstyle")
fontsize = plt.rcParams["font.size"]

config = toml.load("../config.toml", _dict=adict)

# linestyle
loosely_dashed = (0, (5, 7))
config.quantiles.kw["ls"] = loosely_dashed

# size
config.size.height = config.size.width / config.size.ratio
