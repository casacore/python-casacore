#!/usr/bin/env bash

# Inspired by https://conda.io/docs/travis.html
set -e
set -v


if [ "$TRAVIS_OS_NAME" = linux ]; then
    nosetests --with-coverage
    nosetests3 --with-coverage
    travis-sphinx --nowarn -s doc build
else
    nosetests --with-coverage
fi
