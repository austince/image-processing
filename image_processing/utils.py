""" General utilities used in various operations
"""
import numpy as np
from skimage.draw import line_aa
from termcolor import cprint
import sys
import warnings


def cprint_progressbar(iteration, total, prefix='Progress:', suffix='Complete', decimals=1,
                       length=50, fill='x', color='yellow'):
    """
    A terminal progress bar
    :param iteration: 
    :param total: 
    :param prefix: 
    :param suffix: 
    :param decimals: 
    :param length: 
    :param fill: 
    :param color: 
    :return: 
    """
    if total == 0:
        percent = 1
    else:
        percent = iteration / float(total)

    percent_str = ("{0:." + str(decimals) + "f}").format(100 * percent)
    filled_len = int(length * int(percent))
    bar_str = fill * filled_len + '-' * (length - filled_len)
    cprint('\r%s |%s| %s%% %s' % (prefix, bar_str, percent_str, suffix), end='\r', color=color)
    # Print newline on complete
    if iteration == total:
        print()
        sys.stdout.flush()


def vec_nd_average(vecs):
    if len(vecs) == 0:
        return np.asarray([0])
    dimensions = vecs[0].shape
    vec_sum = np.zeros(shape=dimensions, dtype='int32')

    for v in vecs:
        vec_sum = np.add(vec_sum, v, casting='same_kind')

    return (vec_sum / len(vecs)).astype('int32')


def vec_3d_average(vecs):
    """

    :param vecs: 
    :return: 
    """
    vec_sum = np.zeros(shape=(3,), dtype='int32')

    for v in vecs:
        vec_sum[0] += v[0]
        vec_sum[1] += v[1]
        vec_sum[2] += v[2]

    return (vec_sum / len(vecs)).astype('int32')


def vec_nd_distance(vec1, vec2):
    """

    :param vec1: n dimensional vector
    :param vec2: n dimensional vector
    :return: 
    """
    sum_squares = 0
    for i in range(len(vec1)):
        sum_squares += (np.subtract(vec1[i], vec2[i], casting='same_kind') ** 2)

    return np.sqrt(sum_squares)


def vec_3d_distance(vec1, vec2):
    return np.sqrt(
        (vec1[0] - vec2[0]) ** 2 +
        (vec1[1] - vec2[1]) ** 2 +
        (vec1[2] - vec2[2]) ** 2
    )


def gradient_magnitude(grad):
    """
    Magnitude of a gradient 
    :param grad: 
    :return: 
    """
    return np.sqrt(np.square(grad[0]) + np.square(grad[1]))


def gradient_direction(grad):
    """
    Returns radians
    :param grad: x,y
    :return: radians
    """
    # Division by 0 check
    if grad[0] == 0:
        return 1  # completely vertical, approx arctan of 90 degrees

    return np.arctan(grad[1] / grad[0])


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
    x_bounds, y_bounds = vicinity_bounds_image(point[0], point[1], side_len, image)
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


def vicinity_bounds(y, x, max_y, max_x, vicinity):
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

    return (min_y_range, max_y_range), (min_x_range, max_x_range)


def vicinity_bounds_image(x, y, vicinity, image):
    """
    DEPRECATED
    :param x: 
    :param y: 
    :param vicinity: 
    :param image: f
    :return: 
    """
    warnings.warn("Vicinity bounds are deprecated as x and y are reversed", DeprecationWarning)
    max_x, max_y = image.shape
    return vicinity_bounds(y, x, max_y, max_x, vicinity)


def max_in_vicinity(x, y, image, vicinity):
    """

    :param x: 
    :param y: 
    :param image: 
    :param vicinity: 
    :return: 
    """
    max_val = image[x][y]

    x_bounds, y_bounds = vicinity_bounds_image(x, y, vicinity, image)

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
    :param vicinity: the size of the window to check in
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
