"""This module converts a yml file into a dictionary, while also
assuring the yml file has the correct version number and correct
key(s) present in the file.
"""

from pathlib import Path

import yaml

from typing import Dict, Tuple


def yml_to_dict(
    *, yml_path_file: Path, version: float, required_keys: Tuple[str, ...]
) -> Dict:
    """Given a valid Path to a yml input file, read it in and
    return the result as a dictionary.

    yml_path_file (Path): The fully pathed location to the input file.
    version (float): The version of the yml in x.y format.
    required_keys (tuple[str,...]): The key(s) that must be in the yml file for
        conversion to a dictionary to occur.

    """

    # Compared to the lower() method, the casefold() method is stronger.
    # It will convert more characters into lower case, and will find more matches
    # on comparison of two strings that are both are converted
    # using the casefold() method.
    file_type = yml_path_file.suffix.casefold()

    supported_types = (".yaml", ".yml")

    if file_type not in supported_types:
        raise TypeError("Only file types .yaml, and .yml are supported.")

    try:
        with open(yml_path_file, "r") as stream:
            # See deprecation warning for plain yaml.load(input) at
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            db = yaml.load(stream, Loader=yaml.SafeLoader)
    except yaml.YAMLError as error:
        print(f"Error with YAML file: {error}")
        # print(f"Could not open: {self.self.path_file_in}")
        print(f"Could not open or decode: {yml_path_file}")
        # raise yaml.YAMLError
        raise OSError

    version_specified = db.get("version")
    # version_implemented = 1.0
    version_implemented = version

    if version_specified < version_implemented:
        raise ValueError(
            f"Version mismatch: specified was {version_specified}, implemented is {version_implemented}"
        )
    else:
        # check keys found in input file against required keys
        found_keys = tuple(db.keys())
        keys_exist = tuple(map(lambda x: x in found_keys, required_keys))
        has_required_keys = all(keys_exist)
        if not has_required_keys:
            raise KeyError(f"Input files must have these keys defined: {required_keys}")
    return db
