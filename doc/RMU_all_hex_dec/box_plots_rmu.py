"""This module converts the .csv file into a box plot.

Prerequisites:
* Python 3.11 (deprecated 2023-03-13 Python 3.7.9)
* atmesh virtual environment

To run:
> cd ~/autotwin/mesh

# activate the venv at meshenv
> source atmeshenv/bin/activate  # or activate.fish if using fish shell
> python doc/all_hex_dec/box_plots_rmu.py

"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

import numpy as np


def main():
    # user input begin
    path_file_data = (
        "~/Downloads/scratch/Utah_SCI_brain/cell_100_msj.csv",
        "~/Downloads/scratch/all_hex_dec/msj.csv",
    )
    fig_dict = {
        "title": "Utah SCI (left) v. RMU All Hex Dec (right)",
        "xlabel": "Element Count",
        "ylabel": "Minimum Scaled Jacobian Distribution",
        "hist_x": [0.4, 1.0],
        "hist_y": [0.6, 6000],
        "legend_loc": "upper left",
        "height": 6.0,
        "width": 6.0,
        "dpi": 300,
        "serialize": True,
        "figure_shown": False,
    }
    # breakpoint()
    # hist_kwargs = {
    #     # "histtype": "step",
    #     "alpha": 0.9,
    #     "linewidth": 2,
    #     "color": "blue",
    # }
    n_bins = 7
    # delta_bin = 1.0 / n_bins
    xmin, xmax = fig_dict["hist_x"]
    delta_bin = (xmax - xmin) / n_bins
    # bins = [delta_bin * x for x in range(n_bins + 1)]
    bins = [xmin + delta_bin * x for x in range(n_bins + 1)]
    # latex = True
    latex = False
    # user input end
    # --------------
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    print(f"n_bins: {n_bins}")
    print(f"delta_bin: {delta_bin}")
    print(f"bins: {bins}")

    counts = []  # empty list of element count
    qualities = []  # empty list of minsj quality
    for item in path_file_data:

        fin = Path(item).expanduser()

        print(f"Reading file {fin}")
        qual = np.genfromtxt(fname=fin, delimiter=",", usecols=(1,))
        counts.append(len(qual))
        qualities.append(qual)

    # plt.figure()
    # fig = plt.figure()
    fig = plt.figure(
        figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"]
    )
    # plt.ioff()  # interactive mode to OFF
    # plt.ion()  # interactive mode to ON
    # breakpoint()
    # for iii in range(len(counts)):
    #     plt.boxplot(qualities_cell[iii][:], positions=[iii + 1])
    #     # plt.boxplot(qualities_cell[iii][:], positions=[iii])
    flierprops = dict(
        linestyle="none",
        marker=".",
        markerfacecolor="blue",
        markeredgecolor="none",
        markersize=3,
    )
    plt.boxplot(qualities, labels=counts, flierprops=flierprops)

    # plt.title("Minimum Scaled Jacobian by Case Element Count")
    plt.title(fig_dict["title"])

    # plt.xlabel("Element Count")
    plt.xlabel(fig_dict["xlabel"])

    # plt.ylabel("Minimum Scaled Jacobian Distribution")
    plt.ylabel(fig_dict["ylabel"])

    # plt.show()

    if fig_dict["serialize"]:
        path_file_script = Path(__file__)
        parent = path_file_script.parent
        stem = path_file_script.stem
        fig_extension = ".png"
        fig_file = stem + fig_extension
        figure_path_file_str = str(parent.joinpath(fig_file))
        # filename = script_name + "_convergence_log" + ".png"
        # pathfilename = Path.cwd().joinpath(filename)
        # fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
        fig.savefig(figure_path_file_str, bbox_inches="tight", pad_inches=0.25)
        print(f"Serialized to {figure_path_file_str}")


if __name__ == "__main__":
    """Runs the module from the command line."""
    main()
