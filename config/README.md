# Configuration

## Overview

* Install Cubit, which contains Sculpt, a part of the workflow.  Follow the [local installation](cubit-local-installation.md) instructions.
* Configure the local machine with a virtual environment ("venv") named `.venv`.
  * Some historical documents may show the virtual environment name as `atmesh_env`, the deprecated name.
  * The name `.venv` is now preferred since VS Code looks for this naming patttern to automatically load the environment on VS Code start up.
* Create a `pyproject.toml` to configure the `atmesh` package.
* Install the `atmesh` module in developer mode (aka "editable").
* Run unit tests and code coverage.

## Methods

* Reference: https://packaging.python.org/en/latest/tutorials/installing-packages/
* Instead of any `python3` install, `python3.11` is used specifically for compatibility with Cubit version 16.10.
* ~~Instead of any `python3` install, `python3.7` is used specifically for compatibility with Cubit version 16.06.~~
* ~~Python 3.7.9 is available [here](https://www.python.org/downloads/release/python-379/).~~
* Prerequisites:
  * The `autotwin` directory is created within the home `~` directory, and 
  * The `mesh` [repo](https://github.com/autotwin/mesh) is cloned into that `autotwin` folder.
* VS Code [Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)

### Upgrade Python

* 2023-03-03: Upgrade from Python version 3.7 to 3.11.  See Python [downloads](https://www.python.org/downloads/) page.
* Accept default install location: `python3.11@ -> ../../../Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11`

From Cubit user support (T.H.) 2023-03-06:

> CUBIT 16.10 now supports Python 3.6 through Python 3.11 - apart from macs with M1 chips. This story is in the backlog.
> Another M1 user was able to workaround as follows:

```bash
Thank you for your response. I have managed to run cubit python command on M1 mac terminal by creating a separate conda environment with x86_64 python packages. For your reference here what I have done for the installation:

1. Install anaconda / miniconda / miniforge (if it is not present)
2. On a terminal type and execute:
   a. CONDA_SUBDIR=osx-64 conda create -n cubit_x86 python=3.7
   b. conda activate cubit_x86
   c. conda config --env --set subdir osx-64
3. To make sure what machine platform is using: python -c "import platform;print(platform.machine())"
```

Use `arch -x86_64` prefix (do not use conda, as suggested above).  Example:

```bash
Users/chovey/autotwin/mesh> source .venv/bin/activate.fish

(.venv) Users/chovey/autotwin/mesh> python --version
Python 3.11.2

(.venv) Users/chovey/autotwin/mesh> python -c "import platform; print(platform.machine())"
arm64

(.venv) Users/chovey/autotwin/mesh> python3.7 -c "import platform; print(platform.machine())"
x86_64

(.venv) Users/chovey/autotwin/mesh> arch -x86_64 python -c "import platform; print(platform.machine())"
x86_64
```

Then

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

```bash
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

pip install --upgrade pip setuptools
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
fonttools       4.39.0
iniconfig       2.0.0
kiwisolver      1.4.4
matplotlib      3.7.1
mccabe          0.7.0
mypy-extensions 1.0.0
numpy           1.24.2
packaging       23.0
pathspec        0.11.0
Pillow          9.4.0
pip             23.0.1
platformdirs    3.1.0
pluggy          1.0.0
pycodestyle     2.10.0
pyflakes        3.0.1
pyparsing       3.0.9
pytest          7.2.2
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

Run the tests with `pytest`:

```bash
arch -x86_64 pytest -v  # note the `arch -x86_64` ahead of `pytest -v`

========================================================== test session starts ==========================================================
platform darwin -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0 -- /Users/chovey/autotwin/mesh/.venv/bin/python3.11
cachedir: .pytest_cache
rootdir: /Users/chovey/autotwin/mesh
plugins: cov-4.0.0
collected 14 items        
tests/test_command_line.py::test_say_hello PASSED                                   [  7%]
tests/test_command_line.py::test_version PASSED                                     [ 14%]
tests/test_command_line.py::test_yml_version PASSED                                 [ 21%]
tests/test_cubit_inp_to_minsj_csv.py::test_known_element_count PASSED               [ 28%]
tests/test_fac_to_obj.py::test_file_bad PASSED                                      [ 35%]
tests/test_fac_to_obj.py::test_cube_translation PASSED                              [ 42%]
tests/test_hello.py::test_hello PASSED                                              [ 50%]
tests/test_hello.py::test_adios PASSED                                              [ 57%]
tests/test_sculpt_stl_to_inp.py::test_when_io_fails PASSED                          [ 64%]
tests/test_sculpt_stl_to_inp.py::test_cubit_init PASSED                             [ 71%]
tests/test_sculpt_stl_to_inp.py::test_two_spheres PASSED                            [ 78%]
tests/test_sculpt_stl_to_inp.py::test_import_cubit_fails SKIPPED (work in progress) [ 85%]
tests/test_yml_to_dict.py::test_return_is_dict PASSED                               [ 92%]
tests/test_yml_to_dict.py::test_when_io_fails PASSED                                [100%]
```

And `pytest-cov` (coverage) with line numbers missing coverage:

```bash
(.venv) arch -x86_64 pytest --cov=atmesh --cov-report term-missing
==================================== test session starts ===============================
platform darwin -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0
rootdir: /Users/chovey/autotwin/mesh
plugins: cov-4.0.0
collected 14 items

tests/test_command_line.py ...                                 [ 21%]
tests/test_cubit_inp_to_minsj_csv.py .                         [ 28%]
tests/test_fac_to_obj.py ..                                    [ 42%]
tests/test_hello.py ..                                         [ 57%]
tests/test_sculpt_stl_to_inp.py ...s                           [ 85%]
tests/test_yml_to_dict.py ..                                   [100%]

====================================== warnings summary ================================
tests/test_cubit_inp_to_minsj_csv.py::test_known_element_count
  <frozen importlib._bootstrap>:241: DeprecationWarning: builtin type SwigPyPacked has no __module__ attribute

tests/test_cubit_inp_to_minsj_csv.py::test_known_element_count
  <frozen importlib._bootstrap>:241: DeprecationWarning: builtin type SwigPyObject has no __module__ attribute

tests/test_cubit_inp_to_minsj_csv.py::test_known_element_count
  <frozen importlib._bootstrap>:241: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
src/atmesh/__init__.py                            0      0   100%
src/atmesh/command_line.py                       37     26    30%   15-28, 32-49
src/atmesh/cubit_inp_to_aspect_ratio_csv.py      81     81     0%   35-180
src/atmesh/cubit_inp_to_minsj_csv.py             81     15    81%   65, 93, 97, 115-116, 164-167, 172-176, 180
src/atmesh/cubit_inp_to_skew_csv.py              81     81     0%   35-183
src/atmesh/fac_to_obj.py                         52      6    88%   97-107, 112
src/atmesh/hello.py                               4      0   100%
src/atmesh/sculpt_stl_to_inp.py                 106     17    84%   92, 96, 99, 105, 109, 127-128, 260-263, 268-272, 276
src/atmesh/yml_to_dict.py                        25      0   100%
---------------------------------------------------------------------------
TOTAL                                           467    226    52%

==================== 13 passed, 1 skipped, 3 warnings in 4.38s =========================
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

Next: [Workflow](../doc/README.md)
