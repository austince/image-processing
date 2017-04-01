"""Vector Cluster
"""

import numpy as np


# Consider putting these in 'utils.py'
def vec_nd_average(vecs):
    dimensions = vecs[0].shape
    vec_sum = np.zeros(shape=dimensions, dtype='int64')

    for v in vecs:
        vec_sum += v

    return (vec_sum / len(vecs)).astype('int64')


def vec_3d_average(vecs):
    """

    :param vecs: 
    :return: 
    """
    vec_sum = np.zeros(shape=(3,), dtype='int64')

    for v in vecs:
        vec_sum[0] += v[0]
        vec_sum[1] += v[1]
        vec_sum[2] += v[2]

    return (vec_sum / len(vecs)).astype('int64')


def vec_nd_distance(vec1, vec2):
    """
    
    :param vec1: n dimensional vector
    :param vec2: n dimensional vector
    :return: 
    """
    sum_squares = 0
    for i in range(len(vec1)):
        sum_squares += ((vec1[i] - vec2[i]) ** 2)

    return np.sqrt(sum_squares)


def vec_3d_distance(vec1, vec2):
    return np.sqrt(
        (vec1[0] - vec2[0]) ** 2 +
        (vec1[1] - vec2[1]) ** 2 +
        (vec1[2] - vec2[2]) ** 2
    )


class Cluster:
    """
    A Vector Cluster
    """

    def __init__(self, center, distance_func=vec_nd_distance, avg_func=vec_nd_average):
        self.center_vec = center
        self.vecs = []
        self._distance_func = distance_func
        self._avg_func = avg_func

    # def __getattr__(self, item):
    #     if item == 'center':
    #         return self.center_vec
    #
    #     raise AttributeError("Cluster has no attribute: " + item)

    def distance_to_center(self, vec):
        return self._distance_func(self.center_vec, vec)

    def recenter(self):
        """

        :return: whether or not the center changed
        """
        mean = self._avg_func(self.vecs)
        old_center = self.center_vec
        self.center_vec = mean
        return (old_center != self.center_vec).all()

    def reset_vecs(self):
        self.vecs.clear()

    def add_vec(self, vec):
        self.vecs.append(vec)