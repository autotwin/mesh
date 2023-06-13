import pkg_resources  # part of setup tools
from itertools import repeat

from typing import Final

import atmesh.constants as cs

underline: Final[str] = "".join(repeat("-", len(cs.Constants.module_name)))


def say_hello() -> str:
    return "hello world!"


def version() -> str:
    ver = pkg_resources.require("atmesh")[0].version
    print(f"yml input file schema version: {yml_version()}")
    print(f"autotwin mesh module version: {ver}")
    return ver


def atmesh() -> None:  # This is an entry point in pyproject.toml
    """Echos available command line entry points to the terminal."""
    print(underline)
    module_name = cs.Constants.module_name
    print(f"{module_name}")
    print(underline)
    print(
        f"This is the command line interface help for autotwin {module_name} python module."
    )
    print("Available commands:")
    print("atmesh      (this command) Lists the module CLI.")
    print("atmeshinfo  Prints the distribution dependencies.")
    print("cubit_inp_to_quality_csv <input_file_schema.yml>")
    print("            Given an input file with schema of version 1.6,")
    print("            converts ABAQUS .inp file to a quality metric, e.g.,")
    print("            minimum scaled Jacobian file, in comma separated value")
    print("            (.csv) format.")
    print("sculpt_stl_to_inp <input_file_schema.yml>")
    print("            Given an input file with schema of version 1.6,")
    print("            converts a STL file, containing an isosurface, to an")
    print("            all-hex solid in ABAQUS mesh format.")
    print("version     Prints the version of the yml input file schema, and")
    print("            prints the semantic version of the autotwin mesh module.")

    #     print("commands           (this command)")
    #     print("autotwin mesh module available commands:")
    #     print("\n")
    #     print("atmesh")
    #     print("  This command.  Lists the atmesh module API.")
    # print("atmeshinfo")
    # print("  Prints the distribution dependencies.")
    # print("cubit_inp_to_minsj_csv <file.inp>")
    # print("  Converts an ABAQUS .inp file into a minimum scaled Jacobian file")
    # print("  in comma separate value (.csv) format.")
    # print("sculpt_stl_to_inp <file.stl>")
    # print("  Converts a STL file, containing an isosurface, into an all-hex solid")
    # print("  in ABAQUS mesh format.")
    # print("version")
    # print("  Prints the semantic version of the current installation.")


def atmeshinfo() -> None:
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
    * Change from bounding box and cell count to bounding box and cell size, for
    interfacing with Sculpt.

    1.3:
    * Deprecate cell_count, use cell_size instead.
    * Bounding box now a required key and value.

    For additional version history, see
    https://github.com/autotwin/mesh/tree/main#updates
    """
    # return 1.6
    aa = cs.Constants.yml_schema_version
    return aa
