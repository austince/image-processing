""" Canny Edge Detection
"""
from scipy import misc
from termcolor import cprint
from image_processing.operations import gaussian, sobel, suppression


def detect(image, g_sig=1, threshold=100):
    """
    Steps:
    0. Load image from path
    1. Gaussian filter
    2. Gradient computation using Sobel filters
    3. Non-maximum suppression
    :param image:
    :param g_sig: gaussian sigma
    :param threshold:
    :return:
    """

    filtered = gaussian.filter_image(image, g_sig)
    filtered = suppression.non_max_suppress(filtered, threshold)
    return filtered
