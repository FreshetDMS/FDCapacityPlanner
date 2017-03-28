#!/usr/bin/env python
""" Basic Setup Script """

from setuptools import setup
import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name='fdcp',
    version='0.0.1',
    description='Vector Bin Packing based Capacity Planner for Distributed Log Stores',
    author='Milinda Pathirage, Michael Gabay (Original author of vsvbp)',
    author_email='milinda.pathirage@gmail.com',
    packages=['vsvbp'],
    test_suite='setup.my_test_suite',
    include_package_data=True,
    scripts=['bin/fdcp'],
    url='https://github.com/FreshetDMS/FDCapacityPlanner',
    license='GPL',
    long_description=open('README.md').read(),
    keywords='',
    use_2to3=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
)
