#!/bin/bash

set -e

for ver in 36 37 38 39 310; do
  dockerid=$(docker create python-casacore-py${ver})
  docker cp ${dockerid}:/output/ output-${ver}
  docker rm ${dockerid}
done
