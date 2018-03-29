import numpy as np
from scipy.spatial import KDTree

def match_point_clouds(X, Y):
    """
    In the worst case scenerario, we have no idea what the order is.
    Fortunately, we always write out the point coordinates in the plot data elems,
    so we can just brute force it.
    """
    tree = KDTree(X)
    d,i = tree.query(Y)
    #np.save("cache_match_point_clouds_{0}_{1}.npy".format(hash(X),hash(Y)),i)
    return i
