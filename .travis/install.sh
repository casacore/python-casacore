#!/usr/bin/env bash

set -e
set -v


if [ "$TRAVIS_OS_NAME" = linux ]; then
    true
fi

if [ "$TRAVIS_OS_NAME" = osx ]; then
    pip install -e .
    pip install -r tests/requirements.txt
fi
