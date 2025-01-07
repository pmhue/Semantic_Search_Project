#!/bin/bash

set -ex

# Check if Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 is not installed."
    echo "Please download it from: https://www.python.org/downloads/release/python-3127/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file does not exist."
    echo "Please create it from .env.sample."
    exit 1
fi

source .venv/bin/activate
python -m unittest discover -s test -v
