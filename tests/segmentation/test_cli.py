
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from image_processing.segmentation import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['segmentation', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)

        output = popen(['segmentation', '--help'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['segmentation', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertEqual(str(output.strip()), VERSION)
