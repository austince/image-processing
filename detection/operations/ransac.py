""" RANSAC line detection
"""
from termcolor import cprint
import numpy as np
from scipy import stats

from detection.operations.hessian import detect as feature_detect
from detection.utils import subsample, plot_line, plot_square, most_extreme_points
from detection.utils import distance_between_points
from detection.operations import gaussian


def distance_to_model(a, b, c, point):
    numer = np.abs(a * point[0] + b * point[1] + c)
    denom = np.sqrt(a ** 2 + b ** 2)
    return numer / denom


def linReg(points):
    """
    
    :param points: 
    :return: 
    """
    xs = np.matrix([[x, 1] for (x, _) in points])
    ys = np.matrix([[y] for (_, y) in points])

    bs = np.linalg.inv(xs.transpose() * xs) * xs.transpose() * ys

    return bs[0].item(), bs[1].item()


def fitline(points):
    """
    
    :param points: 
    :return: 
    """
    linReg(points)
    p1 = points[0]
    p2 = points[1]
    # mx + b = y
    # m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    # b = p1[1] - m * p1[0]

    # ax + by + c = 0
    a = p1[1] - p2[1]
    b = p1[0] - p2[0]
    c = (p1[0] * p2[1]) - (p2[0] * p1[1])

    def distance_to(point):
        return distance_to_model(a, b, c, point)

    coeffs = a, b, c
    return distance_to, coeffs


def total_error(coeffs, points):
    """
    Total least squares error of a set of points to a model
    :param coeffs: 
    :param points: 
    :return: 
    """
    error = 0
    a, b, c = coeffs
    for point in points:
        error += (a * point[0] + b * point[1] + c) ** 2

    return error


def find_inliers(dist_to_model_func, threshold, features):
    inliers = []
    for point in features:
        if dist_to_model_func(point) < threshold:
            inliers.append(point)

    return inliers


def plot_inlier_lines(lines, image, max_to_plot=4, inlier_sq_size=3):
    """
    Find two extreme points in the line and plot a connecting segment in the image
    :param lines: 
    :param image: 
    :param max_to_plot:
    :param inlier_sq_size:
    :return: 
    """

    for line_index in range(max_to_plot):
        for point in lines[line_index]:
            plot_square(point, inlier_sq_size, image)

        start, end = most_extreme_points(lines[line_index])
        if start is not None and end is not None:
            plot_line(start, end, image)


def detect(image, subsample_size=2, gaus_sig=1):
    """
    
    :param image: 
    :param subsample_size: 
    :param num_sample_runs: 
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
    # Also could run error regression on each model + inliers to determine best fit
    # Todo: accurate calculation of line distance

    # Where expected proportion of outliers 'e' is .5
    # where probability of at least one sample free of outliers 'p' is .999
    num_sample_runs = int(np.log(.001) / np.log(1 - (.5 ** subsample_size)))
    threshold = np.sqrt(3.84 * gaus_sig ** 2)
    # Min number of inliers to be considered a line
    min_acceptable_inliers = 4

    cprint('Detecting features', 'yellow')
    feat_img, feat_points = feature_detect(image.copy(), gaus_sig=gaus_sig)
    subsets = []
    inlier_lines = []
    inlier_errors = []

    # Randomly choose
    cprint('Fitting models', 'yellow')
    for run in range(num_sample_runs):
        subset = None
        # Make sure not to pick the same subset twice
        # todo: not inverse-invariant
        while subset is None or subset in subsets:
            subset = subsample(feat_points, subsample_size)

        model_distance_to, model_coeffs = fitline(subset)
        inliers = find_inliers(model_distance_to, threshold, feat_points)

        # add to inlier_lines
        if len(inliers) >= min_acceptable_inliers:
            inlier_lines.append(inliers)
            # linear regression and Error checking,
            inlier_errors.append(total_error(model_coeffs, inliers))

    # Find the lines with the best support
    # Sort by minimal total error
    inlier_lines = [line for (line, err) in sorted(zip(inlier_lines, inlier_errors))]
    cprint('Plotting lines and inliers', 'yellow')
    plot_inlier_lines(inlier_lines, image)
    return image
