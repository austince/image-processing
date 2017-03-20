import numpy as np
from scipy import misc

from detection.operations.convolution import convolve_replicate_bounds, convolve_replicate_bounds_point

SOBEL_X = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
SOBEL_Y = np.fliplr(SOBEL_X).transpose()


def x_derivative(x, y, image):
    return convolve_replicate_bounds_point(x, y, image, SOBEL_Y)


def y_derivative(x, y, image):
    return convolve_replicate_bounds_point(x, y, image, SOBEL_X)


def gradient(x, y, image):
    dfx = x_derivative(x, y, image)
    dfy = y_derivative(x, y, image)
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


def filter_area(image, area=((0, 3), (0, 3)), kernel=SOBEL_X):
    """
    
    :param image: ndarray
    :param img_area: 
    :param kernel: 
    :return: 
    """
    max_x = image.shape[0]
    max_y = image.shape[1]

    x_start = area[0][0]
    x_end = area[0][1]

    y_start = area[1][0]
    y_end = area[1][1]

    if x_start < 0:
        x_start = 0
    if x_end >= max_x:
        x_end = max_x - 1

    if y_start < 0:
        y_start = 0
    if y_end >= max_y:
        y_end = max_y - 1

    img_area = np.copy(image[
                       x_start:x_end,
                       y_start:y_end
                       ])
    return filter_image(img_area, kernel=kernel)


def filter_image(image, kernel=SOBEL_X):
    """
    Filters in place
    :param image:
    :param kernel:
    :return:
    """

    return convolve_replicate_bounds(image, kernel)
