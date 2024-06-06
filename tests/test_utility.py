"""This module tests the utility module.
"""

from pathlib import Path

import atmesh.utility as ut


def test_compare_files():
    """Tests that files of unequal length are different, files of equal length
    but with different lines are different, files of equal length but with
    different specified ignore_words are the same, and a file compared to
    itself is the same.
    """

    files = Path(__file__).parent.joinpath("files")

    file_two_lines = files.joinpath("testing_two_lines.txt")
    file_three_lines = files.joinpath("testing_three_lines.txt")
    file_three_lines_aug = files.joinpath("testing_three_lines_augmented.txt")

    assert not ut.compare_files(file_two_lines, file_three_lines, [])

    assert not ut.compare_files(file_three_lines, file_three_lines_aug, [])

    assert ut.compare_files(
        file_three_lines, file_three_lines_aug, ["two", "augmented"]
    )

    assert ut.compare_files(file_two_lines, file_two_lines, [])


def test_underline():
    """Tests that the underline function has 78 dashes, a leading asterisk,
    and a final newline character.
    """
    aa = ut.underline()
    assert len(aa) == 81
    assert aa[0] == "#"
    assert aa[1] == " "
    assert all(["-" in x for x in aa[2:80]])
    assert aa[80] == "\n"
