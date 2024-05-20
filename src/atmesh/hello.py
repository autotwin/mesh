from typing import NamedTuple


def hello():
    return "Hello world!"


def adios():
    return "Bye"


class Origin(NamedTuple):
    """The origin in spatial coordinates.
    Defaults to (0.0, 0.0, 0.0).
    """

    x0: float = 0.0
    y0: float = 0.0
    z0: float = 0.0


class Centroid(NamedTuple):
    """The centroid location for the X, Y, and Z axes,
    in length units, i.e., in units of microns.
    """

    cx: float
    cy: float
    cz: float
