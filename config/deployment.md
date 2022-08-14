# Deployment

Deploy a Python module as a distribution.

Prerequisites:

* A virtual environment created with [Configuration](README.md).

Requirements, from https://pip.pypa.io/en/latest/user_guide/#requirements-files 

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

Install the requirements:

```bash
python -m pip install -r requirements.txt
```

Build and twine:

```bash
python -m pip install --upgrade build
python -m build
```

*Optional:* Upload to archive

```bash
python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*
```

