""" K-means Processor
"""

import numpy as np
from termcolor import cprint

from .Processor import Processor, ClusterProcessor
from ._Cluster import Cluster
from image_processing.utils import cprint_progressbar


class Kmeans(ClusterProcessor):
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

        max_y, max_x, _ = image.shape
        self.point_clusters = np.ndarray(shape=(max_y, max_x), dtype=Cluster)

    def get_point_vec(self, y, x):
        """
        Get a vector to add to the cluster at point y, x
        :param y: 
        :param x: 
        :return: 
        """
        return self.image[y][x]

    def set_point_closest_cluster(self, y, x, cluster):
        """
        Set the point (y,x)'s cluster to cluster
        :param y: 
        :param x: 
        :param cluster: 
        :return: 
        """
        self.point_clusters[y][x] = cluster

    def recenter_points(self):
        # First reset all the points in the clusters
        self.reset_cluster_vecs()

        # Then center all points of the image
        max_y, max_x, _ = self.image.shape
        for y in range(max_y):
            for x in range(max_x):
                if self.verbose:
                    cprint_progressbar((y * max_x) + x, max_x * max_y, prefix='Points Centered:')
                point_vec = self.get_point_vec(y, x)
                closest = self.closest_cluster(y, x, point_vec)
                closest.add_vec(point_vec)
                # Keep track of which point is where for overlay
                self.set_point_closest_cluster(y, x, closest)

    def closest_cluster(self, y, x, vec):
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

    def print_info(self):
        super(Kmeans, self).print_info()
        cprint('Total clusters: ' + str(self.k))
        print()

    def process(self):
        """
        
        :return: the processed image 
        """
        max_y, max_x, _ = self.image.shape
        center_points = []

        if self.verbose:
            self.print_info()
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
            self.add_cluster(Cluster(self.image[point]))

        if self.verbose:
            cprint('Initial point center', 'yellow')

        self.recenter_points()

        if self.verbose:
            print()
            cprint('Initial cluster recenter', 'yellow')

        num_loops = 0
        # Find closest centers
        while self.recenter_clusters() != 0:
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

