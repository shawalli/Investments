#!/bin/bash

# Assumes prior installation of virtualenv


if [[ ! -d "venv" ]]; then
    echo "Creating virtual environment"
    virtualenv venv
    . venv/bin/activate
fi

echo "Removing prior builds of app"
rm -rf build/ dist/

echo "Building app"
python setup.py py2app

echo
echo "Done."