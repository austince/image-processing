""" K-means Processor
"""

import numpy as np
from termcolor import cprint

from . import Processor
from ._Cluster import Cluster
from image_processing.utils import cprint_progressbar


class Kmeans(Processor):
    """
    A K-means implementation
    """
    
    def __init__(self, image, cli_args=None, k=10):
        super(Kmeans, self).__init__(image, cli_args=cli_args)

        if cli_args.k_value:
            self.k = cli_args.k_value
        else:
            self.k = k

        if self.k < 1:
            raise ValueError('K must be at least 1')

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

        if self.verbose:
            print()
            cprint('Info:', 'cyan')
            print('Total points: ' + str(max_x * max_y))
            print('Total clusters: ' + str(self.k))
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

        if self.verbose:
            cprint('Initial point center', 'yellow')

        self.recenter_points()

        if self.verbose:
            print()
            cprint('Initial cluster recenter', 'yellow')

        num_loops = 0
        # Find closest centers
        while self.recenter_clusters():
            num_loops += 1
            if self.verbose:
                cprint('Recentering loop #' + str(num_loops), 'yellow')
            # Repeat until all clusters have found their optimal centers
            self.recenter_points()

        if self.verbose:
            cprint('Centering complete', 'green')
            cprint('Overlaying', 'yellow')

        self.overlay()

        return self.image

    def get_file_prefix(self):
        return 'k-' + str(self.k)

