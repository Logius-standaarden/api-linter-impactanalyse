#!/usr/bin/env sh
CURRENT_DIRECTORY=$(dirname "$0")

cd $CURRENT_DIRECTORY

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
