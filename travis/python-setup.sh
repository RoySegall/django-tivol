#!/usr/bin/env bash
#pip install -r requirements.txt
mysql -e 'CREATE DATABASE bifrost;'
#cp bifrost/local_settings.travis.py bifrost/local_settings.py
pip install pycodestyle
