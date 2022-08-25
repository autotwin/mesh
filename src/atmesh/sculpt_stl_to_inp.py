"""This module uses Cubit to convert a .stl file into a .inp file using Sculpt

Prerequisites:
* Python 3.7.4 is required to run Cubit 16.06 and Sculpt.
* We actually use Python 3.7.9 successfully for now.

Methods:
> cd ~/autotwin/mesh/src/atmesh

* Interactive Method
# > /usr/local/bin/python3.7 sculpt_stl_to_inp.py <input_file>.yml
> python --version
  Python 3.7.9
> python sculpt_stl_to_inp.py <input_file>.yml

* Log Method
# > /usr/local/bin/python3.7 sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log
> python sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log

Example 1:
# activate the venv atmeshenv
~/autotwin/mesh> source atmeshenv/bin/activate.fish # (atmeshenv) uses Python 3.7
(atmeshenv) ~/autotwin/mesh> python src/atmesh/sculpt_stl_to_inp.py tests/files/sphere.yml

Example 2:
# uses the same venv
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> python src/atmesh/sculpt_stl_to_inp.py ../data/octa/octa_loop00.yml
"""

import argparse
from pathlib import Path
import sys

import yaml


def _yml_to_dict(*, yml_path_file: Path) -> dict:
    """Given a valid Path to a yml input file, read it in and
    return the result as a dictionary."""

    # Compared to the lower() method, the casefold() method is stronger.
    # It will convert more characters into lower case, and will find more matches
    # on comparison of two strings that are both are converted
    # using the casefold() method.
    file_type = yml_path_file.suffix.casefold()

    supported_types = (".yaml", ".yml")

    if file_type not in supported_types:
        raise TypeError("Only file types .yaml, and .yml are supported.")

    try:
        with open(yml_path_file, "r") as stream:
            # See deprecation warning for plain yaml.load(input) at
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            db = yaml.load(stream, Loader=yaml.SafeLoader)
    except yaml.YAMLError as error:
        print(f"Error with YAML file: {error}")
        # print(f"Could not open: {self.self.path_file_in}")
        print(f"Could not open or decode: {yml_path_file}")
        # raise yaml.YAMLError
        raise OSError

    version_specified = db.get("version")
    version_implemented = 1.0

    if version_specified != version_implemented:
        raise ValueError(
            f"Version mismatch: specified was {version_specified}, implemented is {version_implemented}"
        )
    else:
        # require that input file has at least the following keys:
        required_keys = (
            "version",
            "cubit_path",
            "working_dir",
            "stl_path_file",
            "inp_path_file",
        )
        # has_required_keys = all(tuple(map(lambda x: db.get(x), required_keys)))
        found_keys = tuple(db.keys())
        keys_exist = tuple(map(lambda x: x in found_keys, required_keys))
        has_required_keys = all(keys_exist)
        if not has_required_keys:
            raise KeyError(f"Input files must have these keys defined: {required_keys}")
    return db


def translate(*, path_file_input: str):
    # from typing import Final # Final is new in Python 3.8, Cubit uses 3.7

    # atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    user_input = _yml_to_dict(yml_path_file=fin)

    print(f"{atmesh} User input:")
    for key, value in user_input.items():
        print(f"  {key}: {value}")

    cubit_path = user_input["cubit_path"]
    inp_path_file = user_input["inp_path_file"]
    stl_path_file = user_input["stl_path_file"]
    working_dir = user_input["working_dir"]
    working_dir_str = str(Path(working_dir).expanduser())

    for item in [cubit_path, working_dir]:
        if not Path(item).expanduser().is_dir():
            raise OSError(f"{atmesh} Path not found: {item}")

    for item in [stl_path_file]:
        if not Path(item).expanduser().is_file():
            raise OSError(f"{atmesh} File not found: {item}")

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

        cubit.init
        print(f"{atmesh} Import cubit module completed.")

        # cubit.cmd('cd "~/sibl-dev/sculpt/tests/sphere-python"')
        cc = 'cd "' + working_dir_str + '"'
        cubit.cmd(cc)
        print(f"{atmesh} The Cubit Working Directory is set to: {working_dir_str}")

        print(f"{atmesh} stl import initiatied:")
        print(f"{atmesh} Importing stl file: {stl_path_file}")
        cc = 'import stl "' + stl_path_file + '"'
        cubit.cmd(cc)
        print(f"{atmesh} stl import completed.")

        print(f"{atmesh} Sculpt parallel initiated:")
        cc = "sculpt parallel"
        cubit.cmd(cc)
        print(f"{atmesh} Sculpt parallel completed.")

        print(f"{atmesh} Abaqus file export initiated:")
        print(f"{atmesh} Exporting inp file: {inp_path_file}")
        cc = 'export abaqus "' + inp_path_file + '" overwrite'
        cubit.cmd(cc)
        print(f"{atmesh} Abaqus file export completed.")

        # print(f"{atmesh} Script: {Path(__file__).resolve()} has completed.")
        print(f"{atmesh} Done.")

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
