#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    python3-dateutil \
    python3.8-venv
sudo ln -s /usr/bin/python3 /usr/bin/python
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
PATH="$HOME/.local/bin:$PATH"
export PATH
git clone https://github.com/OlegVolchenko/bikes-rental-project.git
cd bikes-rental-project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PREFECT_KEY=$(gcloud secrets versions access 1 --secret="prefect-key")
export PROJECT=$(gcloud config get project)
export WORKSPACE=$(gcloud secrets versions access 1 --secret="prefect-workspace")
prefect cloud login -k $PREFECT_KEY -w $WORKSPACE
prefect agent start -q main
