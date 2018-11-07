FROM kernsuite/base:4

RUN docker-apt-install \
    casacore-data \
    casacore-dev \
    libboost-python-dev \
    libcasa-python3-2 \
    libcfitsio-dev \
    wcslib-dev \
    python-dev \
    python-numpy \
    python-setuptools \
    python-six \
    python-pip \
    python-nose \
    python3-all \
    python3-dev \
    python3-numpy \
    python3-setuptools \
    python3-six \
    python3-pip \
    python3-nose


ADD . /code
WORKDIR /code

RUN pip install -e .
RUN pip3 install -e .

RUN pip install -r tests/requirements.txt
RUN pip3 install -r tests/requirements.txt

RUN nosetests --with-coverage --verbose --cover-package=casacore
RUN nosetests3 --with-coverage --verbose --cover-package=casacore
