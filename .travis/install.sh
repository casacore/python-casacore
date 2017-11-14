#!/usr/bin/env bash

set -e
set -v


if [ "$TRAVIS_OS_NAME" = linux ]; then
    true
fi

if [ "$TRAVIS_OS_NAME" = osx ]; then
    cd $TRAVIS_BUILD_DIR
    python setup.py build_ext \
        -L$HOME/miniconda/envs/testenv/lib \
        -I$HOME/miniconda/envs/testenv/include
    python setup.py install
    pip install -r tests/requirements.txt
fi

