#!/bin/bash

# Check if file was sourced innstead of executed
[[ $_ != $0 ]] || echo -e "\n\e[5m\e[91mTHIS SCRIPT SHOULD BE SOURCED RATHER THAN EXECUTED!\e[0m\n"

PYTHON_VERSION=python3.9
PIP_VERSION=pip3.9
PIP_VERBOSITY="-q"

# Check if venv not exists
if [ ! -e .venv/bin/activate ]; then
    # Create new venv, return on error
    $PYTHON_VERSION -m venv .venv || return
    # Source newly created venv
    source .venv/bin/activate
    # Upgrade pip and tools for building a package
    pip $PIP_VERBOSITY install --upgrade pip wheel setuptools

    # Install pre-commit
    python -m pip install pre-commit
    pre-commit install

    # Install editable package of AI Academy app
    python -m pip install -e app
else
    # Source venv if exists
    source .venv/bin/activate
    echo "Activated virtual env"
    # Install editable package of AI Academy app
    python -m pip install -e app
fi

# Install requirements
pip $PIP_VERBOSITY install -r requirements.txt
