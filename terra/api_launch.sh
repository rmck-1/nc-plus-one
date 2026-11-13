#! /bin/bash

sudo apt update -y
sudo apt install git python3.12-venv python3-pip postgresql-client -y
cd /home/ubuntu

git clone https://github.com/rmck-1/nc-plus-one.git

cd nc-plus-one
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chown -R ubuntu:ubuntu /home/ubuntu/nc-plus-one
touch .env

echo "PGDATABASE=${db_name}" >> .env
echo "PGUSER=${db_username}" >> .env
echo "PGPASSWORD=${db_password}" >> .env
echo "PGHOST=${db_address}" >> .env
echo "PGPORT=${db_port}" >> .env
echo "JWT_SECRET=${jwt_secret}" >> .env

python3 -m db.seed.seed

nohup uvicorn main:app --host 0.0.0.0 --port 80 &