import numpy as np


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
