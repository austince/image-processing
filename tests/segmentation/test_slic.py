""" SLIC Tests
"""
from unittest import TestCase

from image_processing.segmentation.processors import *
from tests import test_images_dict
from tests.utils import load_image_bw, save_result


class TestGeneral(TestCase):
    def test_results_wt_slic(self):
        image = load_image_bw(test_images_dict['wt_slic.png'])
        processor = Slic()
        slic_image = processor.process(image.copy())
        save_result('slic/wt_slic.png')

