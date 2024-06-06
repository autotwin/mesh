"""This module takes in an Exodus file, deletes blocks specified, and then
writes out a new Exodus file without the deleted block.
"""

import argparse
from pathlib import Path
from typing import Final, NamedTuple

import yaml

import atmesh.constants as cs

ATMESH_PROMPT: Final[str] = cs.Constants.module_prompt


class Recipe(NamedTuple):
    """The user input yml recipe as a NamedTuple."""

    exodus_input_mesh: Path
    delete_blocks: list[int]


def cubit_delete_blocks(*, yml_input_file: Path) -> int:
    """Given a yml recipe input file that specifies an Exodus input
    file, deletes blocks specified, and then writes out a new Exodus
    file without the deleted block.

    Arguments:
        input_file: The .yml recipe that specifies path variables.
            See the schema in the `Recipe(NamedTuple)` for keys, values,
            and types.

    Returns:
        The error code from the Sculpt subprocess call, which is 0
        if successful.
    """
    print(f"{ATMESH_PROMPT} This is {Path(__file__).resolve()}")

    fin = yml_input_file.expanduser()

    print(f"{ATMESH_PROMPT} Processing file: {yml_input_file}")

    if not fin.is_file():
        raise FileNotFoundError(f"{ATMESH_PROMPT} File not found: {str(fin)}")

    # Compared to the lower() method, the casefold() method is stronger.
    # It will convert more characters into lower case, and will find more
    # matches on comparison of two strings that are both are converted
    # using the casefold() method.
    file_type = fin.suffix.casefold()
    supported_types = (".yaml", ".yml")

    if file_type not in supported_types:
        raise TypeError(
            f"{ATMESH_PROMPT} Only file types .yaml, and .yml are supported."
        )

    yml_db = []

    try:
        with open(file=fin, mode="r", encoding="utf-8") as stream:
            yml_db = yaml.load(stream, Loader=yaml.SafeLoader)  # overwrite
    except yaml.YAMLError as error:
        print(f"{ATMESH_PROMPT} Error with yml module: {error}")
        print(f"{ATMESH_PROMPT} Could not open or decode: {fin}")
        raise OSError from error

    ss = f"{ATMESH_PROMPT} "
    ss += f"Success: database created from file: {yml_input_file}"
    print(ss)
    print(yml_db)

    recipe = Recipe(
        exodus_input_mesh=Path(yml_db["exodus_input_mesh"]).expanduser(),
        delete_blocks=yml_db["delete_blocks"],
    )

    ss_err = f"Cannot find {recipe.exodus_input_mesh}"
    assert recipe.exodus_input_mesh.is_file(), ss_err

    assert isinstance(recipe.delete_blocks, list)

    return 0  # 0 is a success


def main():
    """Runs the module from the command line."""
    print(cs.BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml recipe")
    args = parser.parse_args()
    input_file = args.input_file
    input_file = Path(input_file).expanduser()

    breakpoint()

    cubit_delete_blocks(yml_input_file=input_file)


if __name__ == "__main__":
    main()
