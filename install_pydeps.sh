#!/bin/sh
cd "$(dirname "$0")"
mkdir -p pydeps
if ! python3 -m pip --version
then
    curl https://bootstrap.pypa.io/get-pip.py -o pydeps/get-pip.py
    python3 pydeps/get-pip.py --user
fi
python3 -m pip install --target=pydeps bottle markdown pillow pygments
