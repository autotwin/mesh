from typing import NamedTuple
import platform
import pytest


class CubitMachines(NamedTuple):
    """Lists the local machines with a Cubit installation."""

    names = ["s1088757"]


def run_only_on_cubit_machines(func):
    """To come."""

    def wrapper_func():
        current_machine = platform.uname().node.lower()
        test_machines = [machine.lower() for machine in CubitMachines().names]
        if current_machine not in test_machines:
            pytest.skip("Skip test since Cubit is not installed.")
        else:
            func()

    return wrapper_func
