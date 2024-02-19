#!/usr/bin/env bash

# Build pytest coverage report.

FULL_PATH=$(realpath $0)
SCRIPT_DIR=$(dirname $FULL_PATH)
PROJECT_ROOT=$SCRIPT_DIR/..

set -o pipefail

poetry run pytest --cov-config=$PROJECT_ROOT/.coveragerc \
--cov-report=term-missing:skip-covered \
--junitxml=$PROJECT_ROOT/pytest.xml --cov=$PROJECT_ROOT/pyaqueduct \
$PROJECT_ROOT/tests/unittests | tee $PROJECT_ROOT/pytest-coverage.txt
if [[ $? -ne 0 ]]; then
unset pipefail
exit 1
else
unset pipefail
exit 0
fi
