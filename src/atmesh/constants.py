"""This module stores constants values in a single location for the module."""

from typing import NamedTuple
import platform

import pytest


class Constants(NamedTuple):
    """Creates all constants used in this module."""

    yml_schema_version = 1.6
    module_name = "atmesh"
    module_prompt = module_name + ">"
    test_machines = ["atlas", "s1060600", "s1088757", "skybridge"]


def run_on_cubit_machine(func):
    """Only run on a machine that only has as Cubit installation."""

    def wrapper_func():

        current_machine = platform.uname().node.lower()
        test_machines = [x.lower() for x in Constants().test_machines]

        if current_machine not in test_machines:
            pytest.skip("Only run on a test machine with Cubit installed.")

    return wrapper_func
