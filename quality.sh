#!/bin/bash

# prerequisite to running this script:
# activate the venv with one of the following:
#
# source autotwin_env/bin/activate # for bash shell
# source autotwin_env/bin/activate.csh # for c shell
# source autotwin_env/bin/activate.fish # for fish shell
# source autotwin_env/bin/Activate.fish # for powershell


# historical context: sibl repo
# pytest --cov=geo/src/ptg  --cov-report term-missing

# current context: autotwin repos, either `atmesh` or `atpixel`
pytest --cov=atmesh --cov-report term-missing
# pytest --cov=atpixel  --cov-report term-missing

