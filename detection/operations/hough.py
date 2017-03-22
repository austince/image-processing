from termcolor import cprint
import numpy as np
from detection.operations.hessian import detect as feature_detect


def detect(image):
    """
    Todo
    :param image: 
    :return: 
    """
    cprint('TODO: Hough', 'red')

    # Algorithm:
    # Discretize parameter space into bins (accumulator)
    # For each feature point in the image
    #   Put a vote in every bin that could have generated this point
    # Find bins that have the most votes

    # Parameter space will be represented using a polar format

    # rho will never be above x + y
    max_x, max_y = image.shape

    accumulator = np.ndarray(shape=(180, max_x + max_y))
    # Detect feature points with hessian
    cprint('Detecting features', 'yellow')
    feat_img, feat_points = feature_detect(image)

    for point in feat_points:
        for theta in range(180):
            rho = int(point[0] * np.cos(theta) + point[1] * np.sin(theta))
            accumulator[theta][rho] += 1

    # Find local maximums

    return image
