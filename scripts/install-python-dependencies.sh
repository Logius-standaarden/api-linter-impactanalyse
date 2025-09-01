#!/usr/bin/env sh
CURRENT_DIRECTORY=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $CURRENT_DIRECTORY

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r $CURRENT_DIRECTORY/requirements.txt
