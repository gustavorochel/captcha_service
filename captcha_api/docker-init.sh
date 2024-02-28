#!/bin/bash
dpkg --configure -a
apt-get update
apt-get install ffmpeg libsm6 libxext6 -y
pip install --upgrade pip
pip install -r requirements.txt
cd ./app
uvicorn app.main:app --host 0.0.0.0 --port $SERVER_PORT