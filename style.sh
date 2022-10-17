#!/bin/bash

# -----
# Black
# -----
echo "---------------------------------"
echo "Checking code style with Black..."
# black --check src/atmesh --diff
# black --check tests --diff
black --check src/atmesh --diff
black --check tests --diff
# black --check . --diff --line-length=79
echo "Checking code style with Black... Done."




# ------
# flake8
# ------
# flake8 errors:
# E203 whitespace before ':'
# E501 line too long (## > 79 characters)
#
# flake8 warnings:
# W503 line break occurred before a binary operator
#
# flake8 . --statistics
# E501 - line length exceeds 79 characters
# https://peps.python.org/pep-0008/#maximum-line-length

echo "----------------------------------"
echo "Checking code style with flake8..."
flake8 src/atmesh --ignore E203,E501,W503 --statistics
flake8 tests --ignore E203,E501,W503 --statistics
echo "Checking code style with flake8... Done."

# ----
# mypi
# ----
# https://github.com/python/mypy

echo "..."
echo "-----------------------------"
echo "The script has now completed."
echo "-----------------------------"

# sleep 5
