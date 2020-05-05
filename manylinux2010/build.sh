#!/bin/bash -ve

HERE=`dirname "$0"`
cd $HERE/..

for i in 27 34 35 36 37 38; do
    docker build -f manylinux2010/wheel${i}.docker . -t python-casacore${i}
    docker run -v `pwd`/manylinux2010:/manylinux2010 python-casacore${i} sh -c "cp /output/*.whl /manylinux2010/."
done

