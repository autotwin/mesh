"""This module is a unit test for .inp file input to minimum
scaled Jacobian .csv file output via Cubit translation.

To run:
(.venv) ~/autotwin/mesh> arch -x86_64 pytest tests/test_cubit_inp_to_minsj_csv.py -v
(.venv) ~/autotwin/mesh> arch -x86_64 pytest tests/test_cubit_inp_to_minsj_csv.py -vs  # --capture=no

For coverage:
(.venv) ~/autotwin/mesh> arch -x86_64 pytest tests/test_cubit_inp_to_minsj_csv.py --cov=src/atmesh --cov-report term-missing

For help:
(.venv) ~/chovey/autotwin/mesh> arch -x86_64 python src/atmesh/cubit_inp_to_quality_csv.py --help

usage: cubit_inp_to_quality_csv.py [-h] input_file quality_metrics

positional arguments:
  input_file       the .yml user input file
  quality_metrics  tuple of quality strings from ('aspect ratio', 'scaled jacobian', 'skew')

options:
  -h, --help       show this help message and exit
"""


# import os
from pathlib import Path
import platform

import pytest

# import atmesh.cubit_inp_to_minsj_csv as translator
import atmesh.cubit_inp_to_quality_csv as translator


@pytest.mark.skipif(
    ("atlas" not in platform.uname().node.lower())
    and ("1060600" not in platform.uname().node)
    and ("1088757" not in platform.uname().node),
    reason="Run on Atlas and local machines only.",
)
def test_known_element_count():
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_path_file = data_path.joinpath("sphere_minsj.yml")
    qms = ("scaled jacobian",)  # quality metrics
    found = translator.translate(
        path_file_input=str(input_path_file), quality_metrics=qms
    )
    known = 352  # number of hex elements

    assert known == found


def test_unknown_quality_metric():
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    input_path_file = data_path.joinpath("sphere_minsj.yml")
    quality_metric_bad_input = ("foo",)
    with pytest.raises(ValueError) as error:
        translator.translate(
            path_file_input=str(input_path_file),
            quality_metrics=quality_metric_bad_input,
        )
    assert error.typename == "ValueError"
