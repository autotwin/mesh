"""This module stores constants values in a single location for the module."""

from typing import NamedTuple


class Constants(NamedTuple):
    """Creates all constants used in this module."""

    yml_schema_version = 1.6
    module_name = "atmesh"
    module_prompt = module_name + ">"
