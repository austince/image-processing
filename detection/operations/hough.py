""" Hough Transform
"""
from termcolor import cprint
import numpy as np

from detection.operations.utils import local_maxes_2d, plot_square, plot_line, most_extreme_points
from detection.operations.hessian import detect as feature_detect


def plot_best_lines(maxes, points_in_bins, image, max_to_plot=4, inlier_sq_size=3):
    for line_index in range(max_to_plot):
        line = points_in_bins[maxes[line_index]]

        for point in line:
            plot_square(point, inlier_sq_size, image)

        start, end = most_extreme_points(line)
        if start is not None and end is not None:
            plot_line(start, end, image)


def detect(image, feature_threshold=None, gaus_sig=1):
    """
    
    :param image:
    :param feature_threshold:
    :param gaus_sig:
    :return: 
    """

    # Algorithm:
    # Discretize parameter space into bins (accumulator)
    # For each feature point in the image
    #   Put a vote in every bin that could have generated this point
    # Find bins that have the most votes
    # Parameter space will be represented using a polar format

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
    feat_img, feat_points = feature_detect(image.copy(), threshold=feature_threshold, gaus_sig=gaus_sig)

    cprint('Accumulating votes', 'yellow')
    for point in feat_points:
        for theta in range(max_theta):
            rho = int(point[0] * np.cos(theta) + point[1] * np.sin(theta))
            accumulator[theta][rho] += 1
            points_in_bins[theta][rho].append(point)

    # Find local maximums
    cprint('Finding local vote maximums', 'yellow')
    maxes = local_maxes_2d(accumulator)
    # Todo: try max just by accumulated value
    plot_best_lines(maxes, points_in_bins, image)

    return image
