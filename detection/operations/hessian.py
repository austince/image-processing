from termcolor import cprint
import numpy as np
from scipy import misc

from detection.operations import gaussian
from detection.operations import sobel


def max_in_vicinity(x, y, arr, vicinity):
    """
    
    :param x: 
    :param y: 
    :param arr: 
    :param vicinity: 
    :return: 
    """
    max_val = arr[x][y]
    max_x, max_y = arr.shape
    v_len = int(vicinity / 2)

    min_x_range = x - v_len
    if min_x_range < 0:
        min_x_range = 0

    max_x_range = x + v_len + 1
    if max_x_range >= max_x:
        max_x_range = max_x - 1

    min_y_range = y - v_len
    if min_y_range < 0:
        min_y_range = 0

    max_y_range = y + v_len + 1
    if max_y_range >= max_y:
        max_y_range = max_y - 1

    for arr_x in range(min_x_range, max_x_range):
        for arr_y in range(min_y_range, max_y_range):
            max_val = max(arr[arr_x][arr_y], max_val)

    return max_val


def hessian_suppress(image, determinates, vicinity):

    max_x, max_y = image.shape

    for x in range(0, max_x):
        for y in range(0, max_y):
            if determinates[x][y] >= max_in_vicinity(x, y, determinates, vicinity) \
                    and determinates[x][y] != 0:
                image[x][y] = 1
            else:
                image[x][y] = 0


def detect(image, threshold=1000, gaus_sig=1, vicinity=3):
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
    ixy_filtered = sobel.filter_image(ix_filtered, kernel=sobel.SOBEL_X)
    iyy_filtered = sobel.filter_image(iy_filtered, kernel=sobel.SOBEL_X)

    cprint('Finding determinants', 'yellow')
    # ixx * iyy - ixy ^ 2
    determinants = ixx_filtered * iyy_filtered - (ixy_filtered ** 2)
    # assert determinants == np.linalg.det()

    cprint('Thresholding determinants', 'yellow')
    max_x, max_y = determinants.shape
    for x in range(0, max_x):
        for y in range(0, max_y):
            if determinants[x][y] < threshold:
                determinants[x][y] = 0

    # Non max suppress each point in the threshold-ed image
    cprint('Non-max suppressing', 'yellow')
    hessian_suppress(image, determinants, vicinity)

    features = []
    for x in range(0, max_x):
        for y in range(0, max_y):
            if image[x][y] == 1:
                features.append((x, y))

    # Also return a list of x,y points that are the 'features'

    return image, features


