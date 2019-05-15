#!/bin/bash
python setup.py sdist bdist_wheel
twine upload dist/*

rm -r build/ dist/ ssshare.egg-info/
