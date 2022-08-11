# Configuration

From https://packaging.python.org/en/latest/tutorials/installing-packages/

```bash
python3 -m pip install --upgrade pip setuptools wheel

python3 -m venv tutorial_env

# activate the venv with one of the following:
source tutorial_env/bin/activate # for bash shell
source tutorial_env/bin/activate.csh # for c shell
source tutorial_env/bin/activate.fish # for fish shell
source tutorial_env/bin/Activate.fish # for powershell

pip list

python3 -m pip install --upgrade pip

```


From https://packaging.python.org/en/latest/tutorials/packaging-projects/

```bash
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── example_package_YOUR_USERNAME_HERE/
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

```bash
cd ~/autotwin/mesh
python3 -m pip install -e .
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

Test

```bash
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> python --version                     (base)
Python 3.8.13
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> python                               (base)
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
>>>
```

And pytest

```bash
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest -v                            (base)
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0 -- /Users/cbh/autotwin/mesh/tutorial_env/bin/python3
cachedir: .pytest_cache
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py::test_one PASSED                                                   [ 25%]
tests/test_hello.py::test_two PASSED                                                   [ 50%]
tests/test_hello.py::test_adios PASSED                                                 [ 75%]
tests/test_hello.py::test_bubble_sort PASSED                                          [100%]

===================================== 4 passed in 0.01s ======================================
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> 

```

And pytest-cov (coverage)

```bash
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh tests/           (base)
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py ....                                                               [100%]

---------- coverage: platform darwin, python 3.8.13-final-0 ----------
Name                                                      Stmts   Miss  Cover
-----------------------------------------------------------------------------
tutorial_env/src/atmesh/src/atmesh/__init__.py                0      0   100%
tutorial_env/src/atmesh/src/atmesh/__vesion__.py              1      1     0%
tutorial_env/src/atmesh/src/atmesh/hello.py                   8      1    88%
tutorial_env/src/atmesh/src/atmesh/sculpt_stl_to_inp.py      53     53     0%
-----------------------------------------------------------------------------
TOTAL                                                        62     55    11%


===================================== 4 passed in 0.02s ======================================
```

Finally, line numbers missing coverage:

```bash
(tutorial_env) cbh@atlas/Users/cbh/autotwin/mesh> pytest --cov=atmesh --cov-report term-missing
==================================== test session starts =====================================
platform darwin -- Python 3.8.13, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/cbh/autotwin/mesh
plugins: cov-3.0.0
collected 4 items

tests/test_hello.py ....                                                               [100%]

---------- coverage: platform darwin, python 3.8.13-final-0 ----------
Name                                                      Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------
tutorial_env/src/atmesh/src/atmesh/__init__.py                0      0   100%
tutorial_env/src/tmesh/src/atmesh/__version__.py              1      1     0%   1
tutorial_env/src/atmesh/src/atmesh/hello.py                   8      1    88%   10
tutorial_env/src/atmesh/src/atmesh/sculpt_stl_to_inp.py      53     53     0%   16-100
---------------------------------------------------------------------------------------
TOTAL                                                        62     55    11%


===================================== 4 passed in 0.02s ======================================
```

