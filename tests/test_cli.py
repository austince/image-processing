
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from detection import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['detection', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)

        output = popen(['detection', '--help'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue("usage:" in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['detection', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertEqual(str(output.strip()), VERSION)
