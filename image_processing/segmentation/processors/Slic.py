""" SLIC Processor
"""

from termcolor import cprint

from . import Processor
from ._Cluster import Cluster


class Slic(Processor):
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

    def __init__(self, image, cluster_width=50, cluster_height=50, cli_args=None):
        super(Slic, self).__init__(image, cli_args=cli_args)
        self.cluster_width = cluster_width
        self.cluster_height = cluster_height

    def process(self):
        # Segment cWidth x cHeight
        max_y, max_x = self.image.shape

        if self.verbose:
            print()
            cprint('Info:', 'cyan')
            print('Total points: ' + str(max_x * max_y))


