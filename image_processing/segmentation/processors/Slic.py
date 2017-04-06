""" SLIC Processor
"""

import numpy as np
from termcolor import cprint

from .Processor import ClusterProcessor
from ._Cluster import Cluster
from image_processing.utils import gradient_magnitude as grad_mag
from image_processing.utils import vec_nd_average, vec_nd_distance, cprint_progressbar, vicinity_bounds


def make_flat_vec(y, x, rbg):
    center = np.ndarray(shape=(5,))
    center[0] = y
    center[1] = x
    center[2:] = rbg

    return center


def rgb_grad(center, lower, right):
    """
    
    :param center: rgb vector in focus
    :param lower: rgb vector one pixel below
    :param right: rgb vector one pixel to the right
    :return: 
    """
    # Each color dy dx
    r_mag = grad_mag((
        center[0] - lower[0],
        center[0] - right[0],
    ))
    g_mag = grad_mag((
        center[1] - lower[1],
        center[1] - right[1],
    ))
    b_mag = grad_mag((
        center[2] - lower[2],
        center[2] - right[2],
    ))

    return np.sqrt((r_mag ** 2) + (b_mag ** 2) + (g_mag ** 2))


def slic_vec_distance(vec1, vec2):
    """
    Use Euclidean distance, but divide x and y by 2
    :param vec1: 
    :param vec2: 
    :return: 
    """
    # Adjust x and y
    adj_vec1 = vec1.copy()
    adj_vec1[0] /= 2
    adj_vec1[1] /= 2

    adj_vec2 = vec2.copy()
    adj_vec2[0] /= 2
    adj_vec2[1] /= 2

    return vec_nd_distance(adj_vec1, adj_vec2)


class SlicCluster(Cluster):
    def __init__(self, center, distance_func=vec_nd_distance, avg_func=vec_nd_average):
        super(SlicCluster, self).__init__(center, distance_func=distance_func, avg_func=avg_func)

    def get_center_rgb(self):
        return self.center_vec[2:]


class Slic(ClusterProcessor):
    """
    Divide image into blocks of 50x50
        Initialize a centroid at the center of each block
    Compute Magnitude of Gradient in each of the RGB channels
        Use the square root of the sum of squares of the three magnitudes 
        Move centroids to the position with the smallest gradient magnitude in 3x3 windows
            centered on initial centroids
    Apply k-means in the 5D space of x, y, RGB
        Use Euclidean distance, but divide x and y by 2
    Optional:
        Only compare pixels to centroids within a distance of 100 pixels (2x block size) during update
    After convergence:
        Color pixels that touch two or more clusters black
        All others the average of their region
    """

    def __init__(self, image, cluster_width=50, cluster_height=50, stop_error=.05, cli_args=None):
        super(Slic, self).__init__(image, cli_args=cli_args)

        if cli_args.cluster_width:
            self.cluster_width = cli_args.cluster_width
        else:
            self.cluster_width = cluster_width

        if cli_args.cluster_height:
            self.cluster_height = cli_args.cluster_height
        else:
            self.cluster_height = cluster_height

        self.show_borders = True
        if 'no_borders' in cli_args and cli_args.no_borders:
            self.show_borders = False

        if cli_args.stop_error:
            stop_error = cli_args.stop_error

        max_y, max_x, _ = self.image.shape
        # List of clusters associated with points
        self.point_clusters = np.ndarray(shape=(max_y, max_x), dtype=SlicCluster)

        self.height_sections = int(max_y / self.cluster_height)
        self.width_sections = int(max_x / self.cluster_width)

        # initialize clusters
        self._segment_clusters()

        self.stop_under = stop_error * len(self.clusters)
        self.stop_error = stop_error

        # All the distances from points to their closest cluster
        self.point_distances = np.ndarray(shape=(max_y, max_x), dtype='float64')
        self.point_distances.fill(np.finfo(self.point_distances.dtype).max)

    def _segment_clusters(self):
        """
        Initialize the clusters by breaking them into cluster_height x cluster_width chunks
        :return: 
        """
        max_y, max_x, _ = self.image.shape
        # Segment cluster Width x cluster Height
        c_offset_y = int(self.cluster_height / 2)
        c_offset_x = int(self.cluster_width / 2)
        for y in range(0, max_y - c_offset_y, self.cluster_height):
            for x in range(0, max_x - c_offset_x, self.cluster_width):
                c_y = y + c_offset_y
                c_x = x + c_offset_x

                if c_y >= max_y:
                    c_y = max_y - 1

                if c_x >= max_x:
                    c_x = max_x - 1

                # Find the local gradient minimum in 3x3 window
                # Move center there
                min_y, min_x = self.local_grad_min(c_y, c_x)
                cluster = self._make_cluster(min_y, min_x)
                self.add_cluster(cluster)

    def _make_cluster(self, y, x):
        center = make_flat_vec(y, x, self.image[y][x])
        return SlicCluster(center, distance_func=slic_vec_distance)

    def rgb_grad(self, center_y, center_x):
        """
        Use the square root of the sum of squares of the three magnitudes 
        :param center_y:
        :param center_x:
        :return: 
        """
        max_y, max_x, _ = self.image.shape

        right_x = center_x + 1
        if right_x >= max_x:
            # Actually, let's take the left?
            right_x = max_x - 2

        lower_y = center_y + 1
        if lower_y >= max_y:
            # Actually, let's take above?
            lower_y = max_y - 2

        one_right_vec = self.image[center_y][right_x]
        one_lower_vec = self.image[lower_y][center_x]
        rgb_vec = self.image[center_y][center_x]
        return rgb_grad(rgb_vec, one_lower_vec, one_right_vec)

    def local_grad_min(self, center_y, center_x, vicinity=3):
        min = self.rgb_grad(center_y, center_x)
        min_y, min_x = center_y, center_x
        max_y, max_x, _ = self.image.shape

        bounds = vicinity_bounds(center_y, center_x, max_y, max_x, vicinity)
        for y in range(bounds[0][0], bounds[0][1]):
            for x in range(bounds[1][0], bounds[1][1]):
                if center_y == y and center_x == x:
                    # don't compute twice
                    continue
                point_min = self.rgb_grad(y, x)
                if point_min < min:
                    min = point_min
                    min_y, min_x = y, x

        return min_y, min_x

    def get_cluster(self, y, x):
        """
        Gets the cluster associated with point y,x
        Maps from y * x to a Cluster stored in a list
        :param y: 
        :param x: 
        :return: 
        """
        cluster = self.point_clusters[y][x]
        if cluster is not None:
            return cluster

        # If no point cluster has been assigned, use the initial assignment
        # aka, the one closest
        cluster_y = int(y / self.cluster_height)
        cluster_x = int(x / self.cluster_width)
        return self._get_cluster(cluster_y, cluster_x)

    def _get_cluster(self, cluster_y, cluster_x):
        """
        Maps from cluster_y * cluster_x space to the 1D list index
        :param cluster_y: 
        :param cluster_x: 
        :return: 
        """
        return self.clusters[cluster_x + (cluster_y * self.width_sections)]

    def overlay(self):
        """
        :override:
        :return: 
        """
        if self.verbose:
            cprint('Overlaying', 'yellow')

        max_y, max_x = self.point_clusters.shape
        # Draw Averages
        for y in range(max_y):
            for x in range(max_x):
                if self.verbose:
                    cprint_progressbar((y * max_x) + x, max_x * max_y, prefix='Points Overlaid:')
                cluster = self.get_cluster(y, x)
                self.image[y][x] = cluster.get_center_rgb()

        if self.show_borders:
            self.overlay_borders()

    def overlay_borders(self):
        """
        Paint border points black
        Aka points that are 
        :return: 
        """
        if self.verbose:
            cprint('Overlaying borders', 'yellow')

        max_y, max_x = self.point_clusters.shape
        # Draw Borders
        for y in range(1, max_y - 1):
            for x in range(1, max_x - 1):
                if self.verbose:
                    cprint_progressbar((y * (max_x - 2)) + x, max_x * max_y, prefix='Border Points Overlaid:')
                # Check if any surrounding pixels are in another cluster
                # If so --> border
                yx_cluster = self.get_cluster(y, x)
                is_border = False
                for ay in range(y - 1, y + 1):
                    for ax in range(x - 1, x + 1):
                        if yx_cluster != self.get_cluster(ay, ax):
                            is_border = True
                            self.image[y][x] = (0, 0, 0)
                            break
                    # Cut early
                    if is_border:
                        break

    def point_is_in_bounds(self, y, x):
        """
        Check if y,x are inside the bounds of the image
        :param y: 
        :param x: 
        :return: 
        """
        max_y, max_x, _ = self.image.shape
        return y >= 0 and y < max_y and x >= 0 and x < max_x

    def print_info(self):
        """
        :override:
        :return: 
        """
        max_y, max_x, _ = self.image.shape
        super(Slic, self).print_info()
        cprint('Total clusters: ' + str(len(self.clusters)))
        cprint('Cluster Recentering Error Threshold: ' + str(self.stop_under))
        cprint('Cluster Recentering Error Percent: ' + str(self.stop_error))
        cprint('Cluster width x height: %d x %d' % (self.cluster_width, self.cluster_height))
        cprint('Showing borders? ' + ('Yes' if self.show_borders else 'No'))

    def recenter_points(self):
        """
        Recenters each point around the closest center
        Only checks points within 2 * cluster (width | height) away from each cluster
        :return: 
        """
        for i in range(len(self.clusters)):
            if self.verbose:
                cprint_progressbar(i, len(self.clusters), prefix='Points Centered:')

            cluster = self.clusters[i]
            center = cluster.center_vec
            center_y = int(center[0])
            center_x = int(center[1])
            for y in range(center_y - self.cluster_height, center_y + self.cluster_height):
                for x in range(center_x - self.cluster_width, center_x + self.cluster_width):
                    if self.point_is_in_bounds(y, x):
                        point_vec = make_flat_vec(y, x, self.image[y][x])
                        # cluster = self.get_cluster(y, x)
                        dist = slic_vec_distance(point_vec, cluster.center_vec)

                        if dist < self.point_distances[y][x]:
                            self.point_distances[y][x] = dist
                            self.point_clusters[y][x] = cluster

    def process(self):
        """
        :override:
        :return: 
        """
        max_y, max_x, _ = self.image.shape

        if self.verbose:
            print()
            self.print_info()
            print()

        # Apply k-means in the 5D space of x, y, RGB

        max_y, max_x, _ = self.image.shape

        # Find closest centers
        num_centers_changed = self.stop_under + 1
        centering_loop = 0
        # Repeat until all points have found their optimal clusters or residual error is low enough
        while num_centers_changed > self.stop_under:
            if self.verbose:
                centering_loop += 1
                cprint('Recentering loop #' + str(centering_loop), 'yellow')

            self.recenter_points()

            self.reset_cluster_vecs()

            # Recenter clusters
            for y in range(max_y):
                for x in range(max_x):
                    cluster = self.get_cluster(y, x)
                    cluster.add_vec(make_flat_vec(y, x, self.image[y][x]))

            num_centers_changed = self.recenter_clusters()

        if self.verbose:
            cprint('Residual error is low enough', 'green')
            cprint('Centering complete', 'green')

        self.overlay()

        return self.image

    def get_file_prefix(self):
        return 'cw%d-ch%d-se%f' % (self.cluster_width, self.cluster_height, self.stop_error)
