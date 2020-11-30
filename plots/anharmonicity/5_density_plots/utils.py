import numpy as np
import pandas as pd
from scipy import stats


def get_xy(ds, norm=False, harmonic=False):
    """return f and fA as pd.Series"""
    f, fh = ds.forces.data, ds.forces_harmonic.data
    std = f.std()

    f /= std
    fh /= std

    if harmonic:
        fa = fh
    else:
        fa = f - fh

    if norm:
        f = np.linalg.norm(f, axis=2)
        fa = np.linalg.norm(fa, axis=2)

    X = pd.Series(f.flatten())
    Y = pd.Series(fa.flatten())

    return X, Y, std


# KDE estimation
def get_kde(X, Y, npoints=25j, xlim=2, ylim=2, positive=False):
    """get kde, return x, y, f"""
    if positive:
        xx, yy = np.mgrid[0:xlim:npoints, 0:ylim:npoints]
    else:
        xx, yy = np.mgrid[-xlim:xlim:npoints, -ylim:ylim:npoints]

    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([X, Y])
    kernel = stats.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    return xx, yy, f
