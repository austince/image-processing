"""Vector Cluster
"""

import numpy as np
from image_processing.utils import vec_nd_average, vec_nd_distance


class Cluster:
    """
    A Vector Cluster
    """

    def __init__(self, center, distance_func=vec_nd_distance, avg_func=vec_nd_average):
        """
        
        :param center: vector 
        :param distance_func: 
        :param avg_func: 
        """
        self.center_vec = center
        self.vecs = []
        self._distance_func = distance_func
        self._avg_func = avg_func

    def distance_to_center(self, vec):
        return self._distance_func(self.center_vec, vec)

    def recenter(self):
        """

        :return: whether or not the center is different from before recentering
        """
        mean = self._avg_func(self.vecs)
        old_center = self.center_vec
        self.center_vec = mean
        return (old_center != self.center_vec).all()

    def reset_vecs(self):
        self.vecs.clear()

    def add_vec(self, vec):
        self.vecs.append(vec)
