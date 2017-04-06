""" SLIC Tests
"""
from unittest import TestCase
from os import path
from image_processing.segmentation.processors import *
from tests.utils import load_image_color, save_result


class TestGeneral(TestCase):
    def test_results_white_tower(self):
        image = load_image_color('white-tower.png')
        processor = Slic(image.copy())
        processed_image = processor.process()
        save_result(path.join('slic/', processor.get_file_prefix() + '.white-tower.png'), processed_image)

    def test_results_wt_slic(self):
        image = load_image_color('wt_slic.png')
        processor = Slic(image.copy())
        processed_image = processor.process()
        save_result(path.join('slic/', processor.get_file_prefix() + '.wt_slic.png'), processed_image)

