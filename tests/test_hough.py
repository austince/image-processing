""" Hough Transform Tests
"""
from unittest import TestCase

from detection.operations import hough
from tests import test_images_dict
from tests.utils import load_image, save_result


class TestThreshold(TestCase):
    def test_results_road(self):
        thresh_start = 51000
        thresh_end = 171000
        image = load_image(test_images_dict['road.png'])

        for thresh in range(thresh_start, thresh_end + 1, 10000):
            processed_image = hough.detect(image.copy(), feature_threshold=thresh)
            save_result('hough/road-t' + str(thresh) + '.png', processed_image)
