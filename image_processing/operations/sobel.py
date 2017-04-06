"""
 Sobel Gradient Filtering
 
 NOTE: Have been treating x, y incorrectly with numpy this whole time
 They should be reversed. Everywhere. Todo.
"""
import numpy as np

from image_processing.operations.convolution import convolve_replicate_bounds, convolve_replicate_bounds_point

SOBEL_X = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
SOBEL_Y = np.fliplr(SOBEL_X).transpose()


def point_x_derivative(x, y, image):
    return convolve_replicate_bounds_point(x, y, image, SOBEL_Y)


def point_y_derivative(x, y, image):
    return convolve_replicate_bounds_point(x, y, image, SOBEL_X)


def x_derivative(image):
    """
    Image's derivative in the x direction
    :param image: 
    :return: 
    """
    return filter_image(image, SOBEL_Y)


def y_derivative(image):
    """
    Image's derivative in the y direction
    :param image: 
    :return: 
    """
    return filter_image(image, SOBEL_X)


def point_gradient(x, y, image):
    """
    X Y 
    :param x: 
    :param y: 
    :param image: 
    :return: 
    """
    dfx = point_x_derivative(x, y, image)
    dfy = point_y_derivative(x, y, image)
    return np.array([dfx, dfy])


def filter_image(image, kernel=SOBEL_X):
    """
    Filters in place
    :param image:
    :param kernel:
    :return:
    """

    return convolve_replicate_bounds(image, kernel)
