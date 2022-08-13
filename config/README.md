# Configuration

From https://packaging.python.org/en/latest/tutorials/installing-packages/

```bash
python3 -m pip install --upgrade pip setuptools wheel

python3 -m venv autotwin_env  # create a virtual environment

# activate the venv with one of the following:
source autotwin_env/bin/activate # for bash shell
source autotwin_env/bin/activate.csh # for c shell
source autotwin_env/bin/activate.fish # for fish shell
source autotwin_env/bin/Activate.fish # for powershell

pip list
```

From https://packaging.python.org/en/latest/tutorials/packaging-projects/

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

Create a `pyproject.toml`

```bash
python3 -m pip install --upgrade build
python3 -m build
```

Upload to archive

```bash
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

Installing from a local source tree, from

https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-a-local-src-tree

and 

development mode: https://setuptools.pypa.io/en/latest/userguide/development_mode.html

```bash
cd ~/autotwin/mesh

# create a virtual environment
python3 -m venv autotwin_env

# activate the virtual environment
source autotwin_env/bin/activate # for bash shell
source autotwin_env/bin/activate.csh # for c shell
source autotwin_env/bin/activate.fish # for fish shell
source autotwin_env/bin/Activate.fish # for powershell

# upgrade pip for good measure
python3 -m pip install --upgrade pip

# create an editable install (aka development mode)
python3 -m pip install -e .  # note: `-e .` = `--editable .`
```

Post-install package status:

```bash
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> pip list          (base)
Package         Version Editable project location
--------------- ------- -------------------------
atmesh          0.0.2a2 /Users/cbh/autotwin/mesh
attrs           22.1.0
coverage        6.4.3
cycler          0.11.0
fonttools       4.34.4
iniconfig       1.1.1
kiwisolver      1.4.4
matplotlib      3.5.3
numpy           1.23.1
packaging       21.3
Pillow          9.2.0
pip             22.2.2
pluggy          1.0.0
py              1.11.0
pyparsing       3.0.9
pytest          7.1.2
pytest-cov      3.0.0
python-dateutil 2.8.2
setuptools      56.0.0
six             1.16.0
tomli           2.0.1
```

Requirements, from https://pip.pypa.io/en/latest/user_guide/#requirements-files 

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

Install pytest

```bash
python3 -m pip install pytest
python3 -m pip install pytest-cov
```

Update `requirements.txt`

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

Install the requirements:

```bash
python -m pip install -r requirements.txt
```

Deactivate any current `venv`:

```bash
(some_current_venv) cbh@atlas/Users/cbh/autotwin/mesh> deactivate
cbh@atlas/Users/cbh/autotwin/mesh> deactivate
```

Activate the `autotwin_env` virtual environment:

```bash
# activate the venv with one of the following:
source autotwin_env/bin/activate # for bash shell
source autotwin_env/bin/activate.csh # for c shell
source autotwin_env/bin/activate.fish # for fish shell
source autotwin_env/bin/Activate.fish # for powershell
```

Example: activate the venv in fish shell:

```bash
cbh@atlas/Users/cbh/autotwin/mesh> source autotwin_env/bin/activate.fish
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh>
```

Test

```bash
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> python --version                     (base)
Python 3.8.13
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> python                               (base)
Python 3.8.13 (default, Mar 28 2022, 06:13:39)
[Clang 12.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from atmesh import hello
>>> from atmesh import hello as hh
>>> dir(hh)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'add_two', 'adios', 'bubble_sort', 'hello']
>>> hh.hello
<function hello at 0x104caaca0>
>>> hh.hello()
'Hello world!'
>>> quit()
```

And pytest

```bash
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest -v                            (base)
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0 -- /Users/cbh/autotwin/mesh/autotwin_env/bin/python3
cachedir: .pytest_cache
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py::test_one PASSED                                                   [ 25%]
tests/test_hello.py::test_two PASSED                                                   [ 50%]
tests/test_hello.py::test_adios PASSED                                                 [ 75%]
tests/test_hello.py::test_bubble_sort PASSED                                          [100%]

===================================== 4 passed in 0.01s ======================================
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> 

```

And pytest-cov (coverage)

```bash
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh                  (base)
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py ....                                                               [100%]

---------- coverage: platform darwin, python 3.8.13-final-0 ----------
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/atmesh/__init__.py                0      0   100%
src/atmesh/command_line.py            7      7     0%
src/atmesh/hello.py                   8      1    88%
src/atmesh/sculpt_stl_to_inp.py      53     53     0%
-----------------------------------------------------
TOTAL                                68     61    10%

===================================== 4 passed in 0.02s ======================================
```

Finally, line numbers missing coverage:

```bash
(autotwin_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh --cov-report term-missing
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py ....                                                               [100%]

---------- coverage: platform darwin, python 3.8.13-final-0 ----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/atmesh/__init__.py                0      0   100%
src/atmesh/command_line.py            7      7     0%   1-11
src/atmesh/hello.py                   8      1    88%   10
src/atmesh/sculpt_stl_to_inp.py      53     53     0%   16-100
---------------------------------------------------------------
TOTAL                                68     61    10%

===================================== 4 passed in 0.02s ======================================
```

