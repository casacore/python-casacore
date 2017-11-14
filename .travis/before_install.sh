#!/usr/bin/env bash

# Inspired by https://conda.io/docs/travis.html
set -e
set -v


if [ "$TRAVIS_OS_NAME" = linux ]; then
    sudo apt-get update
    sudo apt-get install casacore-data casacore-dev libboost-python-dev \
		libcasa-python3-2 libcfitsio3-dev python-dev python-numpy \
		python-setuptools python-six python3-all python3-dev python3-numpy \
		python3-setuptools python3-six wcslib-dev python-pip, python3-pip \
        python-nose python3-nose
else
	wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -O miniconda.sh;
	bash miniconda.sh -b -p $HOME/miniconda
	export PATH="$HOME/miniconda/bin:$PATH"
	hash -r
	conda config --set always_yes yes --set changeps1 no
	conda update -q conda
	conda config --add channels conda-forge
	# Useful for debugging any issues with conda
	conda info -a
	conda create -q -n testenv python2.7 casacore=2.3.0

	source activate testenv
	export CPATH="$HOME/miniconda/envs/testenv/include:$CPATH"
    mkdir $HOME/data
    cd $HOME/data
    wget ftp://ftp.astron.nl/outgoing/Measures/WSRT_Measures.ztar && tar xf WSRT_Measures.ztar &&
    cd $HOME
	echo "measures.directory: $HOME/data" > $HOME/.casarc
fi
