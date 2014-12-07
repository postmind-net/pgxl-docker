#!/bin/sh

sudo apt-get update
sudo apt-get install -y docker.io python-pip
sudo pip install fig

sudo wget -O /usr/local/bin/weave \
  https://raw.githubusercontent.com/zettio/weave/master/weave
sudo chmod a+x /usr/local/bin/weave

sudo gpasswd -a ${USER} docker

