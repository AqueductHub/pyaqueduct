#!/usr/bin/env bash

# Runs Python unit tests using pytest.

FULL_PATH=$(realpath $0)
SCRIPT_DIR=$(dirname $FULL_PATH)
PROJECT_ROOT=$SCRIPT_DIR/..


poetry run pytest $PROJECT_ROOT/tests/integration -rA -vv
