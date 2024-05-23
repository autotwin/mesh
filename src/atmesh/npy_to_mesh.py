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
from typing import Final, NamedTuple

import yaml

# import atmesh.yml_to_dict as translator
# import atmesh.command_line as cl
import atmesh.constants as cs


class Cubit(NamedTuple):
    """A data interface for running Sculpt via Cubit."""

    binary: Path
    input_spn: Path
    journaling: bool
    nelx: int
    nely: int
    nelz: int
    output_exodus_mesh: Path
    output_abaqus_mesh: Path
    scratch: Path
    spn_xyz_order: int  # make this an enum once types are known
    stair: int  # make this an enum once the types are known


class Recipe(NamedTuple):
    """The user input yml recipe as a NamedTuple."""

    cubit: Cubit
    yml_schema_version: float


def process(*, input_file: Path):
    """Converts the semantic segmentation saved in a
    .npy file into a finite element mesh.

    Arguments:
        input: The .yml recipe.

    """

    atmesh: Final[str] = cs.Constants.module_prompt

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = input_file.expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    db = []

    try:
        with open(file=fin, mode="r", encoding="utf-8") as stream:
            db = yaml.load(stream, Loader=yaml.SafeLoader)  # overwrite
    except yaml.YAMLError as error:
        print(f"Error with yml module: {error}")
        print(f"Could not open or decode: {fin}")
        raise OSError from error

    cc = Cubit(
        binary=db["cubit"]["binary"],
        input_spn=db["cubit"]["input_spn"],
        journaling=db["cubit"]["journaling"],
        nelx=db["cubit"]["nelx"],
        nely=db["cubit"]["nely"],
        nelz=db["cubit"]["nelz"],
        output_abaqus_mesh=db["cubit"]["output_abaqus_mesh"],
        output_exodus_mesh=db["cubit"]["output_exodus_mesh"],
        scratch=db["cubit"]["scratch"],
        spn_xyz_order=db["cubit"]["spn_xyz_order"],
        stair=db["cubit"]["stair"],
    )

    rc = Recipe(cubit=cc, yml_schema_version=db["yml_schema_version"])
    breakpoint()
    aa = 4


process(input_file=Path("~/autotwin/mesh/tests/files/letter_f.yml"))


def main():
    """Runs the module from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml user input file")
    args = parser.parse_args()
    input_file = args.input_file
    input_file = Path(input_file).expanduser()

    breakpoint()

    process(input=input_file)
