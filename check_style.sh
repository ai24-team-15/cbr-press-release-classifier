#!/bin/bash

# Exit on first error
set -e

check_directory () {
  echo "Check directory $1"
  cd $1
  # Define directories and file patterns to check
  PYTHON_FILES=$(find "." -type f -name "*.py" ! -path "./.venv/*" ! -path "./tests*")

  if [ -z "$PYTHON_FILES" ]; then
    echo "No Python files found in the project."
    exit 0
  fi

  # Run flake8
  echo "Running flake8..."
  echo "$PYTHON_FILES" | xargs -n 5 flake8 --max-line-length=120 || {
    exit 1;
  }

  # Run pylint
  echo "Running pylint..."
  pylint --max-line-length=120 --disable="C0103,C0114,C0115" $PYTHON_FILES || {
    exit 1;
  }

  # Run pycodestyle
  echo "Running pycodestyle..."
  pycodestyle --max-line-length 120 $PYTHON_FILES || {
    echo "pycodestyle found issues:";
    pycodestyle --max-line-length 120 $PYTHON_FILES;
    exit 1;
  }
  cd ..
}

check_directory "cbr_ui"
check_directory "cbr_api"

echo "Style checks passed successfully."
