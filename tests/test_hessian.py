""" Hessian Tests
"""
from unittest import TestCase

from detection.operations import hessian
from tests import test_images_dict
from tests.utils import load_image, save_result


class TestThreshold(TestCase):
    def test_results_road(self):
        thresh_start = 1000
        thresh_end = 71000
        image = load_image(test_images_dict['road.png'])

        for thresh in range(thresh_start, thresh_end + 1, 10000):
            feat_image, _ = hessian.detect(image.copy(), threshold=thresh)
            save_result('hessian/road-t' + str(thresh) + '.png', feat_image)
