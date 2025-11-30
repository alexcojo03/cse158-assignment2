#!/usr/bin/env bash
set -e
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
echo
echo "Environment created. Run 'source .venv/bin/activate' to activate it."