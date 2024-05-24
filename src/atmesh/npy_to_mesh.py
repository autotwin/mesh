"""Converts a semantic segmentation inot a finite element mesh.

Requirements:
    Python 3.11
    Sculpt 16.10

Methods:
    cd ~/autotwin/mesh/src/atmesh

    # Interactive method
    source .venv/bin/activate.fish
    python --version # e.g., Python 3.11.9
    arch x-86_64 python npy_to_mesh <input_file>.yml

"""

import argparse
from pathlib import Path
import subprocess
from typing import Final, NamedTuple


import numpy as np
import yaml

# import atmesh.yml_to_dict as translator
# import atmesh.command_line as cl
import atmesh.constants as cs


class Recipe(NamedTuple):
    """The user input yml recipe as a NamedTuple."""

    sculpt_binary: Path
    sculpt_input: Path
    yml_schema_version: float


ATMESH_PROMPT: Final[str] = cs.Constants.module_prompt


def npy_to_spn(*, input_file: Path) -> Path:
    """Converts a .npy 3D semantic segmentation file into a .spn file.

    Arguments:
        input_file:  The .npy 3D semantic segementation

    Returns:
        Path of the output .spn file.
    """
    print(f"{ATMESH_PROMPT} This is {Path(__file__).resolve()}")

    fin = input_file.expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{ATMESH_PROMPT} File not found: {str(fin)}")

    db = np.load(file=fin)

    flattened = db.flatten()
    output_file = input_file.parent.joinpath(input_file.stem + ".spn")
    np.savetxt(fname=output_file, X=flattened, fmt="%s")
    return output_file


def process(*, input_file: Path) -> int:
    """Converts the semantic segmentation saved in a .npy file into a
    finite element mesh.  A .yml recipe is required.

    Arguments:
        input_file: The .yml recipe that specifies path variables.
            See the schema in the `Recipe(NamedTuple)` for key values
            and types.

    Returns:
        The error code from the subprocess call, which is 0 if successful.
    """
    print(f"{ATMESH_PROMPT} This is {Path(__file__).resolve()}")

    fin = input_file.expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{ATMESH_PROMPT} File not found: {str(fin)}")

    db = []

    try:
        with open(file=fin, mode="r", encoding="utf-8") as stream:
            db = yaml.load(stream, Loader=yaml.SafeLoader)  # overwrite
    except yaml.YAMLError as error:
        print(f"Error with yml module: {error}")
        print(f"Could not open or decode: {fin}")
        raise OSError from error

    recipe = Recipe(
        sculpt_binary=Path(db["sculpt_binary"]).expanduser(),
        sculpt_input=Path(db["sculpt_input"]).expanduser(),
        yml_schema_version=db["yml_schema_version"],
    )

    for item in [recipe.sculpt_binary, recipe.sculpt_input]:
        assert item.is_file(), f"Could not find {item}"

    # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
    sculpt_command = str(recipe.sculpt_binary)
    sculpt_command += " -i " + str(recipe.sculpt_input)
    cc = [str(recipe.sculpt_binary), "-i", str(recipe.sculpt_input)]
    # subprocess.run(sculpt_command, check=True)
    # subprocess.run(sculpt_command)
    result = subprocess.run(cc)

    return result.returncode


# quick testing:
# process(input_file=Path("~/autotwin/mesh/tests/files/letter_f.yml"))


def main():
    """Runs the module from the command line."""
    print(cs.BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml npy to mesh recipe")
    args = parser.parse_args()
    input_file = args.input_file
    input_file = Path(input_file).expanduser()

    process(input_file=input_file)


if __name__ == "__main__":
    main()
