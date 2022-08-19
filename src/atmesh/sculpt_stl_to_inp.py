"""This module uses Cubit to convert a .stl file into a .inp file using Sculpt

Prerequisites:
* Python 3.7.4 is required to run Cubit 16.06 and Sculpt.
* We actually use Python 3.7.9 successfully for now.

Methods:
> cd ~/autotwin/mesh/src/atmesh

* Interactive Method
# > /usr/local/bin/python3.7 sculpt_stl_to_inp.py
> python --version
  Python 3.7.9
> python sculpt_stl_to_inp.py

* Log Method
# > /usr/local/bin/python3.7 sculpt_stl_to_inp.py > sculpt_stl_to_inp.log
> python sculpt_stl_to_inp.py > sculpt_stl_to_inp.log

Example:
~/autotwin/mesh> source atmeshenv/bin/activate.fish # (atmeshenv) uses Python 3.7
(atmeshenv) cbh@atlas/Users/cbh/autotwin/mesh> cd src/atmesh

"""
import sys
from pathlib import Path

# from typing import Final # Final is new in Python 3.8, Cubit uses 3.7

# atmesh: Final[str] = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7
atmesh: str = "atmesh>"  # Final is new in Python 3.8, Cubit uses 3.7

print(f"{atmesh} This is {Path(__file__).resolve()}")

# user input file begin
user_input = {
    "cubit_path": "/Applications/Cubit-16.06/Cubit.app/Contents/MacOS",
    #
    "working_dir": "~/autotwin/data/octa",
    "stl_path_file": "~/autotwin/data/octa/octa_loop07.stl",
    "inp_path_file": "~/autotwin/data/octa/octa_loop07.inp",
    #
    # "working_dir": "~/autotwin/mesh/tests/files",
    # "stl_path_file": "~/autotwin/mesh/tests/files/sphere.stl",
    # "inp_path_file": "~/autotwin/mesh/tests/files/sphere.inp",
    #
    # "working_dir"  : "~/autotwin/mesh/data",
    # "stl_path_file": "~/autotwin/mesh/data/bunny_20cm.stl",
    # "inp_path_file": "~/autotwin/mesh/data/bunny_20cm.inp",
}
# user input file end

print(f"{atmesh} User input:")
for key, value in user_input.items():
    print(f"  {key}: {value}")

cubit_path = user_input["cubit_path"]
inp_path_file = user_input["inp_path_file"]
stl_path_file = user_input["stl_path_file"]
working_dir = user_input["working_dir"]

for item in [cubit_path, working_dir]:
    if not Path(item).expanduser().is_dir():
        raise OSError(f"{atmesh} Path not found: {item}")

for item in [stl_path_file]:
    if not Path(item).expanduser().is_file():
        raise OSError(f"{atmesh} File not found: {item}")

for item in [inp_path_file]:
    if not Path(Path(item).expanduser().parent).is_dir():
        raise OSError(f"{atmesh} Path not found: {item}")

# append the cubit path to the system Python path
print(f"{atmesh} Existing sys.path:")
for item in sys.path:
    print(f"  {item}")

sys.path.append(cubit_path)

print(f"{atmesh} Cubit path now added:")
for item in sys.path:
    print(f"  {item}")

try:
    print(f"{atmesh} Import cubit module initiatied:")
    import cubit

    cubit.init
    print(f"{atmesh} Import cubit module completed.")

    # cubit.cmd('cd "~/sibl-dev/sculpt/tests/sphere-python"')
    cc = 'cd "' + working_dir + '"'
    cubit.cmd(cc)
    print(f"{atmesh} The Cubit Working Directory is set to: {working_dir}")

    print(f"{atmesh} stl import initiatied:")
    print(f"{atmesh} Importing stl file: {stl_path_file}")
    cc = 'import stl "' + stl_path_file + '"'
    cubit.cmd(cc)
    print(f"{atmesh} stl import completed.")

    print(f"{atmesh} Sculpt parallel initiated:")
    cc = "sculpt parallel"
    cubit.cmd(cc)
    print(f"{atmesh} Sculpt parallel completed.")

    print(f"{atmesh} Abaqus file export initiated:")
    print(f"{atmesh} Exporting inp file: {inp_path_file}")
    cc = 'export abaqus "' + inp_path_file + '" overwrite'
    cubit.cmd(cc)
    print(f"{atmesh} Abaqus file export completed.")

    # print(f"{atmesh} Script: {Path(__file__).resolve()} has completed.")
    print(f"{atmesh} Done.")

except ModuleNotFoundError as err:
    print("unable to import cubit")
    print(f"{atmesh} {err}")
