""" K-Means Tests
"""
from unittest import TestCase

from image_processing.segmentation.processors import *
from tests.utils import load_image_color, save_result


class TestGeneral(TestCase):
    def test_results_white_tower(self):
        image = load_image_color('white-tower.png')
        for k in range(4, 10, 2):
            processor = Kmeans(image.copy())
            processed_image = processor.process()
            save_result('kmeans/' + processor.get_file_prefix() + '.white-tower.png', processed_image)


