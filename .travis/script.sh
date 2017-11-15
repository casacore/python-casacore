#!/usr/bin/env bash

set -e
set -v

if [ "$TRAVIS_OS_NAME" = linux ]; then
    cd $TRAVIS_BUILD_DIR
    docker build -f .travis/Dockerfile .
fi

if [ "$TRAVIS_OS_NAME" = osx ]; then
    export DYLD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
    export LD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
    nosetests --with-coverage
    travis-sphinx --nowarn -s doc build
fi
