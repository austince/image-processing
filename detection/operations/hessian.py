from enum import Enum
from termcolor import cprint
import numpy as np
from scipy import misc

from detection.operations import gaussian
from detection.operations import sobel


def max_in_vicinity(x, y, arr, vicinity):
    max_val = arr[x][y]
    max_x, max_y = arr.shape
    v_len = int(vicinity / 2)
    for arr_x in range(x - v_len, x + v_len + 1):
        for arr_y in range(y - v_len, y + v_len + 1):
            if arr_x < 0:
                arr_x = 0
            elif arr_x >= max_x:
                arr_x = max_x - 1

            if arr_y < 0:
                arr_y = 0
            elif arr_y >= max_y:
                arr_y = max_y - 1

            max_val = max(arr[arr_x][arr_y], max_val)

    return max_val


def hessian_suppress(image, determinates, vicinity):

    max_x, max_y = image.shape

    for x in range(0, max_x):
        for y in range(0, max_y):
            if determinates[x][y] >= max_in_vicinity(x, y, determinates, vicinity):
                image[x][y] = 1
            else:
                image[x][y] = 0


def detect(image, threshold=-15000, gaus_sig=3, vicinity=3):
    """
    Apply Gaussian Filter first
    Use Sobel filters as derivative operators
    Threshold the determinant of the Hessian
    Apply non-maximum suppression in 3 x 3 neighborhoods
    
    Hessian(I) = [ Ixx Ixy] 
                 [Ixy Iyy] 
    
    :param image: 
    :param threshold:
    :param gaus_sig:
    :param vicinity:
    :return: 
    """

    # Make a copy so we don't lose the original
    cprint('First appying Gaussian', 'yellow')
    gaussian.filter_image(image, gaus_sig)

    cprint('Finding First derivatives', 'yellow')
    # Use inverse filters because everything is in y,x format lol oops
    ix_filtered = sobel.filter_image(image, kernel=sobel.SOBEL_Y)
    iy_filtered = sobel.filter_image(image, kernel=sobel.SOBEL_X)
    cprint('Finding Second derivatives', 'yellow')
    ixx_filtered = sobel.filter_image(ix_filtered, kernel=sobel.SOBEL_Y)
    ixy_filtered = sobel.filter_image(ix_filtered, kernel=sobel.SOBEL_Y)
    iyy_filtered = sobel.filter_image(iy_filtered, kernel=sobel.SOBEL_X)

    cprint('Finding determinants', 'yellow')
    determinants = ixx_filtered * iyy_filtered - (ixy_filtered ** 2)

    cprint('Thresholding determinants', 'yellow')
    max_x, max_y = determinants.shape
    for x in range(0, max_x):
        for y in range(0, max_y):
            if determinants[x][y] < threshold:
                determinants[x][y] = 0

    # Non max suppress each point in the threshold-ed image
    cprint('Non-max suppressing', 'yellow')
    hessian_suppress(image, determinants, vicinity)

    # for x in range(0, max_x):
    #     for y in range(0, max_y):
    #         pass

    return image
