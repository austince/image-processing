""" General utilities used in various operations
"""
import numpy as np
from skimage.draw import line_aa
from termcolor import cprint


def cprint_progressbar(iteration, total, prefix='Progress:', suffix='Complete', decimals=1, length=50, fill='x', color='yellow'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * iteration / float(total))
    filled_len = int(length * iteration // total)
    bar = fill * filled_len + '-' * (length - filled_len)
    cprint('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r', color=color)
    # Print newline on complete
    if iteration == total:
        print()


def subsample(sample, sub_size):
    """
    Choose sub_size unique random elements from a larger sample list
    :param sample: 
    :param sub_size: 
    :return: 
    """
    sub = []
    for s in range(sub_size):
        elem = None
        while elem is None or elem in sub:
            elem = sample[int(len(sample) * np.random.random())]
        sub.append(elem)

    return sub


def plot_line(start_point, end_point, image):
    """
    Draws a line onto an image
    :param start_point:
    :param end_point:
    :param image: 
    :return: 
    """
    rr, cc, val = line_aa(start_point[0], start_point[1], end_point[0], end_point[1])
    image[rr, cc] = 1


def plot_square(point, side_len, image):
    """
    
    :param point: x, y tuple
    :param side_len: 
    :param image: 
    :return: 
    """
    x_bounds, y_bounds = vicinity_bounds(point[0], point[1], side_len, image)
    for x in range(x_bounds[0], x_bounds[1]):
        for y in range(y_bounds[0], y_bounds[1]):
            image[x][y] = 1


def distance_between_points(point1, point2):
    """
    distance formula
    :param point1: 
    :param point2: 
    :return: 
    """
    return np.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))


def most_extreme_points(line):
    """
    Gets the two points that are furthest apart
    :param line: 
    :return: 
    """
    max_distance = 0
    start_point = None
    end_point = None

    for point1 in line:
        for point2 in line:
            distance = distance_between_points(point1, point2)
            if distance > max_distance:
                start_point = point1
                end_point = point2
                max_distance = distance

    return start_point, end_point


def vicinity_bounds(x, y, vicinity, image):
    max_x, max_y = image.shape
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

    return (min_x_range, max_x_range), (min_y_range, max_y_range)


def max_in_vicinity(x, y, image, vicinity):
    """

    :param x: 
    :param y: 
    :param image: 
    :param vicinity: 
    :return: 
    """
    max_val = image[x][y]

    x_bounds, y_bounds = vicinity_bounds(x, y, vicinity, image)

    for arr_x in range(x_bounds[0], x_bounds[1]):
        for arr_y in range(y_bounds[0], y_bounds[1]):
            max_val = max(image[arr_x][arr_y], max_val)

    return max_val


def is_max_in_vicinity(x, y, image, vicinity):
    return image[x][y] >= max_in_vicinity(x, y, image, vicinity)


def local_maxes_2d(arr, vicinity=3):
    """
    Finds coordinates of local maximums
    Sorts by max value
    :param arr: 2d array
    :return: 
    """
    maxes = []

    x_max, y_max = arr.shape

    for x in range(x_max):
        for y in range(y_max):
            if is_max_in_vicinity(x, y, arr, vicinity):
                maxes.append((x, y))

    maxes.sort(key=
               lambda point:
               arr[point[0], point[1]],
               reverse=True
               )

    return maxes


def bw_to_rgb(image):
    """
    :see: http://www.socouldanyone.com/2013/03/converting-grayscale-to-rgb-with-numpy.html
    :param image: 
    :return: 
    """
    w, h = image.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = image
    ret[:, :, 1] = ret[:, :, 2] = ret[:, :, 0]
    return ret