import numpy as np

def near(pt,radius=1.0e-10):
    return lambda x: np.linalg.norm(pt-x)<radius
