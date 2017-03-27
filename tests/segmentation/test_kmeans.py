""" K-Means Tests
"""
from unittest import TestCase

from image_processing.segmentation.processors import *
from tests.utils import load_image_color, save_result


class TestGeneral(TestCase):
    def test_results_white_tower(self):
        image = load_image_color('white-tower.png')
        processor = Kmeans(image.copy())
        processed_image = processor.process()
        save_result('kmeans/white-tower.png', processed_image)


