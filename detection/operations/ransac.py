from termcolor import cprint
import numpy as np

from detection.operations.hessian import detect as feature_detect
from detection.utils import subsample, plot_line, plot_square, most_extreme_points
from detection.operations import gaussian


def fitline(points):
    p1 = points[0]
    p2 = points[1]
    # mx + b = y
    # m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    # b = p1[1] - m * p1[0]

    # ax + by = d
    a = p1[1] - p2[1]
    b = p1[0] - p2[0]
    d = - ((p1[0] * p2[1]) - (p2[0] * p1[1]))

    model = lambda x, y: a * x + b * y - d
    return model


def find_inliers(model, threshold, features):
    inliers = []
    for point in features:
        # Total least squares TODO
        if model(point[0], point[1]) ** 2 < threshold:
            inliers.append(point)

    return inliers


def plot_inlier_lines(lines, image, max_to_plot=4, inlier_sq_size=3):
    """
    Find two extreme points in the line and plot a connecting segment in the image
    :param lines: 
    :param image: 
    :param line_color:
    :return: 
    """

    # Find the lines with the best support
    # More inliers is more support?
    lines.sort(key=len, reverse=True)

    for line_index in range(max_to_plot):
        for point in lines[line_index]:
            plot_square(point, inlier_sq_size, image)

        start, end = most_extreme_points(lines[line_index])
        if start is not None and end is not None:
            plot_line(start, end, image)


def detect(image, subsample_size=2, num_runs=100, gaus_sig=1):
    """
    
    :param image: 
    :param subsample_size: 
    :param num_runs: 
    :param gaus_sig: 
    :return: 
    """
    # Algorithm:
    # Choose a small subset of points uniformly at random
    # Fit a model to that subset
    # Find all remaining points that are 'close' to the model
    # If there are more than a certain number of inliers
    #   Refit using all the new inliers
    # Reject the rest as outliers
    # Repeat and choose the best model

    # Notes
    # could run iteratively and only pull top contender each time, then remove
    # Todo: accurate calculation of line distance


    threshold = np.sqrt(3.84 * gaus_sig ** 2)

    cprint('Detecting features', 'yellow')
    feat_img, feat_points = feature_detect(image.copy(), gaus_sig=gaus_sig)
    subsets = []
    inlier_lines = []

    # Randomly choose
    cprint('Fitting models', 'yellow')
    for run in range(num_runs):
        subset = None
        # Make sure not to pick the same subset twice
        while subset is None or subset in subsets:
            subset = subsample(feat_points, subsample_size)

        model = fitline(subset)
        inliers = find_inliers(model, threshold, feat_points)

        # If more that 'd' inliers, add to inlier_lines
        inlier_lines.append(inliers)

    plot_inlier_lines(inlier_lines, image)
    return image
