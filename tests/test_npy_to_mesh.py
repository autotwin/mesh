"""This module tests input of voxels to a finite element mesh.

Example:
    cd ~/autotwin/mesh
    source .venv/bin/activate.fish
    pytest tests/test_npy_to_mesh.py -v

    # To test a single function:
    pytest tests/test_npy_to_mesh.py::test_npy_to_spn -s
"""

from pathlib import Path

import numpy as np

import atmesh.npy_to_mesh as npm
import atmesh.utility as ut


def test_npy_to_spn():
    """Tests that a .npy file can be converted to a .spn file."""
    tests = Path(__file__).parent
    files = tests.joinpath("files")
    letter_f_encode = np.array(
        [
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
        ],
        dtype=np.uint8,
    )

    letter_f_fiducial_spn = files.joinpath("letter_f_fiducial.spn")
    # -----------------------
    # fiducial creation begin
    # create a fiducial npy file, once it is saved, commend out the following
    # four lines and commit the files to the repo once and for all:
    #    letter_f_fiducial_npy = files.joinpath("letter_f_fiducial.npy")
    #    np.save(file=letter_f_fiducial_npy, arr=letter_f_encode)
    #    flattened = letter_f_encode.flatten()  # overwrite structure
    #    np.savetxt(fname=letter_f_fiducial_spn, X=flattened, fmt="%s")
    # fiducial creation end
    # ---------------------

    # create another test file identical to the fiducial npy file
    # as the stem name of the test npy file becomes the name of the test
    # spn file.
    input_npy = files.joinpath("letter_f_temp.npy")
    np.save(file=input_npy, arr=letter_f_encode)

    result = npm.npy_to_spn(npy_input_file=input_npy)

    assert ut.compare_files(letter_f_fiducial_spn, result, [])

    # remove at end of test
    input_npy.unlink()
    result.unlink()


def test_npy_to_mesh():
    """Tests that the .yml recipe with an existing .spn file can be converted
    to a mesh.
    """
    recipe = Path(__file__).parent.joinpath("files", "letter_f_autotwin.yml")

    result = npm.npy_to_mesh(yml_input_file=recipe)

    assert result == 0  # no errors


def test_npy_to_spn_and_mesh_ixi():
    """Tests the npy_to_mesh workflow on the 'tiny' version of a single IXI
    patient data."""
    tests = Path(__file__).parent
    files = tests.joinpath("files")

    input_npy = files.joinpath("IXI012-HH-1211-T1_tiny_test.npy")
    result = npm.npy_to_spn(npy_input_file=input_npy)

    fiducial_spn = files.joinpath("IXI012-HH-1211-T1_tiny_test_fiducial.spn")
    assert fiducial_spn.is_file()

    assert ut.compare_files(fiducial_spn, result, [])

    # remove at end of test
    result.unlink()

    recipe = files.joinpath("IXI012-HH-1211-T1_tiny_test.yml")
    assert recipe.is_file()

    result_exodus = npm.npy_to_mesh(yml_input_file=recipe)
    assert result_exodus == 0  # no errors
