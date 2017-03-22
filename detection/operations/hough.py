from termcolor import cprint
import numpy as np

from detection.utils import local_maxes_2d
from detection.operations.hessian import detect as feature_detect


def detect(image):
    """
    Todo
    :param image: 
    :return: 
    """
    cprint('TODO: Hough', 'red')

    # Algorithm:
    # Discretize parameter space into bins (accumulator)
    # For each feature point in the image
    #   Put a vote in every bin that could have generated this point
    # Find bins that have the most votes
    # Parameter space will be represented using a polar format

    # Todo: Keep track of which point votes for which bin, then draw line with all points

    max_x, max_y = image.shape
    max_theta = 180
    # rho will never be above x + y
    accumulator = np.ndarray(shape=(max_theta, max_x + max_y))
    # setup identically sized array to record points
    points_in_bins = np.ndarray(shape=(max_theta, max_x + max_y), dtype=object)
    for i in range(points_in_bins.shape[0]):
        for j in range(points_in_bins.shape[1]):
            points_in_bins[i][j] = []

    # Detect feature points with hessian
    cprint('Detecting features', 'yellow')
    feat_img, feat_points = feature_detect(image)

    cprint('Accumulating votes', 'yellow')
    for point in feat_points:
        for theta in range(max_theta):
            rho = int(point[0] * np.cos(theta) + point[1] * np.sin(theta))
            accumulator[theta][rho] += 1
            points_in_bins[theta][rho].append(point)

    # Find local maximums
    cprint('Finding local vote maximums', 'yellow')
    maxes = local_maxes_2d(accumulator)

    return image
