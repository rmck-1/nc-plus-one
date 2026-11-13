#! /bin/bash

sudo apt update -y
sudo apt install git python3.12-venv python3-pip -y
cd /home/ubuntu

git clone https://github.com/rmck-1/nc-plus-one.git

cd nc-plus-one
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

chown -R ubuntu:ubuntu /home/ubuntu/nc-plus-one

nohup uvicorn main:app --host 0.0.0.0 --port 80 &