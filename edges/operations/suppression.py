import numpy as np
from edges.operations.sobel import gradient, gradient_magnitude, gradient_direction


def max_in_direction(x, y, direc, image):
    """
    4 approximate possibilities.
    The most brute force way I could do.
    :param x:
    :param y:
    :param direc:
    :param image:
    :return:
    """
    max_x = image.shape[0]
    max_y = image.shape[1]

    if abs(direc) > 0.87:  # Approx 67.5 degrees
        # A more vertical gradient
        # top and bottom
        y_t = max_y - 1 if y + 1 >= max_y else y + 1
        y_b = 0 if y == 0 else y - 1
        max1 = image[x][y_t]
        max2 = image[x][y_b]
    # elif abs(direc) > 0.66:  # Approx 45 degrees
    #     max1 = 1
    #     max2 = 1
    elif abs(direc) > 0.37:  # Approx 22.5 degrees
        if direc < 0:
            # choose (x-1, y+1) and (x+1, y-1)
            xn1 = max_x - 1 if x + 1 >= max_x else x + 1
            yn1 = 0 if y == 0 else y - 1
            xn2 = 0 if x == 0 else x - 1
            yn2 = max_y - 1 if y + 1 >= max_y else y + 1
        else:
            # choose (x-1, y-1) and (x+1, y+1)
            xn1 = 0 if x == 0 else x - 1
            yn1 = 0 if y == 0 else y - 1
            xn2 = max_x - 1 if x + 1 >= max_x else x + 1
            yn2 = max_y - 1 if y + 1 >= max_y else y + 1

        max1 = image[xn1][yn1]
        max2 = image[xn2][yn2]
    else:
        # A more horizontal gradient
        # One left one right
        x_r = max_x - 1 if x + 1 >= max_x else x + 1
        x_l = 0 if x == 0 else x - 1
        max1 = image[x_r][y]
        max2 = image[x_l][y]

    return max(max1, max2)


def non_max_suppress_point(x, y, image, original, threshold):
    """
    In place suppression
    :param x:
    :param y:
    :param image:
    :param original:
    :param threshold:
    :return:
    """
    max_x = image.shape[0]
    max_y = image.shape[1]

    # Take gradient from original, NOT IMAGE BEING SUPPRESSED
    grad = gradient(x, y, original)
    if gradient_magnitude(grad) < threshold:
        # mark as 0
        image[x][y] = 0
    else:
        # process direction to make sure its a local max
        direc = gradient_direction(grad)

        # Normalize direction so the angle is always below 90

        if abs(direc) > 0.97:  # Approx 85 degrees
            # vertical, check one to left and one to right
            x_r = max_x - 1 if x + 1 >= max_x else x + 1
            x_l = 0 if x == 0 else x - 1
            if original[x][y] < original[x_r][y] or original[x][y] < original[x_l][y]:
                # Suppress if its not a local max
                image[x][y] = 0
        elif abs(direc) > 0.05:
            # Under 0.05 is approximately horizontal
            # Here is where we would bilinear interpolate
            if original[x][y] < max_in_direction(x, y, direc, original):
                image[x][y] = 0
        else:
            # horizontal, check one to top and bottom
            y_t = max_y - 1 if y + 1 >= max_y else y + 1
            y_b = 0 if y == 0 else y - 1
            if original[x][y] < original[x][y_t] or original[x][y] < original[x][y_b]:
                # Suppress if its not a local max
                image[x][y] = 0


def non_max_suppress(image, threshold=0.4):
    """
    Suppress Non Max Edges
    :param image:
    :param threshold:
    :return:
    """

    max_x = image.shape[0]
    max_y = image.shape[1]

    # Make a copy so we can suppress in place
    suppressed = image.copy()

    for x in range(0, max_x):
        for y in range(0, max_y):
            non_max_suppress_point(x, y, suppressed, image, threshold)

    return suppressed
