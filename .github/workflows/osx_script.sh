#!/usr/bin/env bash

wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda config --add channels conda-forge

# Useful for debugging any issues with conda
conda info -a
conda create -q -n testenv python=2.7 casacore=2.3.0
source activate testenv

# setup casacore data
mkdir $HOME/data
cd $HOME/data
wget ftp://ftp.astron.nl/outgoing/Measures/WSRT_Measures.ztar && tar xf WSRT_Measures.ztar &&
cd $HOME
echo "measures.directory: $HOME/data" > $HOME/.casarc

cd $TRAVIS_BUILD_DIR
python setup.py build_ext \
-L$HOME/miniconda/envs/testenv/lib \
-I$HOME/miniconda/envs/testenv/include
pip install -e .
pip install -r tests/requirements.txt
export DYLD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
export LD_LIBRARY_PATH=$HOME/miniconda/envs/testenv/lib
pytest
travis-sphinx --nowarn -s doc build