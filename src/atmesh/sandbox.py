"""Area for testing ideas."""

import argparse
from typing import NamedTuple
import platform
from pathlib import Path

# import pytest
import numpy as np


class CubitMachines(NamedTuple):
    """Lists the local machines with a Cubit installation."""

    names = ["s1088757"]


def run_only_on_cubit_machines(func):
    """To come."""

    def wrapper_func():
        current_machine = platform.uname().node.lower()
        test_machines = [machine.lower() for machine in CubitMachines().names]
        if current_machine not in test_machines:
            pytest.skip("Skip test since Cubit is not installed.")
        else:
            func()

    return wrapper_func


def numpy_io(path_input: Path):
    """Given a path to a .npy semantic segmentation."""

    path_input = path_input.expanduser()

    if not path_input.exists():
        raise FileNotFoundError(f"Path not found: {path_input}")

    aa = np.array((0, 0, 0, 1, 2, 3, 0, 2, 1, 0))
    bb = np.trim_zeros(aa)

    db = np.load(str(path_input))

    breakpoint()


def main():
    """Runs the module from the command line, invoked from pyproject.toml
    with 'sculpt_io' command.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path_input", help="the path to input .npy segmentation file")
    args = parser.parse_args()
    path_input = args.path_input

    numpy_io(path_input=Path(path_input))


if __name__ == "__main__":
    main()
