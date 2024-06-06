"""This module takes in an Exodus file, deletes blocks specified, and then
writes out a new Exodus file without the deleted block.

Prerequisite:
* Cubit 16.10
* Python 3.11

Example:
  cd ~/autotwin/mesh
  source .venv/bin/activate.fish
  arch -x86_64 python src/atmesh/cubit_delete_blocks.py tests/files/IXI012-HH-1211-T1_tiny_test.yml
"""

import argparse
from pathlib import Path
import sys
from typing import Final, NamedTuple

import yaml

import atmesh.constants as cs

AT: Final[str] = cs.Constants.module_prompt


class Recipe(NamedTuple):
    """The user input yml recipe as a NamedTuple."""

    cubit_path: Path
    delete_blocks: list[int]
    exodus_input_mesh: Path
    working_dir: Path


def _validate_recipe(*, recipe: Recipe) -> bool:
    """Given a recipe defined by the Recipe type, assure that all values
    are valid.

    Arguments:
        recipe: The Recipie NamedTuple populated with items from the user input
            .yml file.

    Returns:
        True if the recipe is valid, False otherwise.
    """
    ss_err = f"Cannot find {recipe.cubit_path}"
    assert recipe.cubit_path.is_dir(), ss_err

    assert isinstance(recipe.delete_blocks, list)

    ss_err = f"Cannot find {recipe.exodus_input_mesh}"
    assert recipe.exodus_input_mesh.is_file(), ss_err

    ss_err = f"Cannot find {recipe.working_dir}"
    assert recipe.working_dir.is_dir(), ss_err

    return True


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
    print(f"{AT} This is {Path(__file__).resolve()}")

    fin = yml_input_file.expanduser()

    print(f"{AT} Processing file: {yml_input_file}")

    if not fin.is_file():
        raise FileNotFoundError(f"{AT} File not found: {str(fin)}")

    # Compared to the lower() method, the casefold() method is stronger.
    # It will convert more characters into lower case, and will find more
    # matches on comparison of two strings that are both are converted
    # using the casefold() method.
    file_type = fin.suffix.casefold()
    supported_types = (".yaml", ".yml")

    if file_type not in supported_types:
        raise TypeError(f"{AT} Only file types .yaml, and .yml are supported.")

    yml_db = []

    try:
        with open(file=fin, mode="r", encoding="utf-8") as stream:
            yml_db = yaml.load(stream, Loader=yaml.SafeLoader)  # overwrite
    except yaml.YAMLError as error:
        print(f"{AT} Error with yml module: {error}")
        print(f"{AT} Could not open or decode: {fin}")
        raise OSError from error

    ss = f"{AT} "
    ss += f"Success: database created from file: {yml_input_file}"
    print(ss)
    print(yml_db)

    recipe = Recipe(
        cubit_path=Path(yml_db["cubit_path"]).expanduser(),
        delete_blocks=yml_db["delete_blocks"],
        exodus_input_mesh=Path(yml_db["exodus_input_mesh"]).expanduser(),
        working_dir=Path(yml_db["working_dir"]).expanduser(),
    )

    _validate_recipe(recipe=recipe)

    try:
        print(f"{AT} Attempting to import Cubit Python interface...")
        sys.path.append(str(recipe.cubit_path))

        import cubit

        cubit.init

        ss = f"{AT} Success: Cubit Python interface loaded. "
        ss += "Journaling is ON."
        print(ss)

        cc = 'cd "' + str(recipe.working_dir) + '"'
        cubit.cmd(cc)
        print(f"{AT} Set Cubit working directory: {recipe.working_dir}")

        # delete blocks
        # cc = f'import mesh "{recipe.exodus_input_mesh}" feature_angle 135.00  merge'
        # cc = f'import mesh "{recipe.exodus_input_mesh}" lite'
        cc = f'import mesh "{recipe.exodus_input_mesh}" no_geom'
        cubit.cmd(cc)
        print(f"{AT} Cubit opened: {recipe.exodus_input_mesh}")

        for item in recipe.delete_blocks:
            cc = f"delete block {item}"
            print(f"Processed Cubit command: {cc}")

        # output new mesh
        ff = recipe.exodus_input_mesh.stem
        # gg = ff.replace(".e", "_v2.e")
        gg = ff.split(".")[0] + "_v2.e"
        exodus_output = recipe.exodus_input_mesh.parent.joinpath(gg)

        cubit.cmd("set exodus netcdf4 off")
        cubit.cmd("set large exodus file on")

        cc = f'export mesh "{exodus_output}" overwrite'
        cubit.cmd(cc)
        print(f"{AT} Cubit saved: {exodus_output}")

        print(f"{AT} Done.")
        return 0  # 0 is a success

    except ModuleNotFoundError as error:
        print(f"{AT} Failed to import Cubit Python interface.")
        print(f"{AT} {error}")
        raise ModuleNotFoundError from error

    return 1  # failed to process


def main():
    """Runs the module from the command line."""
    print(cs.BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml recipe")
    args = parser.parse_args()
    input_file = args.input_file
    input_file = Path(input_file).expanduser()

    cubit_delete_blocks(yml_input_file=input_file)


if __name__ == "__main__":
    main()
