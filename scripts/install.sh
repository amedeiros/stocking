#!/usr/bin/env bash

apt update
apt upgrade -y
apt install build-essential -y
python3 -m pip install --upgrade pip
python3 -m pip install -r /app/requirements.txt
