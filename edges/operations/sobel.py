import numpy as np
from edges.operations import convolve_replicate_bounds, convolve_replicate_bounds_coord

SOBEL_X = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
SOBEL_Y = np.fliplr(SOBEL_X).transpose()


def gradient(x, y, image):
    dfx = convolve_replicate_bounds_coord(x, y, image, SOBEL_X)
    dfy = convolve_replicate_bounds_coord(x, y, image, SOBEL_Y)
    return np.array([dfx, dfy])


def gradient_magnitude(grad):
    return np.sqrt((grad[0] * grad[0]) + (grad[1] * grad[1]))


def gradient_direction(grad):
    # Division by 0 check
    if grad[0] == 0:
        return 1  # completely vertical

    return np.arctan(grad[1] / grad[0])


def suppress(x, y, image, threshold):
    grad = gradient(x, y, image)
    if gradient_magnitude(grad) < threshold:
        # mark as 0
        image[x][y] = 0
    else:
        # process direction
        # Todo
        dir = gradient_direction(grad)
        if abs(dir) > 0.46:  # Approx 45 degrees
            # vertical
            pass
        else:
            # horizontal
            pass


def max_suppress(image, threshold=0.4):
    """
    Suppress Non Max Edges
    :param image:
    :param threshold:
    :return:
    """

    max_x = image.shape[0]
    max_y = image.shape[1]

    filtered = image

    for x in range(0, max_x + 1):
        for y in range(0, max_y + 1):
            suppress(x, y, image, threshold)

    return filtered


def filter_image(image, kernel=SOBEL_X):
    """
    Filters in place
    :param image:
    :param kernel:
    :return:
    """

    return convolve_replicate_bounds(image, kernel)
