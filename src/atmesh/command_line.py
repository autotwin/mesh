import pkg_resources  # part of setup tools
from itertools import repeat

# module_name: Final[str] = "atmesh"  # postpone Final until 3.9 is required
module_name: str = "atmesh"  # be D.R.Y.
underline: str = "".join(repeat("-", len(module_name)))


def say_hello() -> str:
    return "hello world!"


def version() -> str:
    ver = pkg_resources.require("atmesh")[0].version
    print("autotwin mesh module version:")
    return ver


def atmesh() -> None:  # This is an entry point in pyproject.toml
    """Echos available command line entry points to the terminal."""
    print(underline)
    print(f"{module_name}")
    print(underline)
    print(
        f"This is the command line interface help for autotwin {module_name} python module."
    )
    print("Available commands:")
    print("atmesh      (this command) Lists the module CLI.")
    print("atmeshinfo  Prints the distribution dependencies.")
    print("cubit_inp_to_minsj_csv <file.inp>")
    print("            Converts ABAQUS .inp file into a minimum scaled Jacobian file")
    print("            in comma separate value (.csv) format.")
    print("sculpt_stl_to_inp <file.stl>")
    print("            Converts a STL file, containing an isosurface, into an")
    print("            all-hex solid in ABAQUS mesh format.")
    print("version     Prints the semantic version of the current installation.")

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
    """Returns (float) the current version of the .yml input file that is supported
    throughout the engine.

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
    """
    return 1.3
