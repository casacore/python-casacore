#!/usr/bin/env bash

set -e
set -v

if [ "$TRAVIS_OS_NAME" = linux ]; then
    cd $TRAVIS_BUILD_DIR
    docker build . -t ${TARGET} -f .travis/${TARGET}.docker
fi

if [ "$TRAVIS_OS_NAME" = osx ]; then
    export DYLD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
    export LD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
    pytest
    travis-sphinx --nowarn -s doc build
fi
