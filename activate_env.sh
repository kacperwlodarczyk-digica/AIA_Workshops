#!/bin/bash

# Check if file was sourced
[[ $_ != $0 ]] || echo -e "\n\e[5m\e[91mTHIS SCRIPT SHOULD BE SOURCED RATHER THAN EXECUTED!\e[0m\n"

PYTHON_VERSION=python3.9
PIP_VERSION=pip3.9

# Check if venv not exists
if [ ! -e .venv/bin/activate ]; then
    # Create new venv, return on error
    $PYTHON_VERSION -m venv .venv || return
    # Source newly created venv
    source .venv/bin/activate
    # Upgrade pip and tools for building a package
    pip install --upgrade pip wheel setuptools

    # Install pre-commit
    # python -m pip install pre-commit
    # pre-commit install

    # Install editable package of AI Academy app
    python -m pip install -e .
    python -m mypy_boto3 > /dev/null 2>&1
else
    # Source venv if exists
    source .venv/bin/activate
    echo "Activated virtual env"
    # Install editable package of AI Academy app
    python -m pip install -e .
    python -m mypy_boto3 > /dev/null 2>&1
fi
