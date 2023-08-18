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
> arch -x86_64 python sculpt_stl_to_inp.py <input_file>.yml

* Log Method
# > /usr/local/bin/python3.11 sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log
> arch -x86_64 python sculpt_stl_to_inp.py <input_file>.yml > sculpt_stl_to_inp.log

Example 1:
# activate the virtual environment
~/autotwin/mesh> source .venv/bin/activate.fish # (.venv) uses Python 3.11
(.venv) ~/autotwin/mesh> arch -x86_64 python src/atmesh/sculpt_stl_to_inp.py tests/files/sphere.yml

Example 2:
# uses the same venv
(.venv) ~/autotwin/mesh> arch -x86_64 python src/atmesh/sculpt_stl_to_inp.py ../data/octa/octa_loop00.yml
"""

import argparse
from pathlib import Path
import sys
from typing import Final

import atmesh.yml_to_dict as translator
import atmesh.command_line as cl
import atmesh.constants as cs


def translate(*, path_file_input: str) -> bool:
    completed = False

    atmesh: Final[str] = cs.Constants.module_prompt

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    # user_input = _yml_to_dict(yml_path_file=fin)
    keys = (
        "bounding_box",
        "cell_size",
        "cubit_path",
        "inp_path_file",
        "stl_path_files",
        "working_dir",
        "version",
    )
    user_input = translator.yml_to_dict(
        yml_path_file=fin, version=cl.yml_version(), required_keys=keys
    )

    # Support input files of version 1.7 or later only.
    min_input_version: Final[float] = 1.7

    if user_input["version"] < min_input_version:
        raise ValueError(
            f"{atmesh} Error: Input file must be of version {min_input_version} or greater."
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

    n_proc_default: Final[int] = 4
    # number of parallel processors
    n_proc: int = user_input.get("n_proc", n_proc_default)

    # If 'jounnaling is present, then echo the commands to a journal file.
    journaling: bool = user_input.get("journaling", False)

    # Version 1.8 implements a stair-step mesh.  For backward compatibility with
    # version 1.7, make the default value for star_step = False.
    stair_step: bool = user_input.get("stair_step", False)

    # If the 'stl_scale_factor' is present, scale the stl objects
    # by that amount, otherwise, do nothing.
    stl_scale_factor: float = user_input.get("stl_scale_factor", 1.0)

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
            cc = 'import stl "' + stl_file + '" feature_angle 135.0 merge'  # overwrite
            cubit.cmd(cc)
        print(f"{atmesh} stl import completed.")

        print(f"{atmesh} Scale up/down applied to the STL file")
        if stl_scale_factor == 1.0:
            print(f"{atmesh} is none (equalivalent to scaleing of 1.0).")
        else:
            print(f"{atmesh} as 'stl_scale_factor' is {stl_scale_factor}")
            cc = "volume all scale " + str(stl_scale_factor)
            cubit.cmd(cc)
            print("f{atmesh} finished STL scaling.")

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

        cc += f" size {cell_size}"

        # if bounding_box is specified in the .yml input file
        # if "bounding_box" in user_input:
        bounding_box = user_input["bounding_box"]
        # bounding_box_auto_generated = bounding_box["auto"]
        bounding_box_auto_generated: bool = bounding_box.get("auto", True)

        # breakpoint()

        if not bounding_box_auto_generated:
            # nx = cell_count["nx"]
            # ny = cell_count["ny"]
            # nz = cell_count["nz"]
            # cc += f" nelx {nx} nely {ny} nelz {nz}"

            xmin = bounding_box["xmin"]
            xmax = bounding_box["xmax"]

            ymin = bounding_box["ymin"]
            ymax = bounding_box["ymax"]

            zmin = bounding_box["zmin"]
            zmax = bounding_box["zmax"]

            cc += f" box location position {xmin} {ymin} {zmin} location position {xmax} {ymax} {zmax}"

        # breakpoint()

        # bounding_box_defeatured = bounding_box["defeatured"]
        bounding_box_defeatured: bool = bounding_box.get("defeatured", False)

        if bounding_box_defeatured:
            cc += " defeature 1 defeature_bbox"

        # breakpoint()

        if stair_step:

            # Build an all voxel-style mesh (aka "sugar cube" mesh).
            # This is a Lagrangian mesh in Eulerian form.
            cc += " stair 1"

        else:
            # Not a voxelized mesh, rather a standard Lagrangian mesh that
            # follows the curvature of a body.

            # journaling: bool = user_input.get("journaling", False)
            b_mesh_adaptivity: bool = user_input.get("mesh_adaptivity", False)

            if b_mesh_adaptivity:
                b_adapt_levels: bool = user_input["mesh_adaptivity"].get(
                    "adapt_levels", False
                )
                b_adapt_type: bool = user_input["mesh_adaptivity"].get(
                    "adapt_type", False
                )
            else:
                b_adapt_levels = False
                b_adapt_type = False

            if b_mesh_adaptivity and b_adapt_levels and b_adapt_type:
                print(f"{atmesh} Mesh adaptivity specified.")

                cc += " adapt_levels " + str(
                    user_input["mesh_adaptivity"]["adapt_levels"]
                )
                cc += " adapt_type " + str(user_input["mesh_adaptivity"]["adapt_type"])
                # Adaptive Meshing
                # Adapt Mesh Size: Boolean, default to False
                #   True:
                #     Adapt Type:
                #       Facet to Surface Distance (1)
                #       Surface to Facet Distance (2)
                #       Surface to Surface (3)
                #       Volume Fraction Average (4)
                #       Coarsen (5)
                #       Volume Fraction Difference (6)
                #       Resample (7)
                #       Material (8)
                #     Default Threshold: Boolean, default to True - maintain as True for now.
                #       If False, then Threshold Distance (float?)
                #     Theshold Distance
                #     Max Levels (Defaults to 2) (int)

            else:
                print(f"{atmesh} Mesh adaptivity not specified; or,")
                print(f"{atmesh} one or more missing keys/value pairs.  Required keys")
                print(f"{atmesh} for adaptivity: 'mesh_adaptivity', 'adapt_levels',")
                print(f"{atmesh} and 'adapt_type'.")

            # if (
            #     (user_input.get("mesh_adaptivity"), False)
            #     and user_input["mesh_adaptivity"].get("adapt_levels", False)
            #     and user_input["mesh_adaptivity"].get("adapt_type", False)
            # ):
            #     print("Version 1.7 or greater with mesh_adaptivity")
            #     cc += " adapt_levels " + str(
            #         user_input["mesh_adaptivity"]["adapt_levels"]
            #     )
            #     cc += " adapt_type " + str(user_input["mesh_adaptivity"]["adapt_type"])
            #     # Adaptive Meshing
            #     # Adapt Mesh Size: Boolean, default to False
            #     #   True:
            #     #     Adapt Type:
            #     #       Facet to Surface Distance (1)
            #     #       Surface to Facet Distance (2)
            #     #       Surface to Surface (3)
            #     #       Volume Fraction Average (4)
            #     #       Coarsen (5)
            #     #       Volume Fraction Difference (6)
            #     #       Resample (7)
            #     #       Material (8)
            #     #     Default Threshold: Boolean, default to True - maintain as True for now.
            #     #       If False, then Threshold Distance (float?)
            #     #     Theshold Distance
            #     #     Max Levels (Defaults to 2) (int)

            # journaling: bool = user_input.get("journaling", False)
            b_mesh_improvement: bool = user_input.get("mesh_improvement", False)

            if b_mesh_improvement:
                b_pillow_curves: bool = user_input["mesh_improvement"].get(
                    "pillow_curves", False
                )
                b_pillow_curve_layers: bool = user_input["mesh_improvement"].get(
                    "pillow_curve_layers", False
                )
                b_pillow_curve_thresh: bool = user_input["mesh_improvement"].get(
                    "pillow_curve_thresh", False
                )
                b_pillow_surfaces: bool = user_input["mesh_improvement"].get(
                    "pillow_surfaces", False
                )
            else:
                b_pillow_curves = False
                b_pillow_curve_layers = False
                b_pillow_curve_thresh = False
                b_pillow_surfaces = False

            if (
                b_mesh_improvement
                and b_pillow_curves
                and b_pillow_curve_layers
                and b_pillow_curve_thresh
                and b_pillow_surfaces
            ):
                print(f"{atmesh} Mesh improvement specified.")

                cc += " pillow_curves"
                cc += " pillow_curve_layers " + str(
                    user_input["mesh_improvement"]["pillow_curve_layers"]
                )
                cc += " pillow_curve_thresh " + str(
                    user_input["mesh_improvement"]["pillow_curve_thresh"]
                )

                # breakpoint()

                # TODO: Mesh Improvement
                # pillow_surfaces
                # pillow_curves
                # pillow_curve_layers 3 (int, default=3)
                # pillow_curve_thresh 0.3 (float, default=0.3)
                # Cubit>sculpt volume all processors 3 pillow_surfaces pillow_curves pillow_curve_layers 10 pillow_curve_thresh 0.32

            else:
                print(f"{atmesh} Mesh improvement not specified; or,.")
                print(f"{atmesh} one or more missing key/value pairs.  Required keys")
                print(f"{atmesh} for improvement: 'mesh_improvement', 'pillow_curves',")
                print(f"{atmesh} 'pillow_curve_layers', 'pillow_curve_thresh', .")
                print(f"{atmesh} and 'pillow_surfaces'.")

            # if user_input.get("mesh_improvement", False) and user_input.get(
            #     "pillow_surfaces", False
            # ):
            #     print("Version 1.7 or greater with pillow_surfaces")
            #     cc += " pillow_surfaces"

            # if (
            #     (user_input.get("mesh_improvement"), False)
            #     and user_input["mesh_improvement"].get("pillow_curves", False)
            #     and user_input["mesh_improvement"].get("pillow_curve_layers", False)
            #     and user_input["mesh_improvement"].get("pillow_curve_thresh", False)
            # ):
            #     print("Version 1.7 or greater with pillow_curves")
            #     cc += " pillow_curves"
            #     cc += " pillow_curve_layers " + str(
            #         user_input["mesh_improvement"]["pillow_curve_layers"]
            #     )
            #     cc += " pillow_curve_thresh " + str(
            #         user_input["mesh_improvement"]["pillow_curve_thresh"]
            #     )

            #     # breakpoint()

            #     # TODO: Mesh Improvement
            #     # pillow_surfaces
            #     # pillow_curves
            #     # pillow_curve_layers 3 (int, default=3)
            #     # pillow_curve_thresh 0.3 (float, default=0.3)
            #     # Cubit>sculpt volume all processors 3 pillow_surfaces pillow_curves pillow_curve_layers 10 pillow_curve_thresh 0.32

        #
        #
        # TODO:
        # Examples:
        # Cubit>Sculpt volume all adapt_type 1 adapt_levels 3
        # Cubit>Sculpt volume all processors 3 adapt_type 3 adapt_levels 3
        # Cubit>sculpt volume all processors 3 pillow_surfaces pillow_curves adapt_type 3 adapt_levels 3
        # Cubit>sculpt volume all processors 3 pillow_surfaces pillow_curves pillow_curve_layers 4 pillow_curve_thresh 0.32 adapt_type 3 adapt_levels 3
        # Cubit>sculpt volume all processors 3 pillow_surfaces pillow_curves pillow_curve_layers 5 pillow_curve_thresh 0.32 adapt_type 3 adapt_levels 3

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

        print(f"{atmesh} Abaqus mesh file export initiated:")
        print(f"{atmesh} Exporting .inp file: {inp_path_file}")
        cc = 'export abaqus "' + inp_path_file + '" overwrite'
        cubit.cmd(cc)
        print(f"{atmesh} Abaqus mesh file export completed.")

        # breakpoint()

        # Remove the .inp file extension, replace with .g extension
        inp_path_file_genesis = inp_path_file.replace(".inp", ".g")

        print(f"{atmesh} Genesis mesh file export initiated:")
        print(f"{atmesh} Exporting .g file: {inp_path_file_genesis}")
        cc = 'export mesh "' + inp_path_file_genesis + '" overwrite'
        cubit.cmd(cc)
        print(f"{atmesh} Genesis mesh file export completed.")

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
