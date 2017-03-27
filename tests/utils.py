""" Testing utilities
"""
from scipy import misc
import os

from tests import results_dir, test_images_dict


def load_image_bw(im_name):
    return misc.imread(test_images_dict[im_name], flatten=True)


def load_image_color(im_name):
    return misc.imread(test_images_dict[im_name])


def save_result(name, image):
    misc.imsave(os.path.join(results_dir, name), image)
