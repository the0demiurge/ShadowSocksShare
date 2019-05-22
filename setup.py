#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

requirements = list()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

dependencies = list()
with open('dependencies.txt') as f:
    requirements = f.read().splitlines()

readme = '\n'.join(open('README.md').readlines())

setup(
    name='ssshare',
    version='1.1.2',

    # Project description
    description='Crawl ShadowSocksR(SSR) accounts, sharing them on the web, and supporting subscription.',
    long_description=readme,
    long_description_content_type="text/markdown",

    # Author details
    author='Charles Xu',
    author_email='charl3s.xu@gmail.com',

    # Project details
    url='https://github.com/the0demiurge/ShadowSocksShare',

    # Project dependencies
    dependency_links=dependencies,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
    ],
)
