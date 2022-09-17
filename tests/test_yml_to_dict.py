"""This module is a unit test for .yml file input to dictionary.

To run:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_yml_to_dict -v
(atmeshenv) ~/autotwin/mesh> pytest tests/test_yml_to_dict -vs  # --capture=no

For coverage:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_yml_to_dict.py --cov=src/atmesh --cov-report term-missing
"""

from pathlib import Path

import pytest

# import atmesh.sculpt_stl_to_inp as translator
import atmesh.yml_to_dict as translator


@pytest.fixture
def keys():
    return ("version", "cubit_path", "working_dir", "stl_path_file", "inp_path_file")


def test_return_is_dict(keys):
    """Given a valid .yml file, checks that the return is of type dict."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_path_file = data_path.joinpath("sphere.yml")
    value = translator.yml_to_dict(
        yml_path_file=input_path_file, version=1.0, required_keys=keys
    )
    assert isinstance(value, dict)


def test_when_io_fails(keys):
    """Given a file name or a path that does not exist, checks that the
    function raises a FileNotFoundError."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()

    with pytest.raises(FileNotFoundError) as error:
        input_file = data_path.joinpath("this_file_does_not_exist.yml")
        translator.yml_to_dict(
            yml_path_file=input_file, version=1.0, required_keys=keys
        )
    assert error.typename == "FileNotFoundError"

    # If the user tries to run with a file type that is not a .yml or .yaml,
    # then check that a TypeError is raised.

    with pytest.raises(TypeError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_filetype.txt")
        translator.yml_to_dict(
            yml_path_file=input_file, version=1.0, required_keys=keys
        )
    assert error.typename == "TypeError"

    # If the user tried to run the input yml version that is not the version
    # curently implemented, then check that a ValueError is raised.

    with pytest.raises(ValueError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_version.yml")
        translator.yml_to_dict(
            yml_path_file=input_file, version=1.0, required_keys=keys
        )
    assert error.typename == "ValueError"

    # If the user tried to run the input yml that
    # does not have the correct keys, then test that a KeyError is raised.

    with pytest.raises(KeyError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_keys.yml")
        translator.yml_to_dict(
            yml_path_file=input_file, version=1.0, required_keys=keys
        )
    assert error.typename == "KeyError"

    """If the yaml cannot be loaded, then test that an OSError is raised."""
    with pytest.raises(OSError) as error:
        input_file = data_path.joinpath("sculpt_stl_to_inp_bad_yaml_load.yml")
        translator.yml_to_dict(
            yml_path_file=input_file, version=1.0, required_keys=keys
        )
    assert error.typename == "OSError"
