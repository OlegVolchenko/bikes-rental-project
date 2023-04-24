#!/bin/bash
git clone https://github.com/OlegVolchenko/bikes-rental-project.git
cd bikes-rental-project
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    python3-dateutil
sudo ln -s /usr/bin/python3 /usr/bin/python
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
PATH="$HOME/.local/bin:$PATH"
export PATH
pip3 install -r requirements.txt
PREFECT_KEY=$(gcloud secrets versions access 1 --secret="prefect-key")
prefect cloud login -k $PREFECT_KEY