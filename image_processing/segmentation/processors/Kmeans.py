""" K-means Processor
"""

import numpy as np
from termcolor import cprint

from . import Processor
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

    return np.asarray(avg).astype('int16')


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
        
        :return: true if changed, false is the same
        """
        if len(self.vecs) == 0:
            return False

        mean = vec_average(self.vecs)
        old_center = self.center_vec
        self.center_vec = mean
        return (old_center != self.center_vec).all()

    def reset_vecs(self):
        self.vecs.clear()

    def add_vec(self, vec):
        self.vecs.append(vec)


class Kmeans(Processor):
    """
    A K-means implementation
    """
    
    def __init__(self, image, cli_args=None, k=10):
        super(Kmeans, self).__init__(cli_args=cli_args)

        if cli_args.k_value:
            self.k = cli_args.k_value
        else:
            self.k = k
        self.image = image.astype('int64')
        self.clusters = []
        max_y, max_x, _ = image.shape
        self.point_clusters = np.ndarray(shape=(max_y, max_x), dtype=Cluster)

    def recenter_clusters(self):
        centers_changed = False
        num_changed = 0
        for i in range(len(self.clusters)):
            if self.verbose:
                cprint_progressbar(i, len(self.clusters) - 1, prefix='Clusters Centered:')

            changed = self.clusters[i].recenter()

            if changed:
                num_changed += 1

            # If any cluster has changed centers, report True
            centers_changed = changed | centers_changed

        if self.verbose:
            cprint('Number of changed centers: ' + str(num_changed), 'yellow')

        return centers_changed

    def reset_points(self):
        for cluster in self.clusters:
            cluster.reset_vecs()

    def recenter_points(self):
        # First reset all the points in the clusters
        self.reset_points()

        # Then center all points of the image
        max_y, max_x, _ = self.image.shape
        for y in range(max_y):
            for x in range(max_x):
                if self.verbose:
                    cprint_progressbar((y * max_x) + x, max_x * max_y, prefix='Points Centered:')
                point = (y, x)
                point_vec = self.image[point]
                closest = self.closest_cluster(point_vec)
                closest.add_vec(point_vec)
                # Keep track of which point is where for overlay
                self.point_clusters[point] = closest

    def closest_cluster(self, vec):
        closest = self.clusters[0]
        closest_dist = closest.distance_to_center(vec)

        for clust in self.clusters[1:]:
            dist = clust.distance_to_center(vec)
            if dist < closest_dist:
                closest_dist = dist
                closest = clust

        return closest

    def overlay(self):
        """
        Overlay the Clusters onto the image
        :return: 
        """
        max_y, max_x = self.point_clusters.shape
        for y in range(max_y):
            for x in range(max_x):
                self.image[y][x] = self.point_clusters[y][x].center_vec

    def process(self):
        """
        
        :return: the processed image 
        """
        max_y, max_x, _ = self.image.shape
        center_points = []

        print()
        cprint('Info:', 'cyan')
        cprint('Total points: ' + str(max_x * max_y), 'yellow')
        print()

        cprint('Sampling centers', 'yellow')
        # Randomly sample centers
        for i in range(self.k):
            # Randomly add a center that has not yet been picked
            point = None
            while point is None or point in center_points:
                point = (
                    int(max_y * np.random.random()),
                    int(max_x * np.random.random())
                )
            self.clusters.append(Cluster(self.image[point]))

        cprint('Initial point center', 'yellow')
        self.recenter_points()

        cprint('Initial cluster recenter', 'yellow')

        num_loops = 1
        # Find closest centers
        while self.recenter_clusters():
            cprint('Recentering loop #' + str(num_loops), 'yellow')
            num_loops += 1
            # Repeat until all clusters have found their optimal centers
            self.recenter_points()

        cprint('Centering complete', 'green')

        cprint('Overlaying', 'yellow')
        self.overlay()

        return self.image


