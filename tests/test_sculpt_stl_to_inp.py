"""This module is a unit test for .stl file input to .inp file output via Cubit and Sculp for translation.

To run:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp -v

For coverage:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp.py --cov=src/atmesh --cov-report term-missing
"""


# import os
from pathlib import Path
import platform

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

    """If the user tries to run with a file type that is not a .yml or .yaml, then check that a TypeError is raised."""

    with pytest.raises(TypeError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_filetype.txt")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "TypeError"

    """If the user tried to run the input yml version that is not the version curently implemented, then check that a ValueError is raised."""

    with pytest.raises(ValueError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_version.yml")
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "ValueError"

    """If the user tried to run the input yml that
    does not have the correct keys, then test that a KeyError is raised."""

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
    platform.uname().node != "atlas.lan",
    reason="Only test on local development machine",
)
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
