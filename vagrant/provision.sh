#!/bin/bash -ev

export DEBIAN_FRONTEND=noninteractive

## enable wordwide mirrors and all repositories
cp /vagrant/vagrant/apt.sources.list /etc/apt/sources.list

## install all requirements
apt-get install -y software-properties-common
add-apt-repository ppa:ska-sa/main
add-apt-repository ppa:ska-sa/beta
apt-get update
apt-get upgrade -y

apt-get install -y libcasacore-dev casacore-data