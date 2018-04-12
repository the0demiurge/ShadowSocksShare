#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

requirements = list()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

dependencies = list()
with open('dependencies.txt') as f:
    requirements = f.read().splitlines()

readme = 'ShadowSocksShare'

setup(name='ShadowSocks-share',

      # PEP 440 -- Version Identification and Dependency Specification
      version='0.0.1',

      # Project description
      description='share free ss',
      long_description=readme,

      # Author details
      author='Charles Xu',
      author_email='charl3s.xu@gmail.com',

      # Project details
      url='https://github.com/the0demiurge/Python-Scripts/tree/master/src/Web/Flask/ShadowSocksShare',

      # Project dependencies
      dependency_links=dependencies,
      install_requires=requirements,
      )
