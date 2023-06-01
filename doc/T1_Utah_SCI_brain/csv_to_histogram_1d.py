"""This self-contained script (not software) takes a population in .csv format, and
produces a histogram (with optional box and whisker plot) visual representation of the
population data.

To run:
> cd ~/autotwin/mesh
~/autotwin/mesh> source .venv/bin/activate.fish
(.venv) ~/autotwin/mesh> python doc/T1_Utah_SCI_brain/histogram_1d.py
"""

from pathlib import Path

from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np


def main():
    """User input begin"""
    path_to_files = "~/Downloads/scratch/Utah_SCI_brain/"
    # files = (
    #     "cell_size_8.0_2023-05-22_UTC_20_50_44_794153_scaled_jacobian.csv",
    #     "cell_size_4.0_2023-05-22_UTC_20_50_44_795467_scaled_jacobian.csv",
    #     "cell_size_2.0_2023-05-22_UTC_20_50_44_796321_scaled_jacobian.csv",
    # )
    files = ("cell_size_8.0_2023-05-22_UTC_20_50_44_794153_scaled_jacobian.csv",)
    fig_dict = {
        "title": "Utah SCI Brain Mesh Quality Metric",
        "xlabel": "Quality",
        "ylabel": "Number of Elements",
        "hist_x": [0.0, 1.0],
        "hist_y": [0.6, 6000],
        "legend_loc": "upper left",
        "n_bins": 7,
        "height": 4.0,
        "width": 6.0,
        "dpi": 300,
        "serialize": True,
        "output_file_ext": "png",
        "figure_shown": False,
        "latex": False,
    }
    histogram_dict = {
        "alpha": 0.6,
        "color": "blue",
        "histtype": "step",
        "linewidth": 2,
    }
    """User input end"""

    # script_name = Path(__file__).stem
    script_path = Path(__file__).parent

    # file io
    for item in files:

        fin = Path(path_to_files + item).expanduser()
        fin_stem = Path(item).stem
        print(f"Reading file {fin}")
        population = np.genfromtxt(fname=fin, delimiter=",", usecols=(1,))

        plt.ioff()  # turn off interactive mode
        # fig = plt.figure(
        #     figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"]
        # )
        # fig = plt.figure()
        # fig, ax = plt.subplots()
        fig, ax = plt.subplots(
            figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"]
        )

        # TODO: function to overwrite the fig_dict["title"] for each file item
        xmin, xmax = fig_dict["hist_x"]
        n_bins = fig_dict["n_bins"]
        delta_bin = (xmax - xmin) / n_bins
        bins = [xmin + delta_bin * x for x in range(n_bins + 1)]

        print(f"n_bins: {n_bins}")
        print(f"delta_bin: {delta_bin}")
        print(f"bins: {bins}")

        if fig_dict["latex"]:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)

        ax.hist(
            population,
            bins=bins,
            label="label to come",
            **histogram_dict,
        )

        ax.set_xlabel(fig_dict["xlabel"])
        ax.set_ylabel(fig_dict["ylabel"])
        title_and_file_id = fig_dict["title"] + "\n" + item
        # plt.title(fig_dict["title"])
        ax.set_title(title_and_file_id)

        # hist_x = fig_dict["hist_x"]
        # # plt.xlim(fig_dict["hist_x"])
        # plt.xlim(hist_x)

        # plt.ylim(fig_dict["hist_y"])

        if fig_dict["figure_shown"]:
            aa = 4
            plt.show()
        else:
            bb = 4
            plt.show(block=False)

        if fig_dict["serialize"]:
            filename = fin_stem + "." + fig_dict["output_file_ext"]
            pathfilename = str(script_path.joinpath(filename))
            fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
            print(f"Serialized to {pathfilename}")


if __name__ == "__main__":
    """Runs this module from the command line."""
    main()
