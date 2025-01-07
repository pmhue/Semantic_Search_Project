#!/bin/bash

set -ex

# Check if Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 is not installed."
    echo "Please download it from: https://www.python.org/downloads/release/python-3127/"
    exit 1
fi

python3.12 -m venv .venv
source .venv/bin/activate
pip install --requirement requirements.txt
pip install --requirement requirements.dev.txt
