#!/usr/bin/env bash

# This script builds the docker images for a release
# -t Tag to tag images with, defaults to dev if not specified
# -p Push built package to PyPi

FULL_PATH=$(realpath $0)
SCRIPT_DIR=$(dirname $FULL_PATH)
PROJECT_ROOT=$SCRIPT_DIR/..
set -e
set -o pipefail

tag="dev"
push="false"

while getopts "t:p:" flag
do 
    case "${flag}" in
        t) tag=${OPTARG};;
        p) push=${OPTARG};;
    esac
done

mkdir build

if [[ -z $(which poetry) ]]; then
echo "Installing poetry"
    export POETRY_HOME=$HOME/.local
    curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
    export PATH="$POETRY_HOME/bin:$PATH"
    poetry config virtualenvs.in-project false
fi

echo "Create sdist"
poetry build -f sdist

if [[ $push != "false" ]]; then

fi
