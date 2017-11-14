#!/usr/bin/env bash

# Inspired by https://conda.io/docs/travis.html
set -e
set -v


if [ "$TRAVIS_OS_NAME" = linux ]; then
    pip install -e .
    pip3 install -e .
    pip install -r tests/requirements.txt
    pip3 install -r tests/requirements.txt
else
    pip install -e .
    pip install -r tests/requirements.txt
fi
