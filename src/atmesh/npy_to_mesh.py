"""Converts a semantic segmentation inot a finite element mesh.

Requirements:
    Python 3.11
    Sculpt 16.10

Methods:
    cd ~/autotwin/mesh

    # Interactive method
    source .venv/bin/activate.fish
    python --version # e.g., Python 3.11.9
    python src/atmesh/npy_to_mesh.py tests/files/letter_f_autotwin.yml
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

ATMESH_PROMPT: Final[str] = cs.Constants.module_prompt


class Recipe(NamedTuple):
    """The user input yml recipe as a NamedTuple."""

    sculpt_binary: Path
    npy_input: Path
    scale_x: float
    scale_y: float
    scale_z: float
    translate_x: float
    translate_y: float
    translate_z: float
    yml_schema_version: float


def npy_to_spn(*, npy_input_file: Path) -> Path:
    """Converts a .npy 3D semantic segmentation file into a .spn file.

    Arguments:
        input_file: The .npy 3D semantic segmentation

    Returns:
        Path of the output .spn file.
    """
    fin = npy_input_file.expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{ATMESH_PROMPT} File not found: {str(fin)}")

    db = np.load(file=fin)

    flattened = db.flatten()
    output_file = npy_input_file.parent.joinpath(npy_input_file.stem + ".spn")
    np.savetxt(fname=output_file, X=flattened, fmt="%s")
    print(f"{ATMESH_PROMPT} Saved spn file: {output_file}")
    return output_file


def npy_to_sculpt_input_file(*, input_file: Path) -> Path:
    """Converts a .npy file 3D semantic segmentation file into a Sculpt input
    .i file.

    Arguments:
        input_file: The .npy 3D semantic segmentation

    Returns:
        Path of the output .i file.
    """
    print(f"{ATMESH_PROMPT} This is {Path(__file__).resolve()}")

    fin = input_file.expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{ATMESH_PROMPT} File not found: {str(fin)}")

    db = np.load(file=fin)
    z, y, x = db.shape

    # build the Sculpt input file line by line
    si = "BEGIN SCULPT\n"
    si += f"  nelx = {x}\n"
    si += f"  nely = {y}\n"
    si += f"  nelz = {z}\n"
    si += "  stair = 1\n"
    spn_file = input_file.parent.joinpath(input_file.stem + ".spn")
    si += f"  input_spn = {spn_file}\n"
    exo_file = input_file.parent.joinpath(input_file.stem)
    si += f"  exodus_file = {exo_file}\n"
    si += "  spn_xyz_order = 5\n"
    si += "END SCULPT\n"

    output_file = input_file.parent.joinpath(input_file.stem + ".i")

    with open(output_file, mode="wt", encoding="utf=8") as fo:
        fo.write(si)

    return output_file


def process(*, yml_input_file: Path) -> int:
    """Given a yml recipe input file that specifies a path to a semantic
    segmentation .npy file, creates a intermediate .spn and Sculpt .i files, and
    creates an output Exodus mesh file.

    * Given the <file>.npy specified in the yml, creates a <file>.spn.
    * Given the <file>.npy specified in the yml and the created <file>.spn file,
        creates a <file>.i Sculpt input file.
    * Runs Sculpt via the command: sculpt -i <file>.i

    process(yml(npy)->spn, yml(npy)->i) -> .e

    Arguments:
        input_file: The .yml recipe that specifies path variables.
            See the schema in the `Recipe(NamedTuple)` for key values
            and types.

    process(yml(npy)->spn, yml(npy)->i) -> .e

    Returns:
        The error code from the subprocess call, which is 0 if successful.
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

    print(f"{ATMESH_PROMPT} Success: database created from file: {yml_input_file}")
    print(yml_db)
    # print("key, value, type")
    # print("---, -----, ----")
    # for key, value in yml_db.items():
    #     print(f"{key}, {value}, {type(value)}")

    recipe = Recipe(
        sculpt_binary=Path(yml_db["sculpt_binary"]).expanduser(),
        npy_input=Path(yml_db["npy_input"]).expanduser(),
        scale_x=yml_db["scale_x"],
        scale_y=yml_db["scale_y"],
        scale_z=yml_db["scale_z"],
        translate_x=yml_db["translate_x"],
        translate_y=yml_db["translate_y"],
        translate_z=yml_db["translate_z"],
        yml_schema_version=yml_db["yml_schema_version"],
    )

    # create the .spn file
    path_spn = npy_to_spn(npy_input_file=recipe.npy_input)

    # create the Sculpt input .i file
    db = np.load(file=recipe.npy_input)
    z, y, x = db.shape

    # build the Sculpt input ("si") .i file line by line
    si = "BEGIN SCULPT\n"
    si += f"  nelx = {x}\n"
    si += f"  nely = {y}\n"
    si += f"  nelz = {z}\n"
    si += f"  xscale = {recipe.scale_x}\n"
    si += f"  yscale = {recipe.scale_y}\n"
    si += f"  zscale = {recipe.scale_z}\n"
    si += f"  xtranslate = {recipe.translate_x}\n"
    si += f"  ytranslate = {recipe.translate_y}\n"
    si += f"  ztranslate = {recipe.translate_z}\n"
    si += "  gen_sidesets = variable\n"
    si += "  stair = 1\n"
    si += f"  input_spn = {path_spn}\n"
    si += f"  exodus_file = {yml_input_file.parent.joinpath(yml_input_file.stem).expanduser()}\n"
    si += "  spn_xyz_order = 5\n"
    si += "END SCULPT\n"

    path_sculpt_i = yml_input_file.parent.joinpath(
        yml_input_file.stem + ".i"
    ).expanduser()
    assert path_sculpt_i.is_file(), f"{ATMESH_PROMPT} Could not find {path_sculpt_i}"

    with open(path_sculpt_i, mode="wt", encoding="utf=8") as fo:
        fo.write(si)
    print(f"{ATMESH_PROMPT} Saved Sculpt input .i file: {path_sculpt_i}")

    for item in [recipe.sculpt_binary, recipe.npy_input, path_spn, path_sculpt_i]:
        assert item.is_file(), f"{ATMESH_PROMPT} Could not find {item}"

    # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
    cc = [str(recipe.sculpt_binary), "-i", str(path_sculpt_i)]
    # subprocess.run(sculpt_command, check=True)
    # subprocess.run(sculpt_command)
    result = subprocess.run(cc)

    return result.returncode


# quick testing:
II = "~/autotwin/mesh/tests/files/letter_f_autotwin.yml"
process(yml_input_file=Path(II))


def main():
    """Runs the module from the command line."""
    print(cs.BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml npy to mesh recipe")
    args = parser.parse_args()
    input_file = args.input_file
    input_file = Path(input_file).expanduser()

    process(yml_input_file=input_file)


if __name__ == "__main__":
    main()
