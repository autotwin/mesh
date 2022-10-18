import pkg_resources  # part of setup tools


def say_hello() -> str:
    return "hello world!"


def version() -> str:
    ver = pkg_resources.require("atmesh")[0].version
    print("autotwin mesh module version:")
    return ver


def yml_version() -> float:
    """Returns (float) the current version of the .yml input file that is supported
    throughout the engine.

    1.1:
    * First well-tested version.
    * Single materials.

    1.2:
    * Allow multi-material .stl input files.
    * Change from bounding box and cell count to bounding box and cell size, for
    interfacing with Sculpt.jJ:w
    """
    return 1.2
