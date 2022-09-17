"""This module uses Cubit to convert a .inp file to an assessment
of minimum scaled Jacobian of the mesh.

Prerequisites:
* Cubit 16.06
* Python 3.7.x

Methods (example):
> cd ~/autotwin/mesh/src/mesh
~/autotwin/mesh> source atmeshenv/bin/activate.fish # (atmeshenv) uses Python 3.7
(atmeshenv) ~/autotwin/mesh> python src/atmesh/cubit_inp_to_minsj.py tests/files/sphere_minsj.yml
"""

import argparse
from pathlib import Path
import sys


import atmesh.yml_to_dict as translator


def translate(*, path_file_input: str) -> int:
    # from typing import Final # Final is new in Python 3.8, Cubit uses 3.7

    # atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    # user_input = _yml_to_dict(yml_path_file=fin)
    # keys = ("version", "cubit_path", "working_dir", "stl_path_file", "inp_path_file")
    keys = ("version", "cubit_path", "working_dir", "inp_path_file")
    user_input = translator.yml_to_dict(
        yml_path_file=fin, version=1.1, required_keys=keys
    )

    print(f"{atmesh} User input:")
    for key, value in user_input.items():
        print(f"  {key}: {value}")

    cubit_path = user_input["cubit_path"]
    inp_path_file = user_input["inp_path_file"]
    inp_path_file_str = str(Path(inp_path_file).expanduser())
    working_dir = user_input["working_dir"]
    working_dir_str = str(Path(working_dir).expanduser())

    journaling = user_input.get("journaling", False)

    for item in [cubit_path, working_dir]:
        if not Path(item).expanduser().is_dir():
            raise OSError(f"{atmesh} Path not found: {item}")

    for item in [inp_path_file]:
        if not Path(Path(item).expanduser().parent).is_dir():
            raise OSError(f"{atmesh} Path not found: {item}")

    # append the cubit path to the system Python path
    print(f"{atmesh} Existing sys.path:")
    for item in sys.path:
        print(f"  {item}")

    sys.path.append(cubit_path)

    print(f"{atmesh} Cubit path now added:")
    for item in sys.path:
        print(f"  {item}")

    try:
        print(f"{atmesh} Import cubit module initiatied:")
        import cubit

        if journaling:
            cubit.init
            print(f"{atmesh} Import cubit module completed.  Journaling is ON.")
        else:
            cubit.init(["cubit", "-nojournal"])
            print(f"{atmesh} Import cubit module completed.  Journaling is OFF.")

        # cubit.cmd('cd "~/sibl-dev/sculpt/tests/sphere-python"')
        cc = 'cd "' + working_dir_str + '"'
        cubit.cmd(cc)
        print(f"{atmesh} The Cubit Working Directory is set to: {working_dir_str}")

        print(f"{atmesh} inp import initiatied:")
        print(f"{atmesh} Importing inp file: {inp_path_file_str}")

        cc = 'import abaqus mesh geometry "' + inp_path_file_str + '" feature_angle 135'
        cubit.cmd(cc)
        print(f"{atmesh} inp import completed.")

        # TODO: start on hex count
        n_elements = cubit.get_hex_count()
        print(f"Number of elements: {n_elements}")

        print(f"{atmesh} Done.")

        return n_elements

    except ModuleNotFoundError as error:
        print("unable to import cubit")
        print(f"{atmesh} {error}")
        raise ModuleNotFoundError


if __name__ == "__main__":
    """Runs the module from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml user input file")
    args = parser.parse_args()
    input_file = args.input_file

    translate(path_file_input=input_file)
