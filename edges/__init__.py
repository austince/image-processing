__version__ = "1.0.0"

from scipy import misc
from termcolor import colored
from edges.operations import gaussian, sobel


def detect(image_path, g_sig=1):
    """
    Steps:
    0. Load image from path
    1. Gaussian filter
    2. Gradient computation using Sobel filters
    3. Non-maximum suppression
    :param image_path:
    :param g_sig: gaussian sigma
    :return:
    """
    try:
        image = misc.imread(image_path)
    except FileNotFoundError:
        raise FileNotFoundError("Can't load image file: " + str(image_path))

    filtered = gaussian.filter_image(image, g_sig)
    filtered = sobel.filter_image(filtered)
    return filtered
