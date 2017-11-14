FROM kernsuite/base:3

RUN apt-get update && apt-get install -y casacore-data casacore-dev \
    libboost-python-dev libcasa-python3-2 libcfitsio3-dev python-dev \
    python-numpy python-setuptools python-six python3-all python3-dev \
    python3-numpy python3-setuptools python3-six wcslib-dev python-pip \
    python3-pip python-nose python3-nose

ADD . /code
WORKDIR /code

RUN pip install -e .
RUN pip3 install -e .

RUN pip install -r tests/requirements.txt
RUN pip3 install -r tests/requirements.txt

RUN nosetests --with-coverage
RUN nosetests3 --with-coverage
