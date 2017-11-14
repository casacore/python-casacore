#!/usr/bin/env bash

set -e
set -v

if [ "$TRAVIS_OS_NAME" = linux ]; then
    cd $TRAVIS_BUILD_DIR
    docker build -f .travis/Dockerfile .
fi

if [ "$TRAVIS_OS_NAME" = osx ]; then
    nosetests --with-coverage
    travis-sphinx --nowarn -s doc build
fi
