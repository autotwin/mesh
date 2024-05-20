"""
For coverage:
pytest tests/test_hello.py -v --cov=src/atmesh --cov-report term-missing
"""

# import .hello as hh
# import hello as hh
# from ptg import hello as hh
from atmesh import hello as hh


def test_hello():
    known = "Hello world!"
    found = hh.hello()

    assert found == known


def test_adios():
    known = "Bye"
    found = hh.adios()

    assert found == known


def test_origin():
    """Test the origin is at (0.0, 0.0, 0.0)."""
    origin = hh.Origin()
    assert type(origin).__name__ == "Origin"
    assert origin.x0 == 0.0
    assert origin.y0 == 0.0
    assert origin.z0 == 0.0


def test_centroid():
    """Tests that the Centroid data type is as expected."""
    centroid = hh.Centroid(cx=1.0, cy=2.0, cz=3.0)
    assert type(centroid).__name__ == "Centroid"
    assert centroid.cx == 1.0
    assert centroid.cy == 2.0
    assert centroid.cz == 3.0
