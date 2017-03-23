""" Testing utilities
"""
from scipy import misc
import os

from tests import results_dir


def load_image(path):
    return misc.imread(path, flatten=True)


def save_result(name, image):
    misc.imsave(os.path.join(results_dir, name), image)
