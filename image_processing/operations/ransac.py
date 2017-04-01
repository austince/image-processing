""" RANSAC line detection
"""
from termcolor import cprint
import numpy as np
from scipy import stats

from image_processing.operations.hessian import detect as feature_detect
from image_processing.utils import subsample, plot_line, plot_square, most_extreme_points


def distance_to_model(a, b, c, point):
    numer = np.abs(a * point[0] + b * point[1] + c)
    denom = np.sqrt(a ** 2 + b ** 2)
    return numer / denom


def fitline_many_points(points):
    """ More robust line fitting for many points
    
    :param points: 
    :return: m, b tuple
    """
    # Split into xs and ys
    xs = np.matrix([[x, 1] for (x, _) in points])
    ys = np.matrix([[y] for (_, y) in points])

    try:
        bs = np.linalg.inv(xs.transpose() * xs) * xs.transpose() * ys
    except np.linalg.linalg.LinAlgError:
        # Do the ol' 2 point fit if there's an error
        return fitline(points)

    m, b_inter = bs[0].item(), bs[1].item()

    a = -m
    b = 1
    c = -b_inter

    def distance_to(point):
        return distance_to_model(a, b, c, point)

    coeffs = a, b, c
    return distance_to, coeffs


def fitline(points):
    """ More efficient for just two points
    
    :param points: 
    :return: 
    """
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


def detect(image, subsample_size=2, num_best=4, min_inliers=7, inlier_threshold=None, feature_threshold=None, gaus_sig=1):
    """
    
    :param image: 
    :param subsample_size: 
    :param num_best:
    :param min_inliers: 
    :param inlier_threshold:
    :param feature_threshold:
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
    # Also could run error regression on each model + inliers to determine best fit: Done!

    # Where expected proportion of outliers 'e' is .75
    # where probability of at least one sample free of outliers 'p' is .999
    num_sample_runs = int(np.log(.001) / np.log(1 - (.25 ** subsample_size)))

    if inlier_threshold is None:
        inlier_threshold = np.sqrt(3.84 * gaus_sig ** 2)

    cprint('Detecting features', 'yellow')
    feat_img, feat_points = feature_detect(image.copy(), threshold=feature_threshold, gaus_sig=gaus_sig)
    best_inlier_lines = []
    best_subsets = []

    cprint('Fitting models', 'yellow')
    for best_run in range(num_best):
        subsets = []
        inlier_lines = []
        inlier_errors = []

        # Run for a sample
        for run in range(num_sample_runs):
            # Randomly choose
            subset = None
            # Make sure not to pick the same subset twice
            # todo: not inverse-invariant
            while subset is None or subset in subsets or subset in best_subsets:
                subset = subsample(feat_points, subsample_size)

            subsets.append(subset)

            distance_to_model_func, _ = fitline(subset)
            inliers = find_inliers(distance_to_model_func, inlier_threshold, feat_points)

            # add to inlier_lines
            if len(inliers) >= min_inliers:
                inlier_lines.append(inliers)
                # Refit using all inliers
                _, model_coeffs = fitline_many_points(inliers)
                # linear regression and Error checking,
                inlier_errors.append(total_error(model_coeffs, inliers))

        # Find the lines with the best support
        # Sort by minimal total error
        # inlier_lines.sort(key=len)
        # inlier_lines = [line for (line, err) in sorted(zip(inlier_lines, inlier_errors))]
        # Choose the best, remove it and rerun
        if len(inlier_lines) > 0:
            min_err_index = inlier_errors.index(min(inlier_errors))
            best_inlier_lines.append(inlier_lines[min_err_index])
            best_subsets.append(subsets[min_err_index])

    cprint('Plotting lines and inliers', 'yellow')
    plot_inlier_lines(best_inlier_lines, image)
    return image
