import numpy as np
from edges.operations.convolution import convolve_replicate_bounds, convolve_replicate_bounds_point

SOBEL_X = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
SOBEL_Y = np.fliplr(SOBEL_X).transpose()


def gradient(x, y, image):
    dfx = convolve_replicate_bounds_point(x, y, image, SOBEL_Y)
    dfy = convolve_replicate_bounds_point(x, y, image, SOBEL_X)
    return np.array([dfx, dfy])


def gradient_magnitude(grad):
    return np.sqrt(np.square(grad[0]) + np.square(grad[1]))


def gradient_direction(grad):
    """
    Returns radians
    :param grad:
    :return: radians
    """
    # Division by 0 check
    if grad[0] == 0:
        return 1  # completely vertical, approx arctan of 90 degrees

    return np.arctan(grad[1] / grad[0])


def filter_image(image, kernel=SOBEL_X):
    """
    Filters in place
    :param image:
    :param kernel:
    :return:
    """

    return convolve_replicate_bounds(image, kernel)
