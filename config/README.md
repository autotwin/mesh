# Configuration

## Overview

* Configure the local machine with a virtual environment ("venv") named `autotwin_env`.  
* Create a `pyproject.toml` to configure the `atmesh` package.
* Install the `atmesh` module in developer mode (aka "editable").
* Assess unit tests and code coverage of the `atmesh` module.

## Methods

* Reference: https://packaging.python.org/en/latest/tutorials/installing-packages/
* Instead of any `python3` install, `python3.7` is used specifically for compatibility with Cubit version 16.06.
* Prerequisites:
  * The `autotwin` directory is created within the home `~` directory, and 
  * The `atmesh` repo is cloned into that `autotwin` folder.

### Within the `autotwin/mesh` folder, install the `venv`

```bash
cd ~/autotwin/mesh

# python3 -m pip install --upgrade pip setuptools wheel
/usr/local/bin/python3.7 -m pip install --upgrade pip setuptools wheel

# python3 -m venv autotwin_env  # create a virtual environment
/usr/local/bin/python3.7 -m venv atmeshenv  # create a virtual environment

# activate the venv with one of the following:
source atmeshenv/bin/activate # for bash shell
source atmeshenv/bin/activate.csh # for c shell
source atmeshenv/bin/activate.fish # for fish shell
source atmeshenv/bin/Activate.fish # for powershell

python --version  # Python 3.7.9, which is the version required by Cubit

pip list

Package    Version
---------- -------
pip        20.1.1
setuptools 47.1.0
WARNING: You are using pip version 20.1.1; however, version 22.2.2 is available.
You should consider upgrading via the '/Users/cbh/autotwin/mesh/atmeshenv/bin/python3.7 -m pip install --upgrade pip' command.
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh>

python -m pip install --upgrade pip

Collecting pip
  Using cached pip-22.2.2-py3-none-any.whl (2.0 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 20.1.1
    Uninstalling pip-20.1.1:
      Successfully uninstalled pip-20.1.1
Successfully installed pip-22.2.2
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh>
```

### Install `atmesh` as a developer

Reference: https://packaging.python.org/en/latest/tutorials/packaging-projects/

```bash
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── your_package_name_here/
│       ├── __init__.py
│       └── example.py
└── tests/
```

Create a `pyproject.toml`, e.g., example `.toml` reference: https://peps.python.org/pep-0621/#example and general setuptools documentation: https://setuptools.pypa.io/en/latest/index.html

Installing from a local source tree, reference:

* https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-a-local-src-tree, and
* development mode: https://setuptools.pypa.io/en/latest/userguide/development_mode.html

```bash
# create an editable install (aka development mode)
python -m pip install -e .  # note: `-e .` = `--editable .`
```

At the time of this writing, the current version of `atmesh` is shown below.  Your version may be newer.  Post-install package status:

```bash
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> pip list
Package            Version Editable project location
------------------ ------- -------------------------
atmesh             0.0.4   /Users/cbh/autotwin/mesh
attrs              22.1.0
black              22.6.0
click              8.1.3
coverage           6.4.4
cycler             0.11.0
flake8             5.0.4
fonttools          4.35.0
importlib-metadata 4.2.0
iniconfig          1.1.1
kiwisolver         1.4.4
matplotlib         3.5.3
mccabe             0.7.0
mypy-extensions    0.4.3
numpy              1.21.6
packaging          21.3
pathspec           0.9.0
Pillow             9.2.0
pip                22.2.2
platformdirs       2.5.2
pluggy             1.0.0
py                 1.11.0
pycodestyle        2.9.1
pyflakes           2.5.0
pyparsing          3.0.9
pytest             7.1.2
pytest-cov         3.0.0
python-dateutil    2.8.2
setuptools         47.1.0
six                1.16.0
tomli              2.0.1
typed-ast          1.5.4
typing_extensions  4.3.0
zipp               3.8.1
```

Note that `pytest` and `pytest-cov` are already installed since they are required in the `pyproject.toml` file.

Deactivate any current `venv`:

```bash
(some_current_venv) cbh@atlas/Users/cbh/autotwin/mesh> deactivate
cbh@atlas/Users/cbh/autotwin/mesh> deactivate
```

Activate the `atmeshenv` virtual environment:

```bash
# activate the venv with one of the following:
source atmeshenv/bin/activate # for bash shell
source atmeshenv/bin/activate.csh # for c shell
source atmeshenv/bin/activate.fish # for fish shell
source atmeshenv/bin/Activate.fish # for powershell
```

Example: activate the venv in fish shell:

```bash
cbh@atlas/Users/cbh/autotwin/mesh> source ../autotwin_env/bin/activate.fish
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh>
```

Run from the REPL:

```bash
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> python --version
Python 3.7.9
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> python
Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from atmesh import hello as hh
>>> dir(hh)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'add_two', 'adios', 'bubble_sort', 'hello']
>>> hh.adios()
'Bye'
>>> quit()
```

Run the tests with `pytest`:

```bash
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> pytest -v
================================================================ test session starts =================================================================
platform darwin -- Python 3.7.9, pytest-7.1.2, pluggy-1.0.0 -- /Users/cbh/autotwin/mesh/autotwin_env/bin/python
cachedir: .pytest_cache
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py::test_one PASSED                                                                                                           [ 25%]
tests/test_hello.py::test_two PASSED                                                                                                           [ 50%]
tests/test_hello.py::test_adios PASSED                                                                                                         [ 75%]
tests/test_hello.py::test_bubble_sort PASSED                                                                                                   [100%]

================================================================= 4 passed in 0.02s ==================================================================
```

And `pytest-cov` (coverage) with line numbers missing coverage:

```bash
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh --cov-report term-missing
================================================================ test session starts =================================================================
platform darwin -- Python 3.7.9, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py ....                                                                                                                       [100%]

---------- coverage: platform darwin, python 3.7.9-final-0 -----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/atmesh/__init__.py                0      0   100%
src/atmesh/command_line.py            7      7     0%   1-11
src/atmesh/hello.py                   8      1    88%   10
src/atmesh/sculpt_stl_to_inp.py      53     53     0%   21-105
---------------------------------------------------------------
TOTAL                                68     61    10%


================================================================= 4 passed in 0.04s ==================================================================
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh>
```

Success!  The `venv` virtual environment `automesh_env` has been created, 
and the `atmesh` module is now installed and tested.
