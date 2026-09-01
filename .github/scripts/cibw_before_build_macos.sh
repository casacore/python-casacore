#!/usr/bin/env bash
# Per-Python-version build of Boost.Python and casacore for macOS wheels.
# cibuildwheel runs this before building each wheel, with the target Python
# first on PATH as `python`. It is the macOS analogue of docker/py_wheel.docker
# in the casacore repo: libcasa_python3 embeds the CPython ABI, so both
# libraries are rebuilt per Python version into CIBW_PREFIX, where the
# python-casacore build finds them via CMAKE_PREFIX_PATH.
#
# As in the Linux wheel images, libcasa_python3 must not link a real
# libpython, or the wheels would only work with one specific interpreter:
# Python3_LIBRARY is pointed at Boost.Python and Python symbols are left
# undefined, to be resolved from the host interpreter at import time.
set -euxo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/cibw_env.sh"

BREW_PREFIX=$(brew --prefix)
export PATH="$BREW_PREFIX/opt/bison/bin:$PATH"
NCPU=$(sysctl -n hw.ncpu)

PYTHON=$(command -v python)
PY_VER=$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
PY_XY=${PY_VER//./}
PY_INCLUDE=$("$PYTHON" -c 'import sysconfig; print(sysconfig.get_path("include"))')

rm -rf "$CIBW_PREFIX"

# ---- Boost.Python against the target Python ------------------------------
# numpy is installed only afterwards, so that b2 skips boost_numpy, matching
# the build order in docker/py_wheel.docker.
cd "$CIBW_SRC/boost_${CIBW_BOOST_VERSION//./_}"
b2_args=()
if command -v ccache >/dev/null; then
    # Route b2 through ccache too, via the darwin toolset so Boost.Python
    # keeps its macOS-specific linking (no libpython; see the header).
    echo "using darwin : : ccache clang++ ;" > user-config.jam
    b2_args=(--user-config=user-config.jam)
fi
./bootstrap.sh --prefix="$CIBW_PREFIX" \
    --with-libraries=python \
    --with-python="$PYTHON" \
    --with-python-version="$PY_VER"
# b2 cannot derive the include dir from a virtualenv Python; the same
# workaround as in docker/py_wheel.docker.
./b2 -j"$NCPU" "${b2_args[@]}" cxxflags="-fPIC -I$PY_INCLUDE" install

# ---- casacore against the target Python ----------------------------------
"$PYTHON" -m pip install numpy

# Flags taken from casacore's own recipes: docker/py_wheel.docker and its
# Homebrew formulae.
casacore_args=(
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX="$CIBW_PREFIX"
    -DBUILD_TESTING=OFF
    -DBUILD_PYTHON=OFF
    -DBUILD_PYTHON3=ON
    -DPython3_EXECUTABLE="$PYTHON"
    -DPython3_INCLUDE_DIR="$PY_INCLUDE"
    # Boost.Python stands in for libpython; see the header comment.
    -DPython3_LIBRARY="$CIBW_PREFIX/lib/libboost_python${PY_XY}.dylib"
    -DPORTABLE=TRUE
    -DUSE_PCH=FALSE
    -DUSE_OPENMP=OFF
    -DUSE_FFTW3=ON
    -DUSE_HDF5=ON
    -DDATA_DIR="$CIBW_DATA"
)

# macOS-specific additions, not present in the casacore recipes.
macos_args=(
    # Find the Homebrew-installed dependencies.
    -DCMAKE_PREFIX_PATH="$BREW_PREFIX"
    # Find the per-Python Boost built above.
    -DBoost_ROOT="$CIBW_PREFIX"
    # Allow undefined symbols, so that Python symbols resolve from the host
    # interpreter at import time. ELF linkers allow this by default, which is
    # why the Linux recipe needs no such flag.
    -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-undefined,dynamic_lookup"
)

# ccache makes the repeated casacore builds cheap after the first.
CCACHE_ARGS=()
if command -v ccache >/dev/null; then
    CCACHE_ARGS=(
        -DCMAKE_C_COMPILER_LAUNCHER=ccache
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
    )
fi

rm -rf "$CIBW_SRC/casacore-build"
cmake -S "$CIBW_SRC/casacore-$CIBW_CASACORE_VERSION" -B "$CIBW_SRC/casacore-build" \
    "${casacore_args[@]}" "${macos_args[@]}" "${CCACHE_ARGS[@]}"
cmake --build "$CIBW_SRC/casacore-build" --parallel "$NCPU"
cmake --install "$CIBW_SRC/casacore-build"
