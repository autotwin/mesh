# Configuration

## Overview

* Install Cubit, which contains Sculpt, a part of the workflow.  Follow the [local installation](cubit-local-installation.md) instructions.
* Configure the local machine with a virtual environment ("venv") named `.venv`.
  * Some historical documents may show the virtual environment name as `atmesh_env`, the deprecated name.
  * The name `.venv` is now preferred since VS Code looks for this naming patttern to automatically load the environment on VS Code start up.
* Create a `pyproject.toml` to configure the `atmesh` package.
* Install the `atmesh` module in developer mode (aka "editable").
* Assess unit tests and code coverage of the `atmesh` module.

## Methods

* Reference: https://packaging.python.org/en/latest/tutorials/installing-packages/
* Instead of any `python3` install, `python3.7` is used specifically for compatibility with Cubit version 16.06.
* Python 3.7.9 is available [here](https://www.python.org/downloads/release/python-379/).
* Prerequisites:
  * The `autotwin` directory is created within the home `~` directory, and 
  * The `atmesh` repo is cloned into that `autotwin` folder.
* VS Code [Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)

### Upgrade Python

* 2022-03-03: Upgrade from Python version 3.7 to 3.11.  See Python [downloads](https://www.python.org/downloads/) page.
* Accept default install location: `python3.11@ -> ../../../Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11`

```bash
cd ~/autotwin/mesh

# python3 -m pip install --upgrade pip setuptools wheel
/usr/local/bin/python3.11 -m pip install --upgrade pip setuptools wheel

Looking in indexes: https://nexus.web.sandia.gov/repository/pypi-proxy/simple
Requirement already satisfied: pip in /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages (22.3.1)
Collecting pip
  Using cached https://nexus.web.sandia.gov/repository/pypi-proxy/packages/pip/23.0.1/pip-23.0.1-py3-none-any.whl (2.1 MB)
Requirement already satisfied: setuptools in /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages (65.5.0)
Collecting setuptools
  Using cached https://nexus.web.sandia.gov/repository/pypi-proxy/packages/setuptools/67.4.0/setuptools-67.4.0-py3-none-any.whl (1.1 MB)
Collecting wheel
  Using cached https://nexus.web.sandia.gov/repository/pypi-proxy/packages/wheel/0.38.4/wheel-0.38.4-py3-none-any.whl (36 kB)
Installing collected packages: wheel, setuptools, pip
  WARNING: The script wheel is installed in '/Library/Frameworks/Python.framework/Versions/3.11/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  Attempting uninstall: setuptools
    Found existing installation: setuptools 65.5.0
    Uninstalling setuptools-65.5.0:
      Successfully uninstalled setuptools-65.5.0
  Attempting uninstall: pip
    Found existing installation: pip 22.3.1
    Uninstalling pip-22.3.1:
      Successfully uninstalled pip-22.3.1
  WARNING: The scripts pip, pip3 and pip3.11 are installed in '/Library/Frameworks/Python.framework/Versions/3.11/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-23.0.1 setuptools-67.4.0 wheel-0.38.4
```

### Within the `autotwin/mesh` folder, install the `venv`

Note: If `.venv` already exists from previous installs, then remove it with `rm -rf .venv/`.

````bash
# python3 -m venv autotwin_env  # create a virtual environment
# VS Code docs reference:
# https://code.visualstudio.com/docs/python/environments#_create-a-virtual-environment
/usr/local/bin/python3.11 -m venv .venv  # create a virtual environment

# activate the venv with one of the following:
source .venv/bin/activate # for bash shell
source .venv/bin/activate.csh # for c shell
source .venv/bin/activate.fish # for fish shell
source .venv/bin/Activate.fish # for powershell

python --version  # Python 3.11.2 (Cubit 16.10 supports Python 3.6 through Python 3.11)

pip list

Package    Version
---------- -------
pip        22.3.1
setuptools 65.5.0

[notice] A new release of pip available: 22.3.1 -> 23.0.1
[notice] To update, run: pip install --upgrade pip

pip install --upgrade pip
```

### Install the `atmesh` module as a developer

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
pip install -e .  # note: `-e .` = `--editable .`
```

At the time of this writing, the current version of `atmesh` is shown below.  Your version may be newer.  Post-install package status:

```bash
pip list
Package         Version Editable project location
--------------- ------- ---------------------------
atmesh          0.0.7   /Users/chovey/autotwin/mesh
attrs           22.2.0
black           22.6.0
click           8.1.3
contourpy       1.0.7
coverage        7.2.1
cycler          0.11.0
flake8          6.0.0
fonttools       4.38.0
iniconfig       2.0.0
kiwisolver      1.4.4
matplotlib      3.7.0
mccabe          0.7.0
mypy-extensions 1.0.0
numpy           1.24.2
packaging       23.0
pathspec        0.11.0
Pillow          9.4.0
pip             23.0.1
platformdirs    3.0.0
pluggy          1.0.0
pycodestyle     2.10.0
pyflakes        3.0.1
pyparsing       3.0.9
pytest          7.2.1
pytest-cov      4.0.0
python-dateutil 2.8.2
PyYAML          6.0
setuptools      65.5.0
six             1.16.0
```

Note that `pytest` and `pytest-cov` are already installed since they are required in the `pyproject.toml` file.

Deactivate/Reactivate method:  To deactivate any current `venv`:

```bash
(some_current_venv) cbh@atlas/Users/cbh/autotwin/mesh> deactivate
cbh@atlas/Users/cbh/autotwin/mesh> deactivate
```

Deactivate/Reactivate method:  To activate the `.venv` virtual environment:

```bash
# activate the venv with one of the following:
source .venv/bin/activate # for bash shell
source .venv/bin/activate.csh # for c shell
source .venv/bin/activate.fish # for fish shell
source .venv/bin/Activate.fish # for powershell
```

Run from the REPL:

```bash
(.venv) cbh@atlas/Users/cbh/autotwin/mesh> python --version
Python 3.11.2
(.venv) cbh@atlas/Users/cbh/autotwin/mesh> python
>>> from atmesh import hello as hh
>>> dir(hh)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'add_two', 'adios', 'bubble_sort', 'hello']
>>> hh.adios()
'Bye'
>>> quit()
```

**2022-03-03** Stop.  Hit error:

```bash
tests/test_sculpt_stl_to_inp.py:116:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src/atmesh/sculpt_stl_to_inp.py:124: in translate
    import cubit
/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/cubit.py:6: in <module>
    from cubit3 import *
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    # This file was automatically generated by SWIG (https://www.swig.org).
    # Version 4.1.0
    #
    # Do not make changes to this file unless you know what you are doing - modify
    # the SWIG interface file instead.

    from sys import version_info as _swig_python_version_info
    # Import the low-level C/C++ module
    if __package__ or "." in __name__:
        from . import _cubit3
    else:
>       import _cubit3
E       ImportError: dlopen(/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/_cubit3.so, 0x0002): tried: '/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/_cubit3.so' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64')), '/System/Volumes/Preboot/Cryptexes/OS/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/_cubit3.so' (no such file), '/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/_cubit3.so' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64'))

/Applications/Cubit-16.10/Cubit.app/Contents/MacOS/cubit3.py:12: ImportError
```


Run the tests with `pytest`:

```bash
pytest -v
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
(.venv) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh --cov-report term-missing
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
(.venv) cbh@atlas/Users/cbh/autotwin/mesh>
```

Success!  The `venv` virtual environment `.venv` has been created, 
and the `atmesh` module is now installed and tested.

### Modify VS Code to find cubit imports

In the user `settings.json`, add a reference to the Cubit install location.  

Reference: Enable IntelliSense for custom package locations, https://code.visualstudio.com/docs/python/editing#_enable-intellisense-for-custom-package-locations

Before:

```bash
    "python.autoComplete.extraPaths": [
        "~/python_modules"
    ],
```

After:

```bash
    "python.autoComplete.extraPaths": [
        "~/python_modules",
        "/Applications/Cubit-16.08/Cubit.app/Contents/MacOS"
    ],
    "python.envFile": "${workspaceFolder}/.venv",
```

And in the `~/autotwin/mesh/.venv` file:

```
PYTHONPATH="/Applications/Cubit-16.08/Cubit.app/Contents/MacOS"
```

which, in `some_source_file.py` Python files, allows

```python
import cubit
```

to be found.
