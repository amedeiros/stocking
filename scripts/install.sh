#!/usr/bin/env bash

apt update
apt upgrade -y
apt install build-essential -y
python -m pip install --upgrade pip
python -m pip install -r /app/requirements.txt
