"""Vector Cluster
"""

import numpy as np
from termcolor import cprint

from ...operations.utils import cprint_progressbar


# Consider putting these in 'utils.py'
def vec_average(vecs):
    """

    :param vecs: 
    :return: 
    """
    avg = [0, 0, 0]

    for v in vecs:
        avg[0] += v[0]
        avg[1] += v[1]
        avg[2] += v[2]

    avg[0] /= len(vecs)
    avg[1] /= len(vecs)
    avg[2] /= len(vecs)

    return np.asarray(avg).astype('int8')


def vec_distance(vec1, vec2):
    # sum_squares = 0
    # for i in range(len(vec1)):
    #     sum_squares += ((vec1[i] - vec2[i]) ** 2)

    return np.sqrt(
        (vec1[0] - vec2[0]) ** 2 +
        (vec1[1] - vec2[1]) ** 2 +
        (vec1[2] - vec2[2]) ** 2
    )


class Cluster:
    """
    A Vector Cluster
    """

    def __init__(self, center):
        self.center_vec = center
        self.vecs = []

    # def __getattr__(self, item):
    #     if item == 'center':
    #         return self.center_vec
    #
    #     raise AttributeError("Cluster has no attribute: " + item)

    def distance_to_center(self, vec):
        return vec_distance(self.center_vec, vec)

    def recenter(self):
        """

        :return: whether or not the center changed
        """
        mean = vec_average(self.vecs)
        old_center = self.center_vec
        self.center_vec = mean
        return (old_center != self.center_vec).all()

    def reset_vecs(self):
        self.vecs = []
