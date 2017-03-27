""" RANSAC Tests
"""
from unittest import TestCase

from image_processing.operations import ransac
from tests import test_images_dict
from tests.utils import load_image_bw, save_result


class TestThreshold(TestCase):
    def test_results_road(self):
        thresh_start = 51000
        thresh_end = 171000
        image = load_image_bw(test_images_dict['road.png'])

        for thresh in range(thresh_start, thresh_end + 1, 10000):
            processed_image = ransac.detect(image.copy(), feature_threshold=thresh)
            save_result('ransac/road-t' + str(thresh) + '.png', processed_image)


class TestInlierThreshold(TestCase):
    def test_results_road(self):
        thresh_start = 1
        thresh_end = 50
        image = load_image_bw(test_images_dict['road.png'])

        for thresh in range(thresh_start, thresh_end + 1, 5):
            processed_image = ransac.detect(image.copy(), inlier_threshold=thresh)
            save_result('ransac/road-inlierThresh' + str(thresh) + '.png', processed_image)

        processed_image = ransac.detect(image.copy())
        save_result('ransac/road-inlierThreshDefault.png', processed_image)


class TestMinAcceptableInliers(TestCase):
    def test_results_road(self):
        thresh = 151000
        image = load_image_bw(test_images_dict['road.png'])
        min_inliers = 2  # has to have at least two points in the line
        max_inliers = 22

        for inliers in range(min_inliers, max_inliers + 1, 3):
            processed_image = ransac.detect(image.copy(), min_inliers=inliers, feature_threshold=thresh)
            save_result('ransac/road-t' + str(thresh) + '-minInliers' + str(inliers) + '.png', processed_image)

