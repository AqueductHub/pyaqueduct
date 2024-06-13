#!/bin/bash
# This script builds the docs

FULL_PATH=$(realpath $0)
SCRIPT_DIR=$(dirname $FULL_PATH)
PROJECT_ROOT=$SCRIPT_DIR/..

set -ex

# convert tutorial notebook to markdown
jupyter nbconvert --to markdown $PROJECT_ROOT/examples/tutorial_notebook.ipynb && \
mv $PROJECT_ROOT/examples/tutorial_notebook.md $PROJECT_ROOT/docs/getting-started.md
