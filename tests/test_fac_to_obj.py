"""This module is a unit test for the facet to object file translation.

To run:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_fac_to_obj.py -v

For coverage:
(atmeshenv) ~/autotwin/mesh> pytest tests/test_fac_to_obj.py --cov=src/atmesh --cov-report term-missing
"""

import hashlib
from pathlib import Path
import sys

import pytest

import atmesh.fac_to_obj as translator


def test_file_bad():
    """Given a file name or path that does not exist, checks that the
    function raises a FileNotFoundError."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_file = data_path.joinpath("this_file_does_not_exist.fac")

    with pytest.raises(FileNotFoundError) as error:
        translator.translate(path_file_input=str(input_file))
    assert error.typename == "FileNotFoundError"


@pytest.mark.skipif(
    sys.platform == "win32", reason="Windows md5 is not the same as Linux and macOS"
)
def test_cube_translation():
    """Given an exemplar input file ~/autotwin/mesh/tests/files/cube.fac,
    check that it is translated into ~/autotwin/mesh/cube.obj and
    has the same md5 has as ground truth tranlated file at
    ~/autotwin/mesh/tests/files/cube.obj.
    """
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_file = data_path.joinpath("cube.fac")
    output_file = data_path.joinpath("cube.obj")

    # assert, prior to translation, that
    # (a) the input file exists and
    assert input_file.is_file()
    # (b) the output file does not exist
    assert not output_file.is_file()

    translated = translator.translate(path_file_input=str(input_file))
    assert translated

    # assert the output file now does exist
    assert output_file.is_file()

    # Correct original md5 goes here
    known_md5 = "655eed985dcaa29853f6ed50e9df7683"

    # open, read file and calculate the md5, close
    with open(str(output_file), "rb") as fstream:
        # read contents of the file
        data = fstream.read()
        # pipe contents of the file through
        found_md5 = hashlib.md5(data).hexdigest()

        # assert known_md5 == found_md5
    assert known_md5 == found_md5

    # clean up, delete the output file
    output_file.unlink()

    # confirm the output file no longer exists
    assert not output_file.is_file()
