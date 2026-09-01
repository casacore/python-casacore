#!/usr/bin/env bash
# Shared configuration for the macOS cibuildwheel scripts. On Linux the
# equivalent values are frozen into the per-Python wheel images built from
# docker/py_wheel.docker in the casacore repo; macOS has no such images, so
# the before-* scripts build the dependencies at CI time.

# Dependency versions.
export CIBW_BOOST_VERSION="1.91.0"
export CIBW_CASACORE_VERSION="3.8.1"

# Everything under one root, so a single CMAKE_PREFIX_PATH finds both installs.
# CIBW_PREFIX, CIBW_DATA and CCACHE_DIR are duplicated as literals in
# pyproject.toml; CCACHE_DIR also appears in build_release.yml.
export CIBW_ROOT="$HOME/cibw"
export CIBW_SRC="$CIBW_ROOT/src"        # extracted boost + casacore sources
export CIBW_PREFIX="$CIBW_ROOT/local"   # install prefix for boost + casacore
export CCACHE_DIR="$CIBW_ROOT/ccache"   # persisted across CI runs
# The leaf directory must be named "data": python-casacore installs it into
# the wheel by basename, and casacore/__init__.py expects casacore/data.
export CIBW_DATA="$CIBW_ROOT/measures/data"
