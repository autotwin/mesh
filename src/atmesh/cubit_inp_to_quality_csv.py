"""This module uses Cubit to convert an ABAQUS .inp file to an assessment
of quality metric for one or more of the following:
    "aspect ratio"
    "scaled jacobian"
    "skew"

Prerequisites:
* Cubit 16.10 (Cubit 16.08 was deprecated on 2023-03-13)
* Python 3.11 (Python 3.7 was deprecated on 2023-03-13)

Methods (example):
> cd ~/autotwin/mesh
~/autotwin/mesh> source .venv/bin/activate.fish # uses Python 3.11
(.venv) ~/autotwin/mesh> arch -x86_64 python src/atmesh/cubit_inp_to_minsj_csv.py tests/files/sphere_minsj.yml

(.venv) ~/autotwin/mesh> arch -x86_64 python src/atmesh/cubit_inp_to_quality_csv.py --help
usage: cubit_inp_to_quality_csv.py [-h] input_file

positional arguments:
  input_file      the .yml user input file

options:
  -h, --help      show this help message and exit

Reference:
Cubit Python Interface at Coreform
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
from typing import Final

import atmesh.yml_to_dict as translator
import atmesh.command_line as cl
import atmesh.constants as cs


def translate(*, path_file_input: str) -> int:
    """Given a fully qualified path to a .yml input file,
    converts an the input .inp file (specified in the input file)
    to the output .csv file (also specified in the input file) that
    contains the element number and the element quality metric
    (e.g., minimum scaled Jacobian) in comma separated value format.

    Returns:
        (int) The number of elements processed.
    """

    atmesh: Final[str] = cs.Constants.module_prompt

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin: Final[Path] = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    keys = ("cubit_path", "inp_path_file", "qualities", "version", "working_dir")
    user_input = translator.yml_to_dict(
        yml_path_file=fin, version=cl.yml_version(), required_keys=keys
    )

    quality_metrics = user_input["qualities"]

    known_metrics = ("aspect ratio", "scaled jacobian", "skew")
    for qm in quality_metrics:
        if qm not in known_metrics:
            raise ValueError(
                f"{atmesh} Unknown quality_metric '{qm}'. Must be one of the following: {known_metrics}."
            )

    print(f"{atmesh} User input:")
    for key, value in user_input.items():
        print(f"  {key}: {value}")

    cubit_path = user_input["cubit_path"]

    working_dir = user_input["working_dir"]
    working_dir_str = str(Path(working_dir).expanduser())

    inp_path_file = user_input["inp_path_file"]
    inp_path_file_Path: Final[Path] = Path(inp_path_file).expanduser()
    inp_path_file_stem: Final[str] = inp_path_file_Path.stem
    inp_path_file_Path_Parent: Final[Path] = inp_path_file_Path.parent
    inp_path_file_str = str(Path(inp_path_file).expanduser())

    # csv_path_file = user_input["csv_path_file"]
    # csv_path_file_str = str(Path(csv_path_file).expanduser())

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

        for qm in quality_metrics:
            print(f"{atmesh} Processing quality metric: {qm}")

            # csv_path_file = user_input["csv_path_file"]
            csv_path_file_str = (
                str(inp_path_file_Path_Parent.joinpath(inp_path_file_stem))
                + "_"
                + qm
                + ".csv"
            ).replace(" ", "_")

            qualities = []  # empty list to start

            with open(csv_path_file_str, "wt") as out_stream:
                print(f"{atmesh} Opened output file for writing: {csv_path_file_str}")

                # for i in np.arange(10):
                # for i in np.arange(n_elements):
                for i in range(n_elements):
                    en = i + 1  # element number = en, change from 0-index to 1-index
                    # print(f"Element {en}")
                    quality = cubit.get_quality_value("hex", int(en), qm)
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
    # Deprecate quality as a command line input.  Instead, quality is an input
    # in the yml input file:
    # parser.add_argument(
    #     "quality_metrics",
    #     help="tuple of quality strings from ('aspect ratio', 'scaled jacobian', 'skew')",
    # )
    args = parser.parse_args()
    # input_file = args.input_file

    # translate(path_file_input=args.input_file, quality_metrics=args.quality_metric)
    translate(path_file_input=args.input_file)


if __name__ == "__main__":
    main()
