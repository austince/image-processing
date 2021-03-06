""" Hessian Feature Detection
"""
from termcolor import cprint
import numpy as np
from scipy import misc

from image_processing.utils import max_in_vicinity
from image_processing.operations import gaussian
from image_processing.operations import sobel


def hessian_suppress(image, determinants, vicinity):
    """
    
    :param image: 
    :param determinants: 
    :param vicinity: 
    :return: 
    """

    max_x, max_y = image.shape
    # v_len = int(vicinity / 2)
    # for x in range(v_len, max_x - v_len):
    #     for y in range(v_len, max_y - v_len):

    for x in range(0, max_x):
        for y in range(0, max_y):
            if determinants[x][y] >= max_in_vicinity(x, y, determinants, vicinity) \
                    and determinants[x][y] != 0:
                image[x][y] = 1
            else:
                image[x][y] = 0


def detect(image, threshold=125000, gaus_sig=1, vicinity=3):
    """
    Apply Gaussian Filter first
    Use Sobel filters as derivative operators
    Threshold the determinant of the Hessian
    Apply non-maximum suppression in 3 x 3 neighborhoods / vicinity
    
    Hessian(I) = [Ixx Ixy] 
                 [Ixy Iyy] 
    
    :param image: 
    :param threshold:
    :param gaus_sig:
    :param vicinity:
    :return: 
    """
    if threshold is None:
        threshold = 125000

    # Make a copy so we don't lose the original
    cprint('Applying Gaussian', 'yellow')
    gaussian.filter_image(image, gaus_sig)

    cprint('Finding First derivatives', 'yellow')
    image_ix = sobel.x_derivative(image)
    image_iy = sobel.y_derivative(image)
    cprint('Finding Second derivatives', 'yellow')
    image_ixx = sobel.x_derivative(image_ix)
    image_ixy = sobel.y_derivative(image_ix)
    image_iyy = sobel.y_derivative(image_iy)

    cprint('Finding determinants', 'yellow')
    # ixx * iyy - ixy ^ 2
    determinants = image_ixx * image_iyy - (image_ixy ** 2)
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


