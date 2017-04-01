from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup

from image_processing import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

with open(join(this_dir, 'requirements.txt')) as file:
    reqs_list = file.read().splitlines()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test',
                      '--cov=image_processing',
                      '--cov-report=term-missing',
                      '--ignore=env'])
        raise SystemExit(errno)


setup(
    name='image_processing',
    version=__version__,
    description='basic image processing / edge image_processing for cs 558',
    long_description=long_description,
    url='',
    author='Randall Degges',
    author_email='austin.cawley@gmail.com',
    license='UNLICENSE',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=reqs_list,
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'detection=image_processing.detection.cli:main',
            'segmentation=image_processing.segmentation.cli:main'
        ],
    },
    cmdclass={'test': RunTests},
)
