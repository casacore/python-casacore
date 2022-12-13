#!/bin/bash

set -e

for ver in 37 38 39 310 311; do
  dockerid=$(docker create python-casacore-py${ver})
  docker cp ${dockerid}:/output/ output-${ver}
  docker rm ${dockerid}
done
