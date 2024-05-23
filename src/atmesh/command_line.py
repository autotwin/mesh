import pkg_resources  # part of setup tools
from itertools import repeat

from typing import Final

import atmesh.constants as cs

UNDERLINE: Final[str] = "".join(repeat("-", len(cs.Constants.module_name)))

CLI_DOCS: Final[
    str
] = """
------
atmesh
------

This is the command line interface help.

atmesh

    (this command) Echos the command line interface.

atmeshinfo

    Prints the module's dependencies.

cubit_inp_to_quality_csv <input_file.yml>

    Given an input file with schema of version 1.6,
    converts ABAQUS .inp file to a quality metric,
    e.g., minimum scaled Jacobian file, in comma
    separated value (.csv) format.

npy_to_mesh <input_file.yml>
    Given a semantic segmentation consisiting of non-zero
    integers to designate a unique material, saved in .npy format,
    converts the recipe in <input_file.yml> to a finite element
    mesh.

sculpt_stl_to_inp <input_file.yml>

    Given an input file with schema of version 1.6,
    converts a STL file, containing an isosurface, to an
    all-hex solid in ABAQUS mesh format.

version

    Prints the version of the yml input file schema, and
    prints the semantic version of the autotwin mesh module.

"""


def say_hello() -> str:
    """A simple example of Hello world!."""
    return "hello world!"


def version() -> str:
    """Prints the module version and yml schema version."""
    ver = pkg_resources.require("atmesh")[0].version
    print(f"yml input file schema version: {yml_version()}")
    print(f"autotwin mesh module version: {ver}")
    return ver


def atmesh() -> None:  # This is an entry point in pyproject.toml
    """Echos available command line entry points to the terminal."""
    print(CLI_DOCS)


def atmeshinfo() -> None:
    """Prints information about the module's dependencies."""

    dist_info = pkg_resources.require("atmesh")  # distribution information
    print("atmesh module details and dependencies:")

    da = dist_info[0]  # distribution attributes of the atmesh module

    print(f"module name: {da.project_name}")
    print(f"location: {da.location}")
    print(f"version: {da.version}")

    def project_attribute(attribute):
        return attribute.project_name.lower()

    # Now sort the dist_info list in place
    dist_info.sort(key=project_attribute)

    print("module and dependencies:")
    for item in dist_info:
        print(f"- {item}")


def yml_version() -> float:
    """Returns (float) the current version of the .yml input file that is
    supported by the mesh engine.

    1.1:
    * First well-tested version.
    * Single materials.

    1.2:
    * Allow multi-material .stl input files.
    * Change from bounding box and cell count to bounding box
      and cell size, for interfacing with Sculpt.

    1.3:
    * Deprecate cell_count, use cell_size instead.
    * Bounding box now a required key and value.

    For additional version history, see
    https://github.com/autotwin/mesh/tree/main#updates
    """
    # return 1.6
    aa = cs.Constants.yml_schema_version
    return aa
