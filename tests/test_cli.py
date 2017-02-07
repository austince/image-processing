
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from edges import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['edges', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)

        output = popen(['edges', '--help'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['edges', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertEqual(str(output.strip()), VERSION)
