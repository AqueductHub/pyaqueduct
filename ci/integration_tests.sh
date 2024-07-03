#!/bin/bash
FULL_PATH=$(realpath $0)
SCRIPT_DIR=$(dirname $FULL_PATH)
PROJECT_ROOT=$SCRIPT_DIR/..
set -e
set -o pipefail

cd $PROJECT_ROOT

mkdir -p /tmp/aqueduct_experiments && \
mkdir -p /tmp/aqueduct_extensions

echo "Building the stack"
docker-compose -f $PROJECT_ROOT/containers/integration_tests/docker-compose.yml up -d

# echo "Fixing permissions"
# sudo chmod -R 777 .

echo "Installing dependencies"
docker exec --workdir /workspace pyaqueduct-host-dev poetry install 

echo "Running integration tests"
docker exec --workdir /workspace pyaqueduct-host-dev ./scripts/run_integration_tests.sh
