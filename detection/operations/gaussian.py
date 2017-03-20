
import numpy as np

from detection.operations.convolution import convolve_replicate_bounds


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

    k_sum = np.sum(kernel)
    if k_sum != 1:
        # Normalize the gaussian filter to sum to 1
        kernel = np.divide(kernel, k_sum)

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
    # if k_sum != 0:
    #   # Normalize the gaussian filter to sum to 0
    #   kernel = np.divide(kernel, k_sum)
    return kernel


def filter_image(image, sigma, scale=None):
    """
    Filters in place
    :param image:
    :param sigma:
    :param scale:
    :return:
    """
    if scale is None:
        # 3 * sigma per half width
        scale = 6 * sigma - 1

    kernel = build_gaussian_kernel(sigma, scale)
    # Apply both kernels to the input image
    filtered = convolve_replicate_bounds(image, kernel)
    # filtered = convolve_replicate_bounds(filtered, kernel_y)
    return filtered
