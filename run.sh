#!/bin/bash

set -e # Exit on error

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_DIR="${THIS_DIR}/venv"

function load-dotenv {
    while read -r line; do
        export "$line"
    done < <(grep -v '^#' "${THIS_DIR}/.env" | grep -v '^$')
}

function create_venv {
    echo "Creating virtual environment..."
    python3 -m venv "${VENV_DIR}"
    source "${VENV_DIR}/bin/activate"
    python -m pip install --upgrade pip
}

function activate_venv {
    if [ ! -d "${VENV_DIR}" ]; then
        create_venv
    else
        source "${VENV_DIR}/bin/activate"
    fi
}

function install {
    activate_venv
    echo "Installing package and dependencies..."
    python -m pip install --editable "${THIS_DIR}/[dev]"
}

function update_hooks {
    activate_venv
    echo "Updating pre-commit hooks..."
    pre-commit autoupdate
    pre-commit clean
    pre-commit install-hooks
}

function lint {
    activate_venv
    echo "Running linters..."
    pre-commit run --all-files
}

function build {
    activate_venv
    echo "Building package..."
    python -m build --sdist --wheel "${THIS_DIR}/"
}

function publish:test {
    activate_venv
    load-dotenv
    echo "Publishing to Test PyPI..."
    twine upload "${THIS_DIR}/dist/*" \
        --repository testpypi \
        --username=__token__ \
        --password="${TEST_PYPI_TOKEN}"
}

function publish:prod {
    activate_venv
    load-dotenv
    echo "Publishing to Test PyPI..."
    twine upload "${THIS_DIR}/dist/*" \
        --repository pypi \
        --username=__token__ \
        --password="${PROD_PYPI_TOKEN}"
}

function release:test {
    lint
    clean
    build
    publish:test
}

function release:prod {
    release:test
    publish:prod
}

function clean {
    echo "Cleaning up..."
    rm -rf "${THIS_DIR}/dist" "${THIS_DIR}/build" "${THIS_DIR}/*.egg-info"
    rm -rf "${THIS_DIR}/.pytest_cache" "${THIS_DIR}/.tox"
    find "${THIS_DIR}" -type d -name "__pycache__" -exec rm -rf {} +
    find "${THIS_DIR}" -type d -name ".mypy_cache" -exec rm -rf {} +
    find . -type d -name '*.egg-info' -exec rm -rf {} +
}

function help {
    echo "Usage: $0 <task> <args>"
    echo "Tasks:"
    compgen -A function | grep -v "^_" | sort | cat -n
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-help}
