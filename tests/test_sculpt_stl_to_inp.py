"""This module is a unit test for .stl file input to .inp file output via Cubit and Sculp for translation.

To run:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp -v

For coverage:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_sculpt_stl_to_inp.py --cov=src/atmesh --cov-report term-missing
"""


from pathlib import Path

import pytest

import atmesh.sculpt_stl_to_inp as translator


def test_file_bad():
    """Given a file name or a path that does not exist, checks that the
    function riases a FileNotFoundError."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_file = data_path.joinpath("this_file_does_not_exist.yml")

    with pytest.raises(FileNotFoundError) as error:
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "FileNotFoundError"
