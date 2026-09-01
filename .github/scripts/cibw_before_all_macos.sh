#!/usr/bin/env bash
# One-time (per runner) setup for building macOS wheels with cibuildwheel.
# Installs the non-Python-specific casacore dependencies via Homebrew and
# downloads the sources that cibw_before_build_macos.sh compiles once per
# Python version, mirroring docker/py_wheel.docker in the casacore repo.
set -euxo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/cibw_env.sh"

# bison: casacore needs >= 3 and macOS ships 2.3. flex ships with macOS.
# No BLAS package: casacore links the Accelerate framework instead.
brew install bison ccache cfitsio fftw gcc gsl hdf5 libdeflate wcslib
ccache -M 1G

mkdir -p "$CIBW_SRC"
cd "$CIBW_SRC"

# Boost source: Boost.Python must be compiled per Python version.
boost_underscored=${CIBW_BOOST_VERSION//./_}
curl -fsSL --retry 3 \
    "https://archives.boost.io/release/${CIBW_BOOST_VERSION}/source/boost_${boost_underscored}.tar.bz2" \
    -o boost.tar.bz2
tar xjf boost.tar.bz2

# casacore source: libcasa_python3 must be compiled per Python version.
curl -fsSL --retry 3 \
    "https://github.com/casacore/casacore/archive/refs/tags/v${CIBW_CASACORE_VERSION}.tar.gz" \
    -o casacore.tar.gz
tar xzf casacore.tar.gz

# Measures data, bundled into the wheels; see CIBW_DATA in cibw_env.sh.
mkdir -p "$CIBW_DATA"
curl -fsSL --retry 3 https://www.astron.nl/iers/WSRT_Measures.ztar -o measures.tgz
tar xzf measures.tgz -C "$CIBW_DATA"
