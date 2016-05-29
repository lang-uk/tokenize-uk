#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "six"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tokenize_uk',
    version='0.1.3',
    description="Simple python lib to tokenize texts into sentences and sentences to words. Small, fast and robust. Comes with ukrainian flavour ",
    long_description=readme + '\n\n' + history,
    author="Vsevolod Dyomkin, Dmitry Chaplinsky",
    author_email='chaplinsky.dmitry@gmail.com',
    url='https://github.com/dchaplinsky/tokenize_uk',
    packages=[
        'tokenize_uk',
    ],
    package_dir={'tokenize_uk':
                 'tokenize_uk'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='tokenize_uk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
