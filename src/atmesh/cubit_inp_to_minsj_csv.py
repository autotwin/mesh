"""This module uses Cubit to convert a .inp file to an assessment
of minimum scaled Jacobian of the mesh.

Prerequisites:
* Cubit 16.08
* Python 3.7.x

Methods (example):
> cd ~/autotwin/mesh/src/mesh
~/autotwin/mesh> source atmeshenv/bin/activate.fish # (atmeshenv) uses Python 3.7
(atmeshenv) ~/autotwin/mesh> python src/atmesh/cubit_inp_to_minsj_csv.py tests/files/sphere_minsj.yml

Reference:
Cubit Python Interface at Corform
https://coreform.com/cubit_help/cubithelp.htm?#t=appendix%2Fpython%2Fnamespace_cubit_interface.htm
get_elem_quality_stats()
std::vector<double> CubitInterface::get_elem_quality_stats(const std::string& entity_type,
    const std::vector< int >  id_list,
    const std::string&  metric_name,
    const double  single_threshold,
    const bool  use_low_threshold,
    const double  low_threshold,
    const double  high_threshold,
    const bool  make_group
)

Hex metrics:
https://coreform.com/cubit_help/cubithelp.htm?#t=mesh_generation%2Fmesh_quality_assessment%2Fhexahedral_metrics.htm

Examples:
cubit.get_quality_value("hex", int(en), "Scaled Jacobian")
cubit.get_quality_value("hex", int(en), "Element Volume")
"""

import argparse
from pathlib import Path
import sys


import atmesh.yml_to_dict as translator


def translate(*, path_file_input: str) -> int:
    """Given a fully qualified path to a .yml input file, converts
    an the input .inp file (specified in the input file)
    to the output .csv file (also specified in the input file) that
    contains the element number and the element minimum scaled Jacobian
    in comma separated value format.

    Returns:
        (int) The number of elements processed.
    """

    # from typing import Final # Final is new in Python 3.8, Cubit uses 3.7

    # atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    # user_input = _yml_to_dict(yml_path_file=fin)
    # keys = ("version", "cubit_path", "working_dir", "stl_path_file", "inp_path_file")
    keys = ("version", "cubit_path", "working_dir", "inp_path_file", "csv_path_file")
    user_input = translator.yml_to_dict(
        yml_path_file=fin, version=1.1, required_keys=keys
    )

    print(f"{atmesh} User input:")
    for key, value in user_input.items():
        print(f"  {key}: {value}")

    cubit_path = user_input["cubit_path"]

    working_dir = user_input["working_dir"]
    working_dir_str = str(Path(working_dir).expanduser())

    inp_path_file = user_input["inp_path_file"]
    inp_path_file_str = str(Path(inp_path_file).expanduser())

    csv_path_file = user_input["csv_path_file"]
    csv_path_file_str = str(Path(csv_path_file).expanduser())

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

        n_elements = cubit.get_hex_count()
        print(f"{atmesh} Number of elements: {n_elements}")
        print(f"{atmesh} Calculating {n_elements} minimum scaled Jacobian values.")

        quality_metric = "Scaled Jacobian"
        qualities = []  # empty list to start

        with open(csv_path_file_str, "wt") as out_stream:
            print(f"{atmesh} Opened output file for writing: {csv_path_file_str}")

            # for i in np.arange(10):
            # for i in np.arange(n_elements):
            for i in range(n_elements):

                en = i + 1  # element number = en, change from 0-index to 1-index
                # print(f"Element {en}")
                quality = cubit.get_quality_value("hex", int(en), quality_metric)
                # breakpoint()
                qualities.append(quality)
                # print(f"{quality_metric} value: {quality}")
                line_out = str(en) + ", " + str(quality) + "\n"
                out_stream.write(line_out)

        # If we reach this point, the input and output buffers are
        # now closed and the function was successful.
        print(f"{atmesh} Closed output file: {csv_path_file_str}")

        print(f"{atmesh} Done.")

        return n_elements

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
