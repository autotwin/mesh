"""
For coverage:
pytest tests/test_hello.py -v --cov=src/atmesh --cov-report term-missing
"""

# import .hello as hh
# import hello as hh
# from ptg import hello as hh
from atmesh import hello as hh


def test_one():
    assert True


def test_two():
    known = "Hello world!"
    found = hh.hello()

    assert found == known


def test_adios():
    known = "Bye"
    found = hh.adios()

    assert found == known


def test_bubble_sort():
    assert hh.bubble_sort()
