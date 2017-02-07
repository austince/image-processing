
import numpy as np

from edges.operations import convolve_replicate_bounds


def build_gaussian_kernel(sigma, scale):
    """
    Builds
    :param sigma:
    :param scale:
    :return:
    """
    kernel = np.zeros((scale, scale))
    k_len_max = int(scale / 2)
    two_sigma_sq = 2.0 * np.power(sigma, 2)
    one_over_two_pi_sigma_sq = 1.0 / (two_sigma_sq * np.pi)

    for x in range(-k_len_max, k_len_max + 1):
        x_sq = np.power(x, 2)
        for y in range(-k_len_max, k_len_max + 1):
            y_sq = np.power(y, 2)
            power = -1 * (x_sq + y_sq) / two_sigma_sq
            kernel[x + k_len_max][y + k_len_max] = np.exp(power) * one_over_two_pi_sigma_sq

    # Derivative
    # two_sigma_sq = 2 * np.power(sigma, 2)
    # for x in range(-k_len_max, k_len_max):
    #     x_sq = np.power(x, 2)
    #     for y in range(-k_len_max, k_len_max):
    #         y_sq = np.power(y, 2)
    #         power = -1 * (x_sq + y_sq) / two_sigma_sq
    #         kernel[x][y] = np.exp(power)
    #         if axis == 'x':
    #             kernel[x][y] *= x
    #         else:
    #             kernel[x][y] *= y
    sum = np.sum(kernel)
    if sum != 0:
        # Normalize the gaussian filter to sum to 1
        kernel = np.divide(kernel, sum)

    return kernel


def filter_image(image, sigma, scale=5):
    """
    Filters in place
    :param image:
    :param sigma:
    :param scale:
    :return:
    """
    kernel = build_gaussian_kernel(sigma, scale)
    # Apply both kernels to the input image
    filtered = convolve_replicate_bounds(image, kernel)
    # filtered = convolve_replicate_bounds(filtered, kernel_y)
    return filtered
