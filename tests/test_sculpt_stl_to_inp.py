"""This module is a unit test for .stl file input to .inp file output via
Cubit and Sculpt for translation.

To run:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp -v
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp -vs  # --capture=no

For coverage:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp.py --cov=src/atmesh --cov-report term-missing
"""


# import os
from pathlib import Path
import platform
import sys

import pytest

import atmesh.sculpt_stl_to_inp as translator


def test_when_io_fails():
    """Given a file name or a path that does not exist, checks that the
    function raises a FileNotFoundError."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()

    with pytest.raises(FileNotFoundError) as error:
        input_file = data_path.joinpath("this_file_does_not_exist.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "FileNotFoundError"

    # If the user tries to run with a file type that is not a .yml or .yaml,
    # then check that a TypeError is raised.

    with pytest.raises(TypeError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_filetype.txt")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "TypeError"

    # If the user tried to run the input yml version that is not the version
    # curently implemented, then check that a ValueError is raised.

    with pytest.raises(ValueError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_version.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "ValueError"

    # If the user tried to run the input yml that
    # does not have the correct keys, then test that a KeyError is raised.

    with pytest.raises(KeyError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_keys.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "KeyError"

    """If the yaml cannot be loaded, then test that an OSError is raised."""
    with pytest.raises(OSError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_yaml_load.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "OSError"


@pytest.mark.skipif(
    ("atlas" not in platform.uname().node.lower())
    and ("1060600" not in platform.uname().node)
    and ("1088757" not in platform.uname().node),
    reason="Run on Atlas and local machines only.",
)
def test_cubit_init():
    """Given a path to the Cubit/Sculpt binary, check that cubit.init and the
    current working directory can be set to the path of the test script.
    """
    # cubit_path = "/Applications/Cubit-16.06/Cubit.app/Contents/MacOS"
    cubit_path = "/Applications/Cubit-16.08/Cubit.app/Contents/MacOS"
    sys.path.append(cubit_path)

    print("Import cubit module initiatied:")
    import cubit

    # stop journaling for this test
    # cubit.init  # journaling is ON
    cubit.init(["cubit", "-nojournal"])  # journaling is OFF

    print("Import cubit module completed.")

    # working_dir = Path(__file__).resolve()
    working_dir = Path(__file__).parent
    working_dir_str = str(working_dir)
    print(f"This is {working_dir_str}")

    cc = 'cd "' + working_dir_str + '"'
    success = cubit.cmd(cc)
    print(f"The Cubit Working Directory is set to: {working_dir_str}")

    assert success


# @pytest.mark.skipif(
#     ("atlas" not in platform.uname().node.lower())
#     and ("1060600" not in platform.uname().node),
#     reason="Run on Atlas and local machines only.",
# )
@pytest.mark.skip("work in progress")
def test_import_cubit_fails():
    """Currently with CI/CD, we have no way to test Cubit and Sculpt, so test
    that a ModuleNotFoundError is raised."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()

    with pytest.raises(ModuleNotFoundError) as error:
        input_file = data_path.joinpath("sphere.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "ModuleNotFoundError"
