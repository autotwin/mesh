from pathlib import Path

import numpy as np

import atmesh.sandbox as sb


def test_no_decorator():
    # assert 4 == 1
    assert 1 == 1


def test_numpy_io():

    tests = Path(__file__).parent
    files = tests.joinpath("files")

    # the capital letter F with the [z, y, x] = (4, 5, 3) matrix:
    # [
    # [[1, 1, 1],
    #  [1, 1, 1],
    #  [1, 1, 1],
    #  [1, 1, 1],
    #  [1, 1, 1]],
    #
    # [[1, 1, 1],
    #  [1, 0, 0],
    #  [1, 1, 0],
    #  [1, 0, 0],
    #  [1, 0, 0]],
    #
    # [[1, 1, 1],
    #  [1, 0, 0],
    #  [1, 1, 0],
    #  [1, 0, 0],
    #  [1, 0, 0]],
    #
    # [[1, 1, 1],
    #  [1, 0, 0],
    #  [1, 1, 0],
    #  [1, 0, 0],
    #  [1, 0, 0]]
    # ]

    letter_f_encode = np.array(
        [
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
            [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
        ],
        dtype=np.uint8,
    )

    letter_f = files.joinpath("letter_f.npy")
    np.save(file=letter_f, arr=letter_f_encode)

    flattened = letter_f_encode.flatten()  # overwrite structure

    letter_f_ascii = files.joinpath("letter_f.spn")
    np.savetxt(fname=letter_f_ascii, X=flattened, fmt="%s")

    sb.numpy_io(path_input=letter_f)

    breakpoint()

    # ixi = files.joinpath("IXI012-HH-1211-T1_small.npy")
    # sb.numpy_io(path_input=ixi)


@sb.run_only_on_cubit_machines
def test_decorator():
    # assert 4 == 1
    assert 1 == 1
