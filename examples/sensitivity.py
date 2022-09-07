"""This module examines the sensitivity of element minimum scaled
Jacobian ("quality") to changes in `.stl` face count, element count,
Jacobi smoothing iteration, and Laplacian smoothing iteration.

Prerequisites:
* Install of Cubit version 16.06 with Sculpt.
* Install Python 3.7.9.
* Install the atmeshevn virtual environment.
* Clone the autotwin/mesh repo.
* Clone the autotwin/data repo.

To run:
> cd ~/autotwin/mesh

# activate the venv at meshenv
> source atmeshenv/bin/activate  # or activate.fish if using fish shell
> python examples/sensitivity.py

"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():

    cubit_path = "/Applications/Cubit-16.06/Cubit.app/Contents/MacOS"
    working_dir_str = str(Path("~/autotwin/data/octa").expanduser())

    # we will loop over and process the following input files
    stl_path_files = [
        "~/autotwin/data/octa/octa_loop03.stl",
        "~/autotwin/data/octa/octa_loop04.stl",
    ]

    # atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
    # append the cubit path to the system Python path
    print(f"{atmesh} Existing sys.path:")
    for item in sys.path:
        print(f"  {item}")

    sys.path.append(cubit_path)

    print(f"{atmesh} Cubit path now added:")
    for item in sys.path:
        print(f"  {item}")

    import cubit

    cubit.init

    cc = 'cd "' + working_dir_str + '"'
    cubit.cmd(cc)
    print(f"{atmesh} The Cubit Working Directory is set to: {working_dir_str}")

    for file_in in stl_path_files:

        # ----------------
        # user input begin
        # stl_path_file = "~/autotwin/data/octa/octa_loop04.stl"
        stl_path_file = file_in
        fig_dict = {
            "title": "Element Minimum Scaled Jacobian",
            "xlabel": "Minimum Scaled Jacobian",
            "ylabel": "Number of Elements",
            "hist_x": [0.4, 1.0],
            "hist_y": [0.6, 6000],
            "legend_loc": "upper left",
            "height": 6.0,
            "width": 6.0,
            "dpi": 200,
            "serialize": True,
            "figure_shown": False,
        }
        hist_kwargs = {
            # "histtype": "step",
            "alpha": 0.9,
            "linewidth": 2,
            "color": "blue",
        }
        n_bins = 7
        # delta_bin = 1.0 / n_bins
        xmin, xmax = fig_dict["hist_x"]
        delta_bin = (xmax - xmin) / n_bins
        # bins = [delta_bin * x for x in range(n_bins + 1)]
        bins = [xmin + delta_bin * x for x in range(n_bins + 1)]
        # user input end
        # --------------

        print(f"n_bins: {n_bins}")
        print(f"delta_bin: {delta_bin}")
        print(f"bins: {bins}")

        fin = Path(stl_path_file).expanduser()
        input_path = fin.parent
        input_file_no_ext = fin.stem
        output_file = input_file_no_ext + "_sj.csv"
        output_path_file = input_path.joinpath(output_file)
        output_path_file_str = str(output_path_file)

        figure_type = ".png"
        figure_file = input_file_no_ext + "_sj" + figure_type
        figure_path_file = input_path.joinpath(figure_file)

        cc = "reset"
        cubit.cmd(cc)
        print(f"{atmesh} The Cubit session cleared via reset.")

        print(f"{atmesh} stl import initiatied:")
        print(f"{atmesh} Importing stl file: {stl_path_file}")
        cc = 'import stl "' + stl_path_file + '"'
        cubit.cmd(cc)
        print(f"{atmesh} stl import completed.")

        print(f"{atmesh} Sculpt parallel initiated:")
        cc = "sculpt parallel"
        cubit.cmd(cc)
        print(f"{atmesh} Sculpt parallel completed.")

        n_elements = cubit.get_hex_count()
        print(f"Number of elements: {n_elements}")

        quality_metric = "Scaled Jacobian"
        qualities = []  # empty list to start

        with open(output_path_file_str, "wt") as out_stream:
            print(f"{atmesh} Opened output file for writing: {output_path_file_str}")

            # for i in np.arange(10):
            for i in np.arange(n_elements):

                en = i + 1  # element number = en, change from 0-index to 1-index
                # print(f"Element {en}")
                quality = cubit.get_quality_value("hex", int(en), quality_metric)
                qualities.append(quality)
                # print(f"{quality_metric} value: {quality}")
                line_out = str(en) + ", " + str(quality) + "\n"
                out_stream.write(line_out)

        # If we reach this point, the input and output buffers are
        # now closed and the function was successful.
        print(f"{atmesh} Closed output file: {output_path_file_str}")

        # Plot the histogram of minimum scaled Jacobians
        fig = plt.figure(
            figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"]
        )
        # ax_hist = fig.gca()
        plt.hist(
            qualities,
            bins=bins,
            **hist_kwargs,
        )
        plt.xlabel(fig_dict["xlabel"])
        plt.ylabel(fig_dict["ylabel"])
        plt.xlim(fig_dict["hist_x"])
        plt.ylim(fig_dict["hist_y"])
        # ax_hist.legend(loc=fig_dict["legend_loc"])
        plt.grid(True)

        if fig_dict["serialize"]:
            # filename = script_name + "_convergence_log" + ".png"
            # pathfilename = Path.cwd().joinpath(filename)
            # fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
            fig.savefig(figure_path_file, bbox_inches="tight", pad_inches=0)
            print(f"{atmesh} Serialized to {figure_path_file}")

    # Now create a single plot the accumlates all the scaled
    # Jacobian data across all stl_path_files and plots their
    # quatilies side-by-side

    # for Mean Scaled Jacobian data sets from stl_path_files, e.g.,
    # ~/autotwin/data/octa/octa_loop03_sj.csv
    # ~/autotwin/data/octa/octa_loop04_sj.csv

    # boxplot for each iii in stl_path_files

    # xabels as 'loop03' and 'loop04' reflected from stl_path_files

    print(f"{atmesh} Script completed.")


if __name__ == "__main__":
    """Runs the module from the command line."""
    main()
