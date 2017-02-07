
from math import floor


def convolve_replicate_bounds_coord(x, y, image, kernel, constant=1):
    """

    :param x:
    :param y:
    :param image:
    :param kernel:
    :param constant:
    :return:
    """
    max_x = image.shape[0] - 1
    max_y = image.shape[1] - 1
    k_max_x = floor(kernel.shape[0] / 2)
    k_max_y = floor(kernel.shape[1] / 2)

    sum = 0

    for k_x in range(-k_max_x, k_max_x + 1):
        for k_y in range(-k_max_y, k_max_y + 1):
            adj_x = k_x + x
            adj_y = k_y + y

            if adj_x < 0:
                adj_x = 0
            elif adj_x > max_x:
                adj_x = max_x

            if adj_y < 0:
                adj_y = 0
            elif adj_y > max_y:
                adj_y = max_y

            sum += kernel[k_x + k_max_x][k_y + k_max_y] * image[adj_x][adj_y]

    return sum * constant


def convolve_replicate_bounds(image, kernel, constant=1):
    """
    convolved[x][y]

    :param image:
    :param kernel:
    :param constant:
    :return:
    """
    max_x = image.shape[0]
    max_y = image.shape[1]
    convolved = image.copy()

    for x in range(0, max_x):
        for y in range(0, max_y):
            convolved[x][y] = convolve_replicate_bounds_coord(x, y, image, kernel, constant)

    return convolved
