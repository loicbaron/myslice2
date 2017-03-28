#!/bin/bash
#
# This will install and configure myslicelib and myslice 
# See RAEDME.md to understand how to start this image
#

#Installing required software 

apt-get -y install wget libssl-dev libcurl4-openssl-dev curl git

apt-get -y install python3-pip

pip --version

apt-get update \
        && apt-get -y upgrade \
        && apt-get -y install software-properties-common python-software-properties \
		&& add-apt-repository -y ppa:fkrull/deadsnakes \
        && apt-get update \
        && apt-get -y install python3.5 python3.5-dev \
        && apt-get -y install libxml2-dev libxslt1-dev \
        && curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" \
        && python3.5 get-pip.py

apt-get -y install libffi-dev libffi6

#Installing RethinkDB 
echo "deb http://download.rethinkdb.com/apt trusty main" > /etc/apt/sources.list.d/rethinkdb.list \
        && wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | apt-key add - \
        && apt-get update \
        && apt-get -y install rethinkdb \
        && echo "bind=all" > /etc/rethinkdb/instances.d/myslice.conf

# Installing myslicelib
cd /root/ \
        && git clone http://gitlab.noc.onelab.eu/onelab/myslicelib.git \
        && pip install --upgrade pip \
        && pip install -r myslicelib/requirements.txt \
        && cd myslicelib \
        && python3.5 setup.py develop

# Here we need to configure pkey and cert:


mkdir /var/myslice
mkdir /etc/myslice

# INSTALLING myslice #
echo "Installing myslice" \
        && cd /root/ \
        && git clone http://gitlab.noc.onelab.eu/onelab/myslice.git \
        && apt-get -y install libzmq3-dev curl nodejs \
        && pip install -r myslice/requirements.txt \
        && cd myslice \
        && python3.5 setup.py develop \
        && cd /root/ \
		&& curl -sL https://deb.nodesource.com/setup_4.x | bash - \
        && apt-get -y install nodejs \
        && cd /root/myslice/myslice/web/static/js/src/ \
        && npm install \
        && npm i -g webpack \
        && webpack

echo "Configure MySlice with default .cfg"
cp /root/myslice/dist/config/* /etc/myslice/
rename 's/.dist$//' /etc/myslice/*.dist

echo "Configure RethinkDB"
echo "bind=all" > /etc/rethinkdb/instances.d/myslice.conf
/etc/init.d/rethinkdb start
/root/myslice/myslice/bin/db-setup
cd /root/myslice/
