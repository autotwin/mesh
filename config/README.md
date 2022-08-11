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


