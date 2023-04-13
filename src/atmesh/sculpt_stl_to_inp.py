"""This module uses Cubit to convert one or more .stl file into a .inp file
Cubit's Sculpt functionality.

Prerequisites:
* ~~Python 3.7.4 is required to run Cubit 16.08 and Sculpt.~~
* ~~We actually use Python 3.7.9 successfully for now.~~
* 2023-03-03: Upgrade to Sculpt 16.10, and use with Python 3.11

Methods:
> cd ~/autotwin/mesh/src/atmesh

* Interactive Method
# > /usr/local/bin/python3.11 sculpt_stl_to_inp.py <input_file>.yml
> python --version
  Python 3.11.2
> python sculpt_stl_to_inp.py <input_file>.yml

* Log Method
# > /usr/local/bin/python3.11 sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log
> python sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log

Example 1:
# activate the atmesh virtual environment
~/autotwin/mesh> source atmeshenv/bin/activate.fish # (.venv) uses Python 3.11
(.venv) ~/autotwin/mesh> python src/atmesh/sculpt_stl_to_inp.py tests/files/sphere.yml

Example 2:
# uses the same venv
(.venv) ~/autotwin/mesh> python src/atmesh/sculpt_stl_to_inp.py ../data/octa/octa_loop00.yml
"""

import argparse
from pathlib import Path
import sys
from typing import Final

import atmesh.yml_to_dict as translator
import atmesh.command_line as cl


def translate(*, path_file_input: str) -> bool:
    completed = False
    # from typing import Final # Final is new in Python 3.8, Cubit uses 3.7

    atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    # atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7

    # Input .yml files must be of a minimum version:
    # mininum_yml_version: Final[float] = 1.5

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    # user_input = _yml_to_dict(yml_path_file=fin)
    keys = (
        "version",
        "cubit_path",
        "working_dir",
        "stl_path_files",
        "inp_path_file",
        "cell_size",
        "bounding_box",
    )
    user_input = translator.yml_to_dict(
        yml_path_file=fin, version=cl.yml_version(), required_keys=keys
    )

    print(f"{atmesh} User input:")
    for key, value in user_input.items():
        print(f"  {key}: {value}")

    cubit_path = user_input["cubit_path"]
    inp_path_file = user_input["inp_path_file"]
    stl_path_files = user_input["stl_path_files"]
    working_dir = user_input["working_dir"]
    working_dir_str = str(Path(working_dir).expanduser())
    cell_size = float(user_input["cell_size"])

    journaling: bool = user_input.get("journaling", False)
    n_proc_default: Final[int] = 4
    # number of parallel processors
    n_proc: int = user_input.get("n_proc", n_proc_default)

    if cell_size <= 0.0:
        raise ValueError(f"cell_size {cell_size} must be positive")

    for item in [cubit_path, working_dir]:
        if not Path(item).expanduser().is_dir():
            raise OSError(f"{atmesh} Path not found: {item}")

    if not (isinstance(stl_path_files, list)):
        raise TypeError(
            f"{atmesh} stl_path_file value must be a list of one or more string paths"
        )

    for item in stl_path_files:
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

        if journaling:
            cubit.init
            print(f"{atmesh} Import cubit module completed.  Journaling is ON.")
        else:
            cubit.init(["cubit", "-nojournal"])
            print(f"{atmesh} Import cubit module completed.  Journaling is OFF.")

        # Examples:
        # cubit.cmd('cd "~/sibl-dev/sculpt/tests/sphere-python"')
        # cubit.cmd('cd "~/Downloads/scratch/Utah_SCI_brain"')
        cc = 'cd "' + working_dir_str + '"'
        cubit.cmd(cc)
        print(f"{atmesh} The Cubit Working Directory is set to: {working_dir_str}")

        print(f"{atmesh} stl import initiatied:")
        for stl_file in stl_path_files:
            print(f"{atmesh} Importing stl file: {stl_file}")
            # cc = 'import stl "' + stl_file + '"' + " feature_angle 135.0 merge"
            cc = 'import stl "' + stl_file + '" feature_angle 135.0 merge'
            cubit.cmd(cc)
        print(f"{atmesh} stl import completed.")

        """Sculpt invocation
        Default:
        Input: /Applications/Cubit-16.06/Cubit.app/Contents/MacOS/psculpt
          --num_procs   -j  4
          --diatom_file -d  sculpt_parallel.diatom
          --exodus_file -e  sculpt_parallel.diatom_result
          --nelx        -x  26
          --nely        -y  26
          --nelz        -z  26
          --xmin        -t  -0.624136
          --ymin        -u  -0.624091
          --zmin        -v  -0.624146
          --xmax        -q  0.624042
          --ymax        -r  0.624087
          --zmax        -s  0.624033
        """

        print(f"{atmesh} Sculpt parallel initiated:")
        # cc = "sculpt parallel"
        # cc = "sculpt parallel processors 3"
        # cc = "sculpt parallel processors 2"
        # cc = "sculpt parallel processors "
        # cc = f"sculpt parallel -j {n_proc}"
        # cc = f"sculpt parallel processors {n_proc}"
        #
        # Generate Sidesets
        # Input file command:   gen_sidesets <arg>
        # Command line options: -SS <arg>
        # Argument Type:        integer (0, 1, 2, 3, 4, 5)
        # Input arguments: off (0)
        #                  fixed (1)
        #                  variable (2)
        #                  geometric_surfaces (3)
        #                  geometric_sidesets (4)
        #                  rve (5)
        #                  input_mesh_and_stl (6)
        #                  input_mesh_and_free_surfaces (7)
        #                  rve_variable (8)
        #                  input_mesh (9)
        enum_variable_sidesets: Final[int] = 2
        cc = (
            f"sculpt parallel processors {n_proc} gen_sidesets {enum_variable_sidesets}"
        )

        # if bounding_box is specified in the .yml input file
        if "bounding_box" in user_input:
            bounding_box = user_input["bounding_box"]
            # nx = cell_count["nx"]
            # ny = cell_count["ny"]
            # nz = cell_count["nz"]

            # cc += f" nelx {nx} nely {ny} nelz {nz}"

            cc += f" size {cell_size}"

            xmin = bounding_box["xmin"]
            xmax = bounding_box["xmax"]

            ymin = bounding_box["ymin"]
            ymax = bounding_box["ymax"]

            zmin = bounding_box["zmin"]
            zmax = bounding_box["zmax"]

            cc += f" box location position {xmin} {ymin} {zmin} location position {xmax} {ymax} {zmax}"

        # TODO: adapativity.
        # Adapt Type
        # Input arguments:
        #   Facet to Surface Distance (1)
        #   Surface to Facet Distance (2)
        #   Surface to Surface (3)
        #   Volume Fraction Average (4)
        #   Coarsen (5)
        #   Volume Fraction Difference (6)
        #   Resample (7)
        #   Material (8)
        # Default Threshold
        # Theshold Distance
        # Max Levels (Defaults to 2)

        print(f"{atmesh} Invoking Sculpt with Cubit command: {cc}")
        cubit.cmd(cc)
        print(f"{atmesh} Sculpt parallel completed.")

        # Get all volume entities
        # References:

        # https://coreform.com/cubit_help/appendix/python/namespace_cubit_interface.htm#ad0f2fc80640e66eea7b652ea43117a32

        # https://coreform.com/cubit_help/appendix/python/class_cubit_interface_1_1_entity.htm

        # https://coreform.com/cubit_help/appendix/python/namespace_cubit_interface.htm

        # https://coreform.com/cubit_help/cubithelp.htm#t=finite_element_model%2Fexodus%2Fnodesets_and_sidesets.htm

        # volume_ids = cubit.get_entities("volume")
        # surface_ids = cubit.get_entities("surface")
        sideset_ids = cubit.get_entities("sideset")

        for item in sideset_ids:
            # cc = 'nodeset 1 add surface 1'
            # cc = f"nodeset {item} add surface {item}"  # 2022-11-16 <-----
            # create a group, then create a nodeset from that group
            # cc = f"nodeset {item} block {item}"  # 2022-11-16
            cc = f"nodeset {item} add node in face in sideset {item}"  # 2022-11-21
            # nodeset 1 add  node in face in sideset 1
            cubit.cmd(cc)
            print(f"{atmesh} Completed: {cc}")

        # assert cubit.get_entity_name("volume", 1) == "Volume 1"

        # block_ids = cubit.get_entities("block")
        # # assert block_ids == (1,)
        # n_blocks = cubit.get_block_count()
        # n_nodesets = cubit.get_nodeset_count()

        print(f"{atmesh} Abaqus file export initiated:")
        print(f"{atmesh} Exporting inp file: {inp_path_file}")
        cc = 'export abaqus "' + inp_path_file + '" overwrite'
        cubit.cmd(cc)
        print(f"{atmesh} Abaqus file export completed.")

        # print(f"{atmesh} Script: {Path(__file__).resolve()} has completed.")
        print(f"{atmesh} Done.")

        completed = True
        return completed

    except ModuleNotFoundError as error:
        print("unable to import cubit")
        print(f"{atmesh} {error}")
        raise ModuleNotFoundError


def main():
    """Runs the module from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the .yml user input file")
    args = parser.parse_args()
    input_file = args.input_file
    translate(path_file_input=input_file)


if __name__ == "__main__":
    main()
