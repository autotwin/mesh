"""This module uses Cubit to convert a .stl file into a .inp file using Sculpt

Prerequisites:
* Python 3.7.4 is required to run Cubit 16.06 and Sculpt.

Methods:
> cd ~/autotwin/mesh/src

* Interactive Method
> /usr/local/bin/python3.7 sculpt_stl_to_inp.py  

* Log Method
> /usr/local/bin/python3.7 sculpt_stl_to_inp.py > sculpt_stl_to_inp.log

"""
import sys
from pathlib import Path

print(f"--> This is {Path(__file__).resolve()}")

# user input file begin
user_input = {
    "cubit_path"   : "/Applications/Cubit-16.06/Cubit.app/Contents/MacOS",
    "inp_path_file": "~/autotwin/mesh/tests/files/sphere.inp",
    "stl_path_file": "~/autotwin/mesh/tests/files/sphere.stl",
    "working_dir"  : "~/autotwin/mesh/tests/files",
}
# user input file end

print("--> User input:")
for key, value in user_input.items():
    print(f"{key}: {value}")

cubit_path = user_input["cubit_path"]
inp_path_file = user_input["inp_path_file"]
stl_path_file = user_input["stl_path_file"]
working_dir = user_input["working_dir"]

for item in [cubit_path, working_dir]:
    if not Path(item).expanduser().is_dir():
        raise OSError(f"Path not found: {item}")

for item in [stl_path_file]:
    if not Path(item).expanduser().is_file():
        raise OSError(f"File not found: {item}")

for item in [inp_path_file]:
    if not Path(Path(item).expanduser().parent).is_dir():
        raise OSError(f"Path not found: {item}")


# append the cubit path to the system Python path
print("--> Existing sys.path:")
for item in sys.path:
    print(f"{item}")

sys.path.append(cubit_path)

print("--> Cubit path now added:")
for item in sys.path:
    print(f"{item}")

try:
    import cubit
    cubit.init
    print("cubit.init successful")

    print(f"Working directory: {working_dir}")
    # cubit.cmd('cd "~/sibl-dev/sculpt/tests/sphere-python"')
    cc = 'cd "' + working_dir + '"'
    cubit.cmd(cc)

    print(f"--> Importing stl file: {stl_path_file}")
    cc = 'import stl "' + stl_path_file + '"'
    cubit.cmd(cc)

    print("--> Starting Sculpt parallel")
    cc = 'sculpt parallel'
    cubit.cmd(cc)

    print(f"--> Exporting inp file: {inp_path_file}")
    cc = 'export abaqus "' + inp_path_file + '"'
    cubit.cmd(cc)

except ModuleNotFoundError as err:
    print("unable to import cubit")
    print(f"{err}")

