"""This module assures that the cubit_delete_blocks can be run successfully.

To run:
cd ~/autotwin/mesh
source .venv/bin/activate.fish
arch -x86_64 pytest tests/test_cubit_delete_blocks.py -vs  # --capture=no
"""

from pathlib import Path
import sys

import atmesh.cubit_delete_blocks as cdb


def test_cubit_delete_blocks():
    """The main test harness for cubit_delete_blocks."""
    self_path = Path(__file__)
    yml_file = "IXI012-HH-1211-T1_tiny_test.yml"
    yml_input_file = self_path.parent.joinpath("files", yml_file)

    cubit_path = "/Applications/Cubit-16.14/Cubit.app/Contents/MacOS"
    sys.path.append(cubit_path)

    print("Import cubit module initiatied:")
    import cubit

    # stop journaling for this test
    # cubit.init  # journaling is ON
    cubit.init(["cubit", "-nojournal"])  # journaling is OFF

    breakpoint()

    result = cdb.cubit_delete_blocks(yml_input_file=yml_input_file)

    assert result == 0  # success, no error codes
    aa = 4
