#!/bin/bash -ev

export DEBIAN_FRONTEND=noninteractive

## enable wordwide mirrors and all repositories
cp /vagrant/vagrant/apt.sources.list /etc/apt/sources.list

## install all requirements
apt-get update
apt-get install -y software-properties-common python-numpy python-nose \
                    python-setuptools libboost-python-dev libcfitsio3-dev
add-apt-repository ppa:ska-sa/beta
apt-get update
apt-get install -y libcasacore-dev
